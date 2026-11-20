"""Section 1 utilities, used by notebooks/01_data.ipynb and by the later notebooks.

* load_dataset            read the Parquet file and check the mandatory columns
* split_tokenize          whitespace split (definition of "token" used in Section 1.1)
* shlex_tokenize(_checked) shell tokenizer based on shlex (Section 1.3, first version)
* regex_tokenize          rule-based shell tokenizer (Section 1.3, adopted)
* SHELL_OPERATOR_RE       the operator rules of regex_tokenize (to recognize operator tokens)
* shell_tokenize          the tokenizer chosen in Section 1.3: use this one elsewhere
* heat_map_section2       weekly share of sessions per label (Section 1.2)

Still to do in Section 1: representations (1.4) and template groups (1.5).
Suggested signatures and requirements in PLAN.md.
"""
from pathlib import Path
import re
import shlex
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
LABELS = ("Persistence", "Discovery", "Defense Evasion", "Execution", "Impact", "Other", "Harmless")

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


# ---------------------------------------------------------------------------
# Section 1.3 - Shell tokenization with shlex
# ---------------------------------------------------------------------------
# Why shlex?
#   shlex is the lexer of the Python standard library that splits text the
#   way a POSIX shell (sh/bash) would. A shell-aware split is what we need:
#   a session is a sequence of shell commands, not natural language.
#
# Configuration (every option below changes the result, see Section 1.3 in
# notebooks/01_data.ipynb):
#
#   posix=False
#       Keeps quotes and backslashes exactly as written by the attacker:
#           echo "root:pwd"   ->  ['echo', '"root:pwd"']
#           echo \x7f         ->  ['echo', '\\x7f']
#       With posix=True shlex would behave like the shell *executing* the line:
#       it removes the quotes ('"root:pwd"' -> 'root:pwd') and consumes
#       backslashes outside quotes ('\x7f' -> 'x7f'). For an analysis we want
#       the text the attacker typed, and the fact that something was quoted
#       is itself useful information, so we keep the literal form.
#
#   punctuation_chars=True
#       Shell control characters ( ; | & < > ( ) ) become separate tokens even
#       when glued to a word, and consecutive ones are grouped:
#           "x"|chpasswd      ->  ['"x"', '|', 'chpasswd']
#           a && b || c       ->  ['a', '&&', 'b', '||', 'c']
#       It also adds  ~ - . / * ? =  to the word characters, so options
#       (-la), paths (/etc/passwd, ~/.ssh) and assignments (a=b) stay whole.
#
#   whitespace_split=True
#       A token ends only at whitespace or at a punctuation character, never
#       in the middle of a word. Without it URLs, base64 blobs and IPs would
#       be cut at characters such as ':' '+' '@'.
#
#   commenters=""
#       By default shlex treats '#' as the start of a comment and silently
#       DROPS the rest of the text. In attack sessions '#' is almost never a
#       comment ($#, URLs with #fragment, "#!/bin/sh" outside quotes, ...),
#       so we disable comments and keep '#' as a normal character.
#
#   Case is never changed: the shell is case sensitive (ls -R != ls -r,
#   base64 payloads change meaning if lower-cased).
#
# Known limits of shlex (documented in the notebook):
#   * it is a lexer, not a bash parser: '2>&1' -> '2', '>&', '1' and
#     '$(' -> '$', '(' ; variables and $(...) are not expanded;
#   * it raises ValueError on unbalanced quotes ("No closing quotation").
#     This happens on a few sessions (a bot that inserts a password ending
#     with " into a double-quoted string, one corrupted session).
#     For those sessions we fall back to whitespace splitting.


