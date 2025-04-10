# pytest unit tests for functions in footnotes.py

import os
import sys
import pytest

tests_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(os.path.dirname(tests_path), "src")
sys.path.append(src_path)
import footnotes

dir = r'C:\DCS\EnglishTest\en_ulb.WA.v21-05'
language_code = 'en'
language_name = 'English'

@pytest.mark.parametrize('dir, expected',
    [(dir, True),
     (r'C:\DCS\EnglishTest', False),
     ('', False),
    ])
def test_validSourceDir(dir, expected):
    assert footnotes.validSourceDir(dir) == expected

@pytest.mark.parametrize('dir, expected',
    [(r'C:\DCS\EnglishTest', False),
     ('', False),
    ])
def test_preScanned(dir, expected):
    assert footnotes.preScanned(dir) == expected

@pytest.mark.parametrize('verse, expected',
    [('GEN 1:26', True),
     ('GEN 1:27', False),
     ('ROM 8:28', True),
    ])
def test_footnotedVerses(verse, expected):
    # Tests the initial, default set
    fv = footnotes.getFootnotedVerses()
    result = (verse in fv)
    assert result == expected
    assert len(fv) == 384

def test_scanFootnotes():
    dir = r'C:\DCS\EnglishTest\work'
    fvpath = os.path.join(dir, "footnotedVerses.json")
    if os.path.isfile(fvpath):
        os.remove(fvpath)
    footnotes.scanFootnotes(dir)
    assert os.path.isfile(fvpath)
    assert footnotes.preScanned(dir) == True
    fv = footnotes.getFootnotedVerses()
    assert len(fv) == 4
    assert ('DAN 9:1' in fv)
    assert ('DAN 9:3' not in fv)

def test_scanFootnotes2():
    global dir
    fvpath = os.path.join(dir, "footnotedVerses.json")
    footnotes.scanFootnotes(dir)
    assert footnotes.preScanned(dir) == True
    assert os.path.isfile(fvpath)
    fv = footnotes.getFootnotedVerses()
    assert len(fv) == 114
    assert "LEV 20:7" not in fv
    assert "MRK 16:20" in fv
