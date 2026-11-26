'''P1'''
import re
from functools import lru_cache
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


# Section 1.3 - shell tokenization
#
# The tokenizer is made of explicit rules and works in two steps:
#   1. shell_tokenize -> where each token starts and ends
#   2. token_type     -> which kind of token it is (operator, option, path, ...)
# The text is never changed: case, quotes and backslashes stay as the attacker wrote them.

# ---- Step 1: where each token starts and ends ----

# Shell operators. A regex takes the first alternative that matches, so the longer
# operators are always written before the shorter ones ('&&' before '&').
_OPERATOR = (
    r"[0-9]?[<>]&[0-9]*-?"          # copy or close a file descriptor :  2>&1  1>&-
    r"|&>>?"                        # redirect stdout and stderr      :  &>  &>>
    r"|[0-9]?(?:>>|>\||>)"          # redirect the output             :  >  >>  2>  2>>
    r"|[0-9]?(?:<<<|<<-?|<>|<)"     # redirect the input              :  <  <<  <<<
    r"|\|\||\|&|\|"                 # "or", pipes                     :  ||  |&  |
    r"|&&|&"                        # "and", run in background        :  &&  &
    r"|;;|;"                        # end of a command                :  ;;  ;
    r"|\$\(|\(|\)|`"                # command inside another command  :  $(  (  )  `
)

# Quoted strings. Inside a string, a quote is the closing one only if after it there is a
# space, an operator or the end of the text. There are passwords that contain a quote:
#     echo "admin B"r0-Scherer" > /tmp/up.txt
# here the quote after B does not close the string (it is followed by a letter).
_NOT_CLOSING = r"(?![\s;|&<>()`]|$)"
_SINGLE_QUOTED = rf"'(?:[^']|'{_NOT_CLOSING})*'"
_DOUBLE_QUOTED = rf'"(?:[^"]|"{_NOT_CLOSING})*"'

# A character of a word outside the quotes: not a space, not a quote, not an operator.
# '$' is allowed if it does not start '$(' , so $HOME and $1 stay in one piece.
_PLAIN = r"""[^\s;|&<>()`'"$]|\$(?!\()"""

# A word can mix plain and quoted parts, as in bash: name="U6" is one token.
_WORD = rf"(?:{_SINGLE_QUOTED}|{_DOUBLE_QUOTED}|{_PLAIN})+"

# At each position we try an operator, then a word, then any single character
# (for example a quote that is never closed): in this way the tokenizer never fails.
_TOKEN = re.compile(rf"{_OPERATOR}|{_WORD}|\S")


def shell_tokenize(text: str) -> list[str]:
    """Rule-based shell tokenizer: the list of the tokens of a session."""
    return _TOKEN.findall(text)


# ---- Step 2: which kind of token it is ----

_ONLY_OPERATOR = re.compile(_OPERATOR)
_URL = re.compile(r"(?:https?|ftp)://", re.IGNORECASE)
_IP = re.compile(r"(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])")
_BASE64 = re.compile(r"[A-Za-z0-9+/]{100,}={0,2}")


def is_base64(token: str) -> bool:
    """True if the token contains a base64 text. The text is only recognized, it is NOT decoded.

    A base64 text uses only the characters of its alphabet and its length is a multiple of 4.
    At least 100 characters: shorter texts of the same characters are passwords, file names, ...
    """
    base64_text = _BASE64.search(token)
    return base64_text is not None and len(base64_text.group()) % 4 == 0


def token_type(token: str) -> str:
    """Type of a token. The rules are checked in this order and the first that matches wins.

    operator, quoted string, address, option, path, word
    """
    if _ONLY_OPERATOR.fullmatch(token):
        return "operator"
    if token[0] in "'\"":
        return "quoted string"
    if _URL.search(token) or _IP.search(token):     # a URL, or an IP with or without its port
        return "address"
    if token[0] == "-" and len(token) > 1:          # -l  -rf  --decode  (a lone '-' is a word)
        return "option"

    looks_like_path = "/" in token or token[0] in "~."      # /etc/passwd  ~/.ssh  .s
    if looks_like_path and not is_base64(token):            # a base64 text contains '/' too
        return "path"
    return "word"                                   # everything else: commands, arguments, numbers, ...


# ---- Comparison with an ordinary tokenizer ----

def how_lost(token: str, tokenizer) -> str:
    """Way in which an ordinary tokenizer loses a token, from what it gives for that token alone."""
    pieces = tokenizer(token)
    if len(pieces) == 0:
        return "removed"
    if len(pieces) > 1:
        return "cut"
    if pieces[0] != token:
        return "changed"
    return "glued"      # alone it is kept: if it is lost in a session, it is attached to something else


def lost_tokens(texts: pd.Series, tokenizer) -> pd.DataFrame:
    """One row for each token that the ordinary tokenizer loses in each session

    A token of shell_tokenize is lost in a session if the ordinary tokenizer never gives it there.
    """
    sessions = []
    tokens = []
    for session, text in texts.items():
        missing = set(shell_tokenize(text)) - set(tokenizer(text))      # tokens of the first set that are not in the second one
        for token in sorted(missing):
            sessions.append(session) # The index of the session where the token is lost
            tokens.append(token)

    lost = pd.DataFrame({"session": sessions, "token": tokens})

    # Type of each distinct token and way in which it is lost -> {token: type} and {token: way}
    distinct_tokens = set(tokens)
    lost["type"] = lost["token"].map({token: token_type(token) for token in distinct_tokens})
    lost["how"] = lost["token"].map({token: how_lost(token, tokenizer) for token in distinct_tokens})
    return lost


