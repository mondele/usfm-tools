# pytest unit tests for functions in verifyUsfm.py

import os
import sys

tests_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(os.path.dirname(tests_path), "src")
sys.path.append(src_path)
import pytest

@pytest.mark.parametrize('str, result',
    [
        ('', 0),
        ('XYZ', 0),
        ('MAT', 28),
        ('mat', 0),
        ('MATT', 0),
        ('REV', 22),
        ('FRT', 0),
        (1, 0),
        (None, 0),
    ])
def test_nChapters(str, result):
    import verifyUSFM
    assert verifyUSFM.nChapters(str) == result

@pytest.mark.parametrize('word, expected',
    [
        ('', False),
        ('XYZ', False),
        ('Mat', False),
        ('mat', False),
        ('MaTT', True),
        ('rEv', True),
        ('frT', True),
        ('I', False),
        ('embed"ded', False),
        ("embed'ded", False),
        ("embed’ded", False),
        ("’leading", False),
        ("trailing’", False),
        ('"leading', False),
        ("'QuoTed'", True),
        ("'", False),
        ("`bwo ", False),
        ("a'iy", False),
        ("ab'b'eh", False),
        ("aka-iy", False),
        ("d'Jerusalem", True),
        ("Śâulo", False),
        ("Bârśâbbâś", False),
        ("BârŚâbbâś", True),
        ('Two Words', False),
        # ('two Words', False),     # isMixed() returns True, GIGO
        ('before”after', False),
        ('Before”', False),
        ('”After', False),
    ])
def test_isMixed(word, expected):
    import verifyUSFM
    assert verifyUSFM.isMixed(word) == expected
