#!/usr/bin/env python3

# Creates a graph-based lookup linking protein groups to proteins to peptides to PSms.
#
#
# Matthias Stahl, 2018

import sys
import sqlite3
from sqlite3 import Error
import json
import gzip

database_file = "target_psmlookup.sql"
file_name = "graph.json"

def _create_connection(database_file):
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def _fetchPeptides2Proteins(conn):
    cur = conn.cursor()
    query = "SELECT peptide_sequences.sequence, protein_psm.protein_acc " \
            "FROM protein_psm " \
            "INNER JOIN psms " \
            "ON protein_psm.psm_id = psms.psm_id " \
            "INNER JOIN peptide_sequences " \
            "ON psms.pep_id = peptide_sequences.pep_id"
    for row in cur.execute(query):
        yield row

def buildLookup(database_file = database_file):
    # connect to database and fetch relevant linkages
    conn = _create_connection(database_file = database_file)
    
    # fetch data and gradually build graph
    lookup = {}
    for peptide, protein in _fetchPeptides2Proteins(conn):
        if (protein in lookup.keys()):
            lookup[protein].append(peptide)
        else:
            lookup[protein] = [peptide]
    
    # close database connection
    conn.close()
    
    return(lookup)

if __name__ == "__main__":
    # look for command line arguments
    if (len(sys.argv) > 1):
        database_file = sys.argv[1]
    if (len(sys.argv) > 2):
        file_name = sys.argv[2]
    
    # build graph
    lookup = buildLookup(database_file)
    
    # save
    with open(file_name, 'w') as f:
        json.dump(lookup, f)
        
    json_str = json.dumps(lookup) + "\n"
    json_bytes = json_str.encode('utf-8')
    with gzip.GzipFile(file_name + ".gz", 'w') as f:
        f.write(json_bytes)  
        