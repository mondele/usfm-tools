# pytest unit tests for functions in projectinfo.py

import os
import sys
import pytest

tests_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(os.path.dirname(tests_path), "src")
sys.path.append(src_path)
from manifestyaml import ManifestYaml

dir = r'C:\DCS\Bangwinji\work'
language_code = 'bsj'
language_name = 'Bangwinji'

def test_loadsave():
    manifest1 = ManifestYaml(dir)
    assert manifest1.load() == []
    assert manifest1.contents['checking']['checking_level'] == '1'
    manifest1.save()
    manifest2 = ManifestYaml(dir)
    assert manifest2.load() == []
    assert manifest1.contents == manifest2.contents

def test_dates():
    manifest = ManifestYaml(dir, filename="test.yaml")
    manifest.create()
    manifest.save()
    manifest2 = ManifestYaml(dir, filename="test.yaml")
    manifest2.load()
    assert manifest2.contents['dublin_core']['issued'] == "2025-03-31"
    manifest.setDates()
    manifest.save()
    manifest2.load()
    from datetime import datetime
    assert manifest2.contents['dublin_core']['issued'] == datetime.today().strftime('%Y-%m-%d')

def test_quotes():
    manifest = ManifestYaml(dir, filename="test.yaml")
    manifest.load()
    manifest.setLanguageName("Bang'winji")
    manifest.save()
    manifest2 = ManifestYaml(dir, filename="test.yaml")
    manifest2.load()
    assert manifest2.contents['dublin_core']['language']['title'] == "Bang'winji"
