# -*- coding: utf-8 -*-
# Used by usfm_cleanup.py.
# Substitutions in this file convert straight quotes to curly quotes.
# These substitutions are applied after some regular expressions replacements have been made.

# subs is a list of tuples to be used for string substitutions.
subs = [
# Convert open quote marks
	("'“", "‘“"),
	("“'", "“‘"),
	('‘"', '‘“'),
	('"‘', '“‘'),

# Convert closing quote marks
	("'”", "’”"),
	("”'", "”’"),
	('’"', '’”'),
	('"’', '”’')
]

import re
quote0_re = re.compile(r'[^\w]([\'"]+)\w+([\'"]+)[^\w]')   # a single word in quotes
quote1_re = re.compile(r'[ \(\[][“‘]*([\'"]+)\w')     # SPACE|PAREN quotes word => open quotes
quote2_re = re.compile(r': +[“‘]*([\'"]+)[^\.!?)]')     # colon SPACE quotes ... => open quotes
quote3_re = re.compile(r'[,;][’”]*([\'"]+)[\)\]]')     # comma/semicolon quotes PAREN => close quotes
quote4_re = re.compile(r'[\.!\?][’”]*([\'"]+)')     # period/bang/question quotes => close quotes
quote5_re = re.compile(r'\w[’”]*([\'"]+) *\n')        # word quotes EOL
quote6_re = re.compile(r'\w[\w ][’”]*([\'"]+\?)')       # quotes question => close quotes question
quote8_re = re.compile(r'\n *([\'"]+)\w')   # quotes word at start of line
snglquote9_re = re.compile(r'‘[^“‘\'’”\n\\]+[^\s“‘\'’”\n\\](\')[^\w]')  # single quote at end of word if there is a matching open quote on the same line
opentrans = str.maketrans('\'"', "‘“")
closetrans = str.maketrans('\'"', '’”')

# Changes straight quotes to curly quotes where context suggests with very high confidence.
# Called by usfm_cleanup, passing in the entire usfm file as a string.
def promoteQuotes(str):
    pos = 0
    snippet = quote0_re.search(str, pos)
    while snippet:
        if snippet.group(1) == snippet.group(2) and len(snippet.group(1)) == 1:
            (i,j) = (snippet.start(1), snippet.end(2))
            str = str[0:i] + snippet.group(1).translate(opentrans) + str[i+1:j-1] + snippet.group(2).translate(closetrans) + str[j:]
        pos = snippet.end()
        snippet = quote0_re.search(str, pos)

    str = _translate(str, quote1_re, opentrans)
    str = _translate(str, quote2_re, opentrans)
    str = _translate(str, quote3_re, closetrans)
    str = _translate(str, quote4_re, closetrans)
    str = _translate(str, quote5_re, closetrans)
    str = _translate(str, quote6_re, closetrans)
    str = _translate(str, quote8_re, opentrans)
    str = _translate(str, snglquote9_re, closetrans)
    str = _translate(str, dblquote9_re, closetrans)
    for pair in subs:
        str = str.replace(pair[0], pair[1])
    return str

dblquote0_re = re.compile(r'[^\w]("+)\w+("+)[^\w]')     # a single word in quotes
dblquote1_re = re.compile(r'[ \(\[]("+)[\w‘\']')     # SPACE|PAREN " word => “
dblquote2_re = re.compile(r': +[\'‘]*("+)[^\.!?)]')     # colon SPACE " ... => “
dblquote3_re = re.compile(r'[,;][’\']*("+)[’\']*[\)\]]')     # comma/semicolon " PAREN => ”
dblquote4_re = re.compile(r'[\.!\?][’\']*("+)')     # period/bang/question " => ”
dblquote5_re = re.compile(r'\w[’\']*("+) *\n')        # word " EOL => ”
dblquote6_re = re.compile(r'\w[\w ][’”]*("+\?)')       # " question => ” question
dblquote8_re = re.compile(r'\n *("+)[\w\'‘]')   # " word at start of line => “
dblquote9_re = re.compile(r'“[^“‘\'’”\n\\]+[^\s“‘\'’”\n\\](")[^\w]')  # quote at end of word if there is a matching open quote on the same line
dblopentrans = str.maketrans('"', '“')
dblclosetrans = str.maketrans('"', '”')
# dblsubs is a list of tuples to be used for string substitutions.
dblsubs = [
# Convert open quote marks
	('"“', '““'),
	('“"', '““'),
	('‘"', '‘“'),
	('"‘', '“‘'),
    ('“\'"', '“\'“'),
    ('"\'“', '“\'“'),
# Convert closing quote marks
	('"”', "””"),
	('”"', "””"),
	('’"', '’”'),
	('"’', '”’'),
    ('”\'"', '”\'”'),
    ('"\'”', '”\'”'),
]

# Changes straight double quotes to curly quotes where context suggests with very high confidence.
def promoteDoubleQuotes(str):
    pos = 0
    snippet = dblquote0_re.search(str, pos)
    while snippet:
        if snippet.group(1) == snippet.group(2) and len(snippet.group(1)) == 1:
            (i,j) = (snippet.start(1), snippet.end(2))
            str = str[0:i] + snippet.group(1).translate(dblopentrans) + str[i+1:j-1] + snippet.group(2).translate(dblclosetrans) + str[j:]
        pos = snippet.end()
        snippet = dblquote0_re.search(str, pos)

    str = _translate(str, dblquote1_re, dblopentrans)
    str = _translate(str, dblquote2_re, dblopentrans)
    str = _translate(str, dblquote3_re, dblclosetrans)
    str = _translate(str, dblquote4_re, dblclosetrans)
    str = _translate(str, dblquote5_re, dblclosetrans)
    str = _translate(str, dblquote6_re, dblclosetrans)
    str = _translate(str, dblquote8_re, dblopentrans)
    str = _translate(str, dblquote9_re, dblclosetrans)

    for pair in dblsubs:
        str = str.replace(pair[0], pair[1])
    return str

# Internal function.
# Translates quotes in the string wherever the expression matches.
# Uses trans as the translation table.
def _translate(str, rexp, trans):
    snippet = rexp.search(str)
    while snippet:
        (i,j) = (snippet.start(1), snippet.end(1))
        str = str[0:i] + snippet.group(1).translate(trans) + str[j:]
        snippet = rexp.search(str)
    return str

# quotes_re = re.compile(r'[“‘‹«\'"’”›»]')

# # Returns the character position of the first quote in the string, or -1 if none.
# def quotepos(str):
#     quote = quotes_re.search(str)
#     return quote.start() if quote else -1

# openquote_re = re.compile(r'[^\w]*[\'"“‘‹«]+.*\w')
# closequote_re = re.compile(r'\w.*[\'"’”›»]+[^\w]*$')
# internalquote_re = re.compile(r'\w.*["“‘‹«”›»]+.*\w')

# Returns True if the string starts or ends an incomplete quotation.
# This function is used by section_titles.is_heading() to exclude
# most candidates for section titles that include quote marks.
# @TODO A *complete* internal quotation should not cause a True return value.
# def partialQuote(str):
#     starts = bool(openquote_re.match(str))
#     ends = bool(closequote_re.search(str))
#     internal = bool(internalquote_re.search(str))   # too simplistic
#     return starts ^ ends ^ internal
