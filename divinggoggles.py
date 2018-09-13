#!/usr/bin/env python3

# Creates a JSON based lookup table linking protein groups to proteins to peptides to PSms.
#
#
# Matthias Stahl, 2018

import sys

default_database_file = "target_psmlookup.sqlite"

def buildJSONLookup(database_file):
    return(True)

if __name__ == "__main__":
    # look for command line arguments
    if (len(sys.argv) > 1):
        database_file = sys.argv[1]
    else:
        print("No database file given. Will use " + default_database_file + " file.")
        database_file = default_database_file
    
    # build JSON lookup
    if (buildJSONLookup(database_file)):
        print("JSON lookup was successfully built.")
    else:
        print("An error occurred during JSON lookup construction.")
        