def lost_recap(texts: pd.Series, tokenizer) -> pd.DataFrame:
    """One row for each type of token and each way in which the ordinary tokenizer loses it

    n_sessions    : sessions with at least one token of that type lost in that way
    example       : the token lost in the largest number of sessions (example_sessions)
    given_instead : what the ordinary tokenizer gives instead of the example
    """
    lost = lost_tokens(texts, tokenizer)

    rows = []
    for (kind, how), group in lost.groupby(["type", "how"]):
        example = group["token"].mode()[0]
            # .mode() := the most frequent token, returns a Series with all the modes (there can be more than one), but we take the first one with [0]
        example_rows = group[group["token"] == example]
            # a Dataframe with one row for each session where the example is lost 

        given = tokenizer(example)
        # removed -> []   changed -> one token   cut -> all its pieces
        if how == "glued":
            # the longer token that contains the example, in the first session where it is lost
            text = texts[example_rows["session"].iloc[0]] # We take the text of the first session where the example is lost, searching by the index
            given = [token for token in tokenizer(text) if example in token][:1] 
            # Tokens that are given instead of the example, in that session, and we take the first one with [:1]
        rows.append({
            "type": kind,
            "how": how,
            "n_sessions": group["session"].nunique(),
            "example": example,
            "example_sessions": len(example_rows),
            "given_instead": given,
        })

    return pd.DataFrame(rows).sort_values("n_sessions", ascending=False)


# Section 1.4 - normalization
#
# The types of Section 1.3 are expanded where they mix different things, then the values that
# change from one session to another are replaced with a placeholder.

_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")      # LC_ALL=C  count=1
_DOTTED_NAME = re.compile(r"[\w-]+(?:\.[\w-]+)+")         # tftp1.sh  read.txt


def expanded_type(token: str) -> str:
    """Type of a token for the normalization

    quoted string -> base64, quoted string
    address       -> url, ip
    word          -> base64, number, variable, assignment, name with a dot, word
    operator, option and path are not expanded
    """
    kind = token_type(token)
    if kind in ("quoted string", "word") and is_base64(token):
        return "base64"
    if kind == "address":
        return "url" if _URL.search(token) else "ip"
    if kind == "word":
        if token.isdigit():                     # 777
            return "number"
        if token[0] == "$":                     # $SHELL
            return "variable"
        if _ASSIGNMENT.match(token):
            return "assignment"
        if _DOTTED_NAME.fullmatch(token):
            return "name with a dot"
    return kind


# The types that are replaced -> {type: placeholder}
PLACEHOLDERS = {"quoted string": "<STR>", "base64": "<B64>", "url": "<ADDR>", "ip": "<ADDR>"}


@lru_cache(maxsize=None) # lru_cache := remembers the results, so each distinct token is normalized only once. It is only for performance, the result is always the same for the same token.
def normalize_token(token: str) -> str:
    """Placeholder of the token, or the token itself if its type is not replaced."""
    return PLACEHOLDERS.get(expanded_type(token), token)


def normalized_tokenize(text: str) -> list[str]:
    """Tokens of a session (shell_tokenize) after the normalization."""
    return [normalize_token(token) for token in shell_tokenize(text)]


# ---- What is inside the quoted strings ----

def commands_of(tokens: list[str]) -> list[list[str]]:
    """The tokens divided into commands, without the operators

    A new command starts after every operator that is not a redirection. After a redirection
    ('>', '2>&1', '<', ...) the same command goes on, because a redirection only changes where
    the command reads or writes:
        echo "321" > /var/tmp/.var03522123   ->   [['echo', '"321"', '/var/tmp/.var03522123']]
    """
    commands = [[]]
    for token in tokens:
        if not _ONLY_OPERATOR.fullmatch(token):
            commands[-1].append(token)
        elif "<" not in token and ">" not in token:     # not a redirection: a new command starts
            commands.append([])
    return [command for command in commands if command]     # without the empty commands


def inside_quotes(string: str) -> str:
    """The text of a quoted string, without its first and its last quote."""
    if len(string) > 1 and string[-1] == string[0]:
        return string[1:-1]
    return string[1:]                                       # the string is never closed


def commands_inside(string: str) -> list[str]:
    """The first token of each command written inside a quoted string

    A string with one token only is taken as a value, also when it is the name of a command ('grep').
    """
    tokens = shell_tokenize(inside_quotes(string))
    if len(tokens) < 2:
        return []
    return [command[0] for command in commands_of(tokens)]


def quoted_strings(texts: pd.Series) -> pd.DataFrame:
    """One row for each quoted string of each session that becomes <STR> (base64 texts are not included)

    session : index of the session
    command : the command that receives the string, i.e. the first token of its command
    string  : the quoted string
    """
    sessions, commands, strings = [], [], []
    for session, text in texts.items():
        for command in commands_of(shell_tokenize(text)):
            for token in command:
                if normalize_token(token) == PLACEHOLDERS["quoted string"]:
                    sessions.append(session)
                    commands.append(command[0])
                    strings.append(token)
    return pd.DataFrame({"session": sessions, "command": commands, "string": strings})


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

