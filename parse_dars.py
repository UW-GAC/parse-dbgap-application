import argparse
import re
import sys

import fitz
import pandas as pd


parser = argparse.ArgumentParser(
    prog='parse_dars',
    description='Parse DARs from a dbGaP application PDF and write them to a tsv.',
)
parser.add_argument("infile", help="PDF of dbGaP application to parse")
parser.add_argument("outfile", help="Output tsv file to write")

args = parser.parse_args()
pdf_file = args.infile
outfile = args.outfile

# Read in all the text in the pdf.
blocks = []
with fitz.open(pdf_file) as doc:
    for page in doc:
        page_text = [x[4].strip() for x in page.get_text("blocks")]
        # Only keep the page if it has the "Project Request" header.
        if page_text[-2].startswith("Project Request\n"):
            blocks = blocks + page_text[:-3]
len(blocks)

# Remove all rows before "Consent Group(s) Information"
idx = blocks.index("Consent Group(s) Information")
blocks = blocks[idx:]

# Find all rows containing a phs
phs_regex = r"^phs\d{6}\.v\d+?\."
#regex = r"phs002719.v1.p1"
phs_idx = [i for i, item in enumerate(blocks) if re.search(phs_regex, item)]

# ... now loop over everything and extract!
n_per_dar = 2 # Number of lines expected per dar

# Create variables to store the beginning and ending indices for each phs.
idx_start = phs_idx
idx_end = phs_idx[1:] + [len(blocks) - 1]
# Create a list that will store one dictionary of information for each dar.
dars = []
for i in range(len(idx_start)):
    # We only want to retain rows that have the DAR or the consent group abbreviation.
    dar_regex = r"(DAR|Abbreviation) :"
    phs = blocks[idx_start[i]]
    phs_blocks = blocks[(idx_start[i]):idx_end[i]]
    # Now search for all the occurrences of "DAR"
    dar_info = [item for j, item in enumerate(phs_blocks) if re.search(dar_regex, item)]
    assert len(dar_info) % n_per_dar == 0
    # Convert each chunk of dar_info to a dictionary
    these_dars = []
    for k in range(len(dar_info) // n_per_dar):
        phs_info = phs.split(" : ")
        this_dar = dar_info[(n_per_dar * k):(n_per_dar * k + n_per_dar)]
        dar_dict = {
            "accession": phs_info[0],
            "study": phs_info[1],
        }
        dar_dict.update(dict([x.split(" : ") for x in this_dar]))
        dars.append(dar_dict) 

# Convert to pandas data frame and write to tsv.
df = pd.DataFrame(dars)
df = df.rename(columns={
    "Abbreviation": "consent_group"
})

df.to_csv(outfile, sep="\t", index=False)