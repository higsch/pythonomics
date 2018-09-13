#!/usr/bin/env python3

# Creates a graph-based lookup table linking protein groups to proteins to peptides to PSms.
#
#
# Matthias Stahl, 2018

import sys
import sqlite3
from sqlite3 import Error
import networkx as nx

default_database_file = "target_psmlookup.sql"

def _create_connection(database_file):
    """ creates a database connection to the SQLite database
        specified by the db_file
    :param database_file: database file
    :return: connection object or None
    """
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def buildInferenceNetwork(database_file = default_database_file):
    """ builds the JSON lookup and handles database connection
    :param database_file: database file
    :return: bool if built was successful
    """
    
    # generate new graph
    G = nx.Graph()
    
    # connect to database and fetch relevant linkages
    conn = _create_connection(database_file = database_file)
    cur = conn.cursor()
    
    # first go for the psm to peptide linkage
    query = "SELECT psms.psm_id, peptide_sequences.sequence " \
            "FROM psms " \
            "INNER JOIN peptide_sequences " \
            "ON psms.pep_id = peptide_sequences.pep_id"
    cur.execute(query)
    psms_to_peptide = cur.fetchall()
    
    # next go for the peptides to proteins association
    query = "SELECT peptide_sequences.sequence, protein_psm.protein_acc " \
            "FROM protein_psm " \
            "INNER JOIN psms " \
            "ON protein_psm.psm_id = psms.psm_id " \
            "INNER JOIN peptide_sequences " \
            "ON psms.pep_id = peptide_sequences.pep_id"
    cur.execute(query)
    peptides_to_proteins = cur.fetchall()
    
    # finally the protein to proteon group linkage
    query = "SELECT protein_group_content.protein_acc, protein_group_master.protein_acc " \
            "FROM protein_group_content " \
            "INNER JOIN protein_group_master " \
            "ON protein_group_content.master_id = protein_group_master.master_id"
    cur.execute(query)
    proteins_to_protein_group = cur.fetchall()
    
    conn.close()
    return(True)

if __name__ == "__main__":
    # look for command line arguments
    if (len(sys.argv) > 1):
        database_file = sys.argv[1]
    else:
        print("No database file given. Will use " + default_database_file + " file.")
        database_file = default_database_file
    
    # build network
    if (buildInferenceNetwork(database_file)):
        print("JSON lookup was successfully built.")
    else:
        print("An error occurred during JSON lookup construction.")
        