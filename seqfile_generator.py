import random

# vars
alphabet = "ACDEFGHIKLMNPQRSTVWY"
length = 10
outfile_name = "peptides.peprec"
sep = " "

# get random sequences
seq = list(''.join(random.choice(alphabet) for _ in range(length)))
seqs = []*length
for i in range(length):
    mod_seq = seq[:]
    mod_seq[i] = "S"
    seqs.append(''.join(mod_seq))

# compile PEPREC file
# space separated file with "spec_id modifications peptide charge"
lines = []
lines.append(sep.join(["spec_id", "modifications", "peptide", "charge"]) + "\n")
for i, peptide in enumerate(seqs):
    lines.append(sep.join([''.join(["peptide", str(i), "n"]), "-", peptide, str(2)]) + "\n")
    lines.append(sep.join([''.join(["peptide", str(i), "p"]), str(i+1) + "|PhosphoS", peptide, str(2)]) + "\n")
lines[-1] = lines[-1].replace("\n", "")

# write in file
o = open(outfile_name, mode = 'w')
o.writelines(lines)
o.close()
