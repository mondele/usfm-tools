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
import operator
from manifestyaml import ManifestYaml

class ProjectInfo:
    def __init__(self, project_dir, language_code):
        self.project_dir = project_dir      # will need self.project_dir for manifest support
        # self.confirmed = False
        self.info = self.configpath = None
        self.manifest = None
        if os.path.exists( os.path.dirname(project_dir) ):
            self.configpath = os.path.join(os.path.dirname(project_dir), language_code+".json")
            if os.path.isfile(self.configpath):
                with io.open(self.configpath, 'r') as json_file:
                    self.info = json.load(json_file)
                assert 'source_translations' in self.info
                # self.confirmed = ('language' in self.info and language_code != "")
        if not self.info:
            self.info = {'language': {'id': language_code},
                        'source_translations': [] }

    def __repr__(self):
        return f'ProjectInfo({self.configpath})'

    # Loads the manifest file, if any.
    # Does not report any load errors, but creates a template yaml in that case.
    # Sets the language code in the manifest.
    # Controls whether the manifest is updated by subsequent calls.
    def useManifest(self, use=True):
        if use:
            self.manifest = ManifestYaml()
            errors = self.manifest.load(self.project_dir)
            if len(errors) > 0:
                self.manifest.create(self.project_dir)
        else:
            self.manifest = None

    # Saves the current information in the project json file.
    # Implicitly saves the manifest file also, if it is in use.
    def save(self):
        self.info['source_translations'].sort(reverse=True, key=operator.itemgetter('count'))    # sorts in place
        with io.open(self.configpath, 'w') as json_file:
            json.dump(self.info, json_file, indent=4)
            # self.confirmed = (self.info['language']['id'] != "")
        if self.manifest:
            if mainsource := self.getMainSource():
                self.manifest.setVersion(mainsource['version'])
            self.manifest.setDates()
            self.manifest.save()

    def setLanguage(self, name, direction):
        self.info['language']['name'] = name
        if self.manifest:
            self.manifest.setLanguage(self.info['language']['id'], name, direction)
    def getLanguageCode(self):
        return self.info['language']['id']
    def getLanguageName(self):
        return self.info['language']['name'] if 'name' in self.info['language'] else None

    # Overwrites the list of source translations
    def resetSources(self):
        self.info['source_translations'].clear()
        if self.manifest:
            self.manifest.resetSources()
            self.manifest.setVersion("")
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
        if self.manifest:
            self.manifest.addSource(language_id, resource_id, version)

    # This function is temporary, until the manifest.yaml is implemented
    def getSources(self):
        return self.info['source_translations']
    def getMainSource(self):
        mainsource = None
        if len(self.info['source_translations']) > 0:
            self.info['source_translations'].sort(reverse=True, key=operator.itemgetter('count'))
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

    def setResourceType(self, id):
        if self.manifest:
            self.manifest.setResourceType(id)

    def addContributors(self, contributors):
        if self.manifest:
            for contributor in contributors:
                self.manifest.addContributor(contributor)

    def addProject(self, project):
        if self.manifest:
            self.manifest.addProject(project)
