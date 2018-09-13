#!/usr/bin/env python3

# Creates a graph-based lookup table linking protein groups to proteins to peptides to PSms.
#
#
# Matthias Stahl, 2018

import sys
import sqlite3
from sqlite3 import Error
import networkx as nx
from networkx.readwrite import json_graph
import json

database_file = "target_psmlookup.sql"
file_name = "network.json"

psm_alias = "_ps__"
peptide_alias = "_pe__"
protein_alias = "_pr__"
protein_group_alias = "_pg__"

def _create_connection(database_file):
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def _fetchPSMs2Peptide(conn):
    cur = conn.cursor()
    
    query = "SELECT psms.psm_id, peptide_sequences.sequence " \
            "FROM psms " \
            "INNER JOIN peptide_sequences " \
            "ON psms.pep_id = peptide_sequences.pep_id"
    cur.execute(query)

    return([(psm_alias + row[0], peptide_alias + row[1]) for row in cur.fetchall()])
    
def _fetchPeptides2Proteins(conn):
    cur = conn.cursor()
    
    query = "SELECT peptide_sequences.sequence, protein_psm.protein_acc " \
            "FROM protein_psm " \
            "INNER JOIN psms " \
            "ON protein_psm.psm_id = psms.psm_id " \
            "INNER JOIN peptide_sequences " \
            "ON psms.pep_id = peptide_sequences.pep_id"
    cur.execute(query)
    
    return([(peptide_alias + row[0], protein_alias + row[1]) for row in cur.fetchall()])
    
def _fetchProteins2ProteinGroup(conn):
    cur = conn.cursor()
    
    query = "SELECT protein_group_content.protein_acc, protein_group_master.protein_acc " \
            "FROM protein_group_content " \
            "INNER JOIN protein_group_master " \
            "ON protein_group_content.master_id = protein_group_master.master_id"
    cur.execute(query)
    
    return([(protein_alias + row[0], protein_group_alias + row[1]) for row in cur.fetchall()])

def _addPSMAttributes(conn):
    # empty
    return()
    
def _addPeptideAttributes(conn):
    # empty
    return()

def _addProteinAttributes(conn):
    cur = conn.cursor()
    
    query = "SELECT protein_seq.protein_acc, protein_seq.sequence, prot_desc.description " \
            "FROM protein_seq " \
            "INNER JOIN prot_desc ON protein_seq.protein_acc = prot_desc.protein_acc"
    #attributes = [(protein_alias + tuple[0], {"sequence": tuple[1], "description": tuple[2]}) for tuple in cur.execute(query)]
    attributes = [(protein_alias + row[0], {"sequence": "", "description": row[2]}) for row in cur.execute(query)]
    
    return(attributes)
    
def _addProteinGroupAttributes(conn):
    cur = conn.cursor()
    
    query = "SELECT protein_group_master.protein_acc, " \
            "protein_group_content.peptide_count, protein_group_content.psm_count " \
            "FROM protein_group_master " \
            "INNER JOIN protein_group_content " \
            "ON protein_group_master.master_id = protein_group_content.master_id"
    attributes = [(protein_group_alias + row[0], {"peptideCount": row[1], "psmCount": row[2]}) for row in cur.execute(query)]
    
    return(attributes)

def buildInferenceGraph(database_file = database_file, add_psms = False, add_attributes = False):
    # generate new graph
    G = nx.Graph()
    
    # connect to database and fetch relevant linkages
    conn = _create_connection(database_file = database_file)
    
    # fetch data and gradually build graph
    if (add_psms == True):
        G.add_edges_from(_fetchPSMs2Peptide(conn))
        
    G.add_edges_from(_fetchPeptides2Proteins(conn))
    G.add_edges_from(_fetchProteins2ProteinGroup(conn))
    
    # add meta information to nodes
    if (add_attributes == True):
        G.add_nodes_from(_addPSMAttributes(conn))
        G.add_nodes_from(_addPeptideAttributes(conn))
        G.add_nodes_from(_addProteinAttributes(conn))
        G.add_nodes_from(_addProteinGroupAttributes(conn))
    
    # close database connection
    conn.close()
    
    return(G)
    
def saveGraph(G, file_name):
    data = json_graph.node_link_data(G)
    
    try:
        with open(file_name, 'w') as outfile:
            json.dump(json.dumps(data), outfile)
        return(True)
    except IOError:
        return(False)

if __name__ == "__main__":
    # look for command line arguments
    if (len(sys.argv) > 1):
        database_file = sys.argv[1]
    if (len(sys.argv) > 2):
        file_name = sys.argv[2]
    
    # build graph
    G = buildInferenceGraph(database_file, add_psms = False, add_attributes = False)
    
    if (G is None):
        print("An error occurred during graph creation!")
        exit(1)
    
    # save graph
    if (saveGraph(G, file_name)):
        print("Graph was saved to " + file_name + ".")
        exit(0)
    else:
        print("An error occurred during saving!")
        exit(1)
        