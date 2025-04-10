# -*- coding: utf-8 -*-
# This script goes through USFM files, generating a list of verses that contain properly marked footnotes.
# Saves the list in the source_dir folder in a file named footnotedVerses.json.

# Global variables
source_dir = r'C:\DCS\English\en_ulb.lversaw'

import sys
import footnotes

if footnotes.validSourceDir(source_dir):
    footnotes.scanFootnotes(source_dir)
else:
    sys.stderr.write(f"Invalid source folder: {source_dir}\n")
