#!/usr/bin/env python3

# Creates a textfile suitable for mzML definition in Lehtiö's proteogenomics pipeline.
#
# in file:    each line comprises absolute path to mzML (each mzML is in a directory specifying its set)
#             file can be created by find /path/to/set_directories/ -name '*.mzML' > in_file.txt
# out file:   new file with meta information
# strip name: name of HiRIEF strip (e.g. '3-10')
#
# Matthias Stahl, 2018

import sys

if len(sys.argv) < 4:
    sys.exit("USAGE: python3 " + sys.argv[0] + " <in file> <out file> <strip name>")

infile_name = sys.argv[1]
outfile_name = sys.argv[2]
strip_name = sys.argv[3]

new_lines = []
for line in open(infile_name, mode='r'):
    if len(line) > 0:
        set_name = line.split('/')[-2]
        fraction = line.split('.')[-2][-2:]
        new_line = line[:-1] + '\t' + set_name + '\t' + strip_name + '\t' + fraction + '\n'
        new_lines.append(new_line)

o = open(outfile_name, mode='w')
o.writelines(new_lines)
o.close()
