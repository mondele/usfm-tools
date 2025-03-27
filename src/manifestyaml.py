# -*- coding: utf-8 -*-
# Manages project-specific information in manifest.yaml file.
# Changes are held in memory until save() is called.
# This class can give access to any yaml file, but the create() and setter functions
#    only work for resource container manifest.yaml files. These files are identified
#    by having a 'dublin_core' element.
# The yaml contents are exposed via the contents member.
# Note: contents a mutable object. Changes made to it affects the contents here.

import os
import io
import yaml
import codecs

class ManifestYaml:
    def __init__(self, project_dir, filename="manifest.yaml"):
        self.project_dir = project_dir
        self.path = os.path.join(project_dir, filename)
        self.contents = None

    def __repr__(self):
        return f'ManifestYaml({self.project_dir})'

    def exists(self):
        return os.path.isfile(self.path)

    # Loads the existing manifest file if it exists.
    # The content is stored internally as a dict structure.
    # Returns list of error strings if not successful.
    def load(self):
        errors = []
        if os.path.isfile(self.path):
            if has_bom(self.path):
                errors.append(f"{self.path} file has a Byte Order Mark. Remove it.")
            with io.open(self.path, "tr", encoding='utf-8-sig') as file:
                try:
                    self.contents = yaml.safe_load(file)
                except yaml.scanner.ScannerError as e:
                    errors.append(f"Yaml syntax error at or before line {e.problem_mark.line} in: {self.path}")
                except yaml.parser.ParserError as e:
                    errors.append(f"Yaml parsing error at or before line {e.problem_mark.line} in: {self.path}")
        else:
            errors.append(f"File not found: {self.path}")
        return errors

    # Creates contents dict with default values for a resource container manifest.yaml file.
    # Does not actually create the file until save() is called.
    def create(self):
        self.contents = {'dublin_core': {'conformsto': 'rc0.2', 'contributor': [],
'creator': 'Bible translation community', 'description': 'An unrestricted literal Bible',
'format': 'text/usfm', 'identifier': 'reg', 'issued': '2025-03-31',
'language': {'direction': '', 'identifier': '', 'title': ''}, 'modified': '2025-03-31',
'publisher': 'Wycliffe Associates', 'relation': [], 'rights': 'CC BY-SA 4.0', 'source': [],
'subject': 'Bible', 'title': 'Bible', 'type': 'bundle', 'version': '12'},
'checking': {'checking_entity': [], 'checking_level': '1'},
'projects': []}

    # Overwrites the current manifest.yaml file.
    def save(self):
        with io.open(self.path, "tw", encoding='utf-8', newline='\n') as file:
            yaml.safe_dump(self.contents, file, default_style="'")

    # Returns the current project information represented in manifest.
    def contents(self):
        return self.contents

    def setLanguageName(self, name):
        if self.contents and 'dublin_core' in self.contents:
            self.contents['dublin_core']['language']['title'] = name
    def setDates(self, date=None):
        if self.contents and 'dublin_core' in self.contents:
            import datetime
            if not date:
                date = datetime.datetime.today().strftime('%Y-%m-%d')
            self.contents['dublin_core']['issued'] = date
            self.contents['dublin_core']['modified'] = date

# Returns True if the file has a BOM
def has_bom(path):
    with open(path, 'rb') as f:
        raw = f.read(4)
    for bom in [codecs.BOM_UTF8, codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE, codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE]:
        if raw.startswith(bom):
            return True
    return False
