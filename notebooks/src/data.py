'''P1'''
import re
import pandas as pd
LABELS = ("Persistence", "Discovery", "Defense Evasion", "Execution", "Impact", "Other", "Harmless")
SEED = 42

def load_dataset(path):
    df = pd.read_parquet(path)

    if {"full_session", "session_id"} - set(df.columns):
        raise ValueError("{full_session, session_i} are not present but they are mandatory")

    if not df["session_id"].is_unique:
        raise ValueError("IDs must be unique")

    return df


def split_tokenize(text: str) -> list[str]:
    """ First tokenization attempt : simple split of the full_session """
    return text.split()


# Section 1.5 - template groups
_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")   # ' ' | " "
_DIGITS = re.compile(r"[0-9]+")


def mask_values(texts: pd.Series) -> pd.Series:
    return texts.str.replace(_QUOTED, "<STR>", regex=True).str.replace(_DIGITS, "<N>", regex=True)


def session_templates(texts: pd.Series) -> pd.Series:
    """Template of each session

    1. quoted strings      -> <STR>   (passwords, credentials)
    2. numbers             -> <N>     (random numbers in file names)
    3. words found in only one session of the dataset -> <RARE>  (random tags)
    """
    masked = mask_values(texts)
    words = masked.map(str.split)
        # -> now in the Series every session is a list of words split by ' '

    # Count in how many sessions each word appears -> {word: number of sessions}
    sessions_per_word = {}
    for session in words:
        distinct_words = set(session)
        for word in distinct_words:
            if word in sessions_per_word:
                sessions_per_word[word] += 1
            else:
                sessions_per_word[word] = 1

    # Every word that is not present in more than 1 session is <RARE>
    return words.map(lambda session: " ".join(
        w if sessions_per_word[w] > 1 else "<RARE>" for w in session))


def template_groups(texts: pd.Series) -> pd.Series:
    """Group number of each session: same template = same group (0 = largest group)."""

    templates = session_templates(texts)

    # Counting how many sessions have each template -> {template: number of sessions}
    sessions_per_template = {}
    for template in templates:
        if template in sessions_per_template:
            sessions_per_template[template] += 1
        else:
            sessions_per_template[template] = 1

    # Sorting the templates from the most to the least frequent
    sorted_templates = sorted(sessions_per_template,
                              key=lambda template: sessions_per_template[template],
                              reverse=True)

    # Give each template a number: the most frequent becomes group 0 -> {template: group}
    group_of = {}
    number = 0
    for template in sorted_templates:
        group_of[template] = number
        number += 1

    # Returns an ordered Series containing the number of group to which each session is part
    return templates.map(group_of)