def _make_shell_lexer(text: str) -> shlex.shlex:
    """Build a shlex lexer configured for attack sessions (see notes above)."""
    lexer = shlex.shlex(text, posix=False, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    return lexer


def shlex_tokenize_checked(text: str) -> tuple[list[str], bool]:
    """Tokenize one session with shlex and report whether shlex succeeded.

    Returns (tokens, parsed_ok):
      * parsed_ok=True  -> tokens come from shlex;
      * parsed_ok=False -> shlex failed (e.g. unbalanced quotes) and the
        tokens come from the fallback, a plain whitespace split.
    The flag lets the notebook count and inspect the fallback sessions.
    """
    try:
        return list(_make_shell_lexer(text)), True
    except ValueError:
        # shlex raises ValueError("No closing quotation") or
        # ValueError("No escaped character"). We do not try to "repair" the
        # text (e.g. by adding a quote): that would invent content.
        return text.split(), False


def shlex_tokenize(text: str) -> list[str]:
    """Shell-aware tokenizer (shlex + whitespace fallback). Returns tokens only."""
    return shlex_tokenize_checked(text)[0]


# ---------------------------------------------------------------------------
# Section 1.3 - Rule-based shell tokenizer (regular expression)
# ---------------------------------------------------------------------------
# Same policy as shlex (operators separate; options, paths, URLs, quoted
# strings whole; case and quotes kept; '#' is a normal character), written as
# explicit rules so that we can fix the limits of shlex seen in the notebook:
#   * multi-character shell operators stay whole:
#         2>&1  2>  >&2  &>  0<&3  3<>  $(     (shlex: '2', '>&', '1' / '$', '(')
#   * a backtick is an operator like $( , so the command inside `...` is visible:
#         x=`id`  ->  'x=', '`', 'id', '`'  (shlex: one token 'x=`id`')
#   * a word may mix unquoted and quoted parts, as in bash:
#         on-event="/tool fetch url=http://x/poll"  ->  one token
#         (shlex non-POSIX splits it at the spaces inside the quotes)
#   * it never raises an error: a quote that is never closed becomes a
#     one-character token and the text goes on, so no fallback is needed.
#
# How it works: re.findall scans the text from left to right and, at each
# position, takes the FIRST alternative of _TOKEN_RE that matches (order
# matters: operators are tried before words, longer operators before shorter
# ones). Whitespace is never part of a match, so it acts as a separator. A
# newline is therefore read like a space, while bash reads it like ';': the
# dataset contains no newline (checked in the notebook).
#
# Backslashes are kept as normal characters and are NOT treated as escapes
# (as shlex with posix=False). Some bots insert passwords ending with '\'
# inside "...": treating \" as an escaped quote would join several commands
# into one token. Consequence: where bash reads a backslash as an escape, the
# tokens can differ; e.g. outside quotes '\;' gives '\' and the operator ';',
# while bash passes a literal ';' to the command (find ... -exec rm {} \;).
# Likewise a quoted string is always one token, even when bash would run a
# command inside it ("$(id)"). Both cases are counted in the notebook: they
# are rare in this dataset, and shlex behaves the same way.
#
# Known limit: a password that contains '"' (e.g. B"r0-Scherer, written
# by a bot without escaping) leaves a quote open; the regex then pairs it
# with the quote of a later command and the text in between, including
# ' ; ', becomes one quoted token. This affects a few dozen sessions
# (measured in Section 1.3); on the same texts shlex either fails (and the
# fallback is used) or cuts the password into pieces.

_SINGLE_QUOTED = r"'[^']*'"                   # '...'  (no escapes inside, as in bash)
_DOUBLE_QUOTED = r'"[^"]*"'                   # "..."  (backslashes kept literally)
_UNQUOTED_CHAR = r"""(?:[^\s'"|;&<>`()$]|\$(?!\())"""   # any char except blanks, quotes,
                                              # operator chars; '$' only if not followed by '('
# Rules 1-7 are all the control and redirection operators of bash (bash manual,
# "Definitions" and "Redirections"), except the newline; a redirection may start
# with a file-descriptor number (2>, 0<&3). Rules 8-9 are command substitutions:
# not operators for bash, but we separate them so that the command inside is visible.
# File-descriptor numbers are written [0-9], not \d: in Python \d also matches
# non-ASCII digits (e.g. Arabic-Indic), which bash does not accept.
_SHELL_OPERATORS = [
    r"[0-9]*[<>]&[0-9]*-?",          # 1 fd duplication:  2>&1   >&2   1>&-   0<&3
    r"&>>?",                         # 2 redirect stdout+stderr:  &>  &>>
    r"[0-9]*(?:>>|>\||>)",           # 3 output redirection:  >  >>  >|  2>  2>>
    r"[0-9]*(?:<<<|<<-|<<|<>|<)",    # 4 input: <  here-doc << <<-  here-string <<<  read-write <>
    r"\|\||\|&|\|",                  # 5 OR list, pipe of stdout+stderr, pipe
    r"&&|&",                         # 6 AND list, background
    r";;&|;;|;&|;",                  # 7 case-clause terminators, command separator
    r"\$\(|\(|\)",                   # 8 command substitution start, sub-shell parentheses
    r"`",                            # 9 backtick command substitution
]
# The operator rules alone: the notebook uses SHELL_OPERATOR_RE.fullmatch(token)
# to recognize the operator tokens when it classifies the tokens by type.
SHELL_OPERATOR_RE = re.compile("|".join(_SHELL_OPERATORS))

_TOKEN_RE = re.compile("|".join(
    _SHELL_OPERATORS
    + [rf"(?:{_UNQUOTED_CHAR}|{_SINGLE_QUOTED}|{_DOUBLE_QUOTED})+"]   # 10 a word: unquoted and
                                                                       # quoted parts glued together
    + [r"\S"]            # 11 anything else (e.g. a quote never closed): one-character token
))


def regex_tokenize(text: str) -> list[str]:
    """Rule-based shell tokenizer (see the notes above). Never raises."""
    return _TOKEN_RE.findall(text)


def shell_tokenize(text: str) -> list[str]:
    """Tokenizer chosen in Section 1.3 for the following sections (1.4 onwards).

    Use this name in the other notebooks: if the group changes the choice,
    only this function has to be updated. It is a named function (not a
    lambda), so vectorizers that use it can be saved with pickle.
    """
    return regex_tokenize(text)


def heat_map_section2(labels_ts):
    # share of sessions with each label, per week 'How many sessions (upon 100) contain the lable'
    #  --> every week goes from Monday to Sunday and is labeled with Sunday
    weekly_share = labels_ts.resample("W").mean() 

    fig, ax = plt.subplots(figsize=(12, 3.5), layout="constrained")
    sns.heatmap(weekly_share.T, cmap="viridis", vmin=0, vmax=1, ax=ax,
                cbar_kws={"label": "Share of sessions"},
                xticklabels=weekly_share.index.strftime("%Y-%m-%d"))
    ax.set(xlabel="Week", ylabel="", title="Weekly share of sessions with each label")
    ax.tick_params(axis="x", labelsize=7, rotation=90)
    plt.show()
