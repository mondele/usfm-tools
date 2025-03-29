# pytest unit tests for functions in projectinfo.py

import os
import sys
import pytest

tests_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(os.path.dirname(tests_path), "src")
sys.path.append(src_path)
from projectinfo import ProjectInfo

dir = r'C:\DCS\Matengo\work'
language_code = 'mgv'
language_name = 'Matengo'

def test_init_newfile():
    # This test function backs up the existing .json file before deleting it.
    path = os.path.join(dir, language_code+'.json')
    bakpath = path + ".bak"
    if os.path.exists(path):
        if not os.path.exists(bakpath):
            os.rename(path, bakpath)
        else:
            os.remove(path)
    projectInfo = ProjectInfo(dir, language_code)
    projectInfo.useManifest()
    assert projectInfo.getLanguageCode() == language_code
    projectInfo.save()
    assert projectInfo.getLanguageCode() == language_code

def test_init_badid():
    newcode = 'xyz'
    projectInfo = ProjectInfo(dir, newcode)
    assert projectInfo.getLanguageCode() == newcode

def test_init_noid():
    newcode = ''
    projectInfo = ProjectInfo(dir, newcode)
    assert projectInfo.getLanguageCode() == newcode
    projectInfo.save()
    projectInfo = ProjectInfo(dir, newcode)
    assert projectInfo.getLanguageCode() == newcode

def test_init_oldfile():
    projectInfo = ProjectInfo(dir, language_code)
    assert projectInfo.getLanguageCode() == language_code
    projectInfo = ProjectInfo(dir, '')
    assert projectInfo.getLanguageCode() == ''

def test_language_name():
    projectInfo = ProjectInfo(dir, language_code)
    projectInfo.setLanguage(language_name, 'rtl')
    projectInfo.save()
    assert projectInfo.getLanguageName() == language_name

@pytest.mark.parametrize('lang, rsrc, ver',
    [
        ('en', 'ulb', '1'),
        ('en', 'ulb', '1'),
        ('en', 'ulb', '2'),
    ])
def test_addsource(lang, rsrc, ver):
    badrsrc = rsrc + 'X'
    projectInfo = ProjectInfo(dir, language_code)
    projectInfo.save()
    # sources = projectInfo.getSources()
    # assert findSource(sources, lang, badrsrc, ver) == None
    orig_source = projectInfo.findSource(lang, rsrc, ver)
    orig_count = orig_source['count'] if orig_source else 0
    projectInfo.addSource(lang, rsrc, ver)
    # sources = projectInfo.getSources()
    modified_source = projectInfo.findSource(lang, rsrc, ver)
    assert modified_source['language_id'] == lang
    assert modified_source['resource_id'] == rsrc
    assert modified_source['version'] == ver
    assert modified_source['count'] == orig_count + 1
    projectInfo.save()
    modified_source = projectInfo.findSource(lang, rsrc, ver)
    assert modified_source['language_id'] == lang
    assert modified_source['resource_id'] == rsrc
    assert modified_source['version'] == ver
    assert modified_source['count'] == orig_count + 1
    projectInfo.addSource(lang, badrsrc, ver)
    # sources = projectInfo.getSources()
    modified_source = projectInfo.findSource(lang, rsrc, ver)
    assert modified_source != None
    assert modified_source['language_id'] == lang
    assert modified_source['resource_id'] == rsrc
    assert modified_source['version'] == ver
    assert modified_source['count'] == orig_count + 1
    other_source = projectInfo.findSource(lang, badrsrc, ver)
    assert other_source['language_id'] == lang
    assert other_source['resource_id'] == badrsrc
    assert other_source['version'] == ver
    assert other_source['count'] == 1

# Before running this test, sort the sources_translations in mgv.json randomly,
# and make version 7.6 the version with the highest count.
def test_getMainSource():
    projectInfo = ProjectInfo(dir, language_code)
    source = projectInfo.getMainSource()
    assert source['version'] == "7.6"
