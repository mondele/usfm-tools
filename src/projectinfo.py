# -*- coding: utf-8 -*-
# Manages project-specific information.
# Project info can be saved to a json configuration file in parent folder of project directory.
# FUTURE: Other parts of project info can be saved to a manifest.yaml file in project directory.
# The contents of the two files partially overlap.
# The config file is named according to the language code. Such as mgv.json.
# If the json file already exists, it is loaded on ProjectInfo initialization.
# Changes to the project info are held in memory until save() is called.
# FUTURE: ProjectInfo manages manifest.yaml via the manifestyaml module, only when updateManifest() is called.

import json
import os
import io

class ProjectInfo:
    def __init__(self, project_dir, language_code):
        self.project_dir = project_dir
        if os.path.exists(os.path.dirname(project_dir)):
            self.configpath = os.path.join(os.path.dirname(project_dir), language_code+".json")
            if os.path.isfile(self.configpath):
                with io.open(self.configpath, 'r') as json_file:
                    self.info = json.load(json_file)
                assert 'language' in self.info
                assert 'source_translations' in self.info
            else:
                self.info = {'language': {'id': language_code},
                            'source_translations': [] }

    def __repr__(self):
        return f'ProjectInfo({self.configpath})'

    # Saves the current information in the project json file.
    def save(self):
        self.info['source_translations'].sort(reverse=True, key=count)    # sorts in place
        with io.open(self.configpath, 'w') as json_file:
            json.dump(self.info, json_file, indent=4)

    def setLanguageName(self, name):
        self.info['language']['name'] = name
    def getLanguageCode(self):
        return self.info['language']['id']
    def getLanguageName(self):
        return self.info['language']['name'] if 'name' in self.info['language'] else None

    # Overwrites the list of source translations
    def resetSources(self):
        self.info['source_translations'] = []
    def addSource(self, language_id, resource_id, version):
        source = None
        assert 'source_translations' in self.info
        source = self.findSource(language_id, resource_id, version)
        if source:
            source['count'] = source['count'] + 1
        else:
            self.info['source_translations'].append( {'language_id': language_id,
                                                    'resource_id': resource_id,
                                                    'version': version,
                                                    'count': 1} )
    def getMainSource(self):
        mainsource = None
        if len(self.info['source_translations']) > 0:
            self.info['source_translations'].sort(reverse=True, key=count)
            mainsource = self.info['source_translations'][0]
        return mainsource

    # used by self.addSource()
    def findSource(self, language_id, resource_id, version):
        found = None
        for source in self.info['source_translations']:
            if source['language_id'] == language_id and source['resource_id'] == resource_id and\
                source['version'] == version:
                found = source
                break
        return found

def count(source):
    return source['count']
