import argparse
import re
import sys

import fitz
import pandas as pd


def parse_phs_blocks(blocks):
    #import ipdb; ipdb.set_trace()
    phs = blocks[0]
    request_date_idx = [i for i, item in enumerate(blocks) if re.search("Request Date", item)]
    dar_list = []
    phs_info = phs.split(" : ")
    for i, idx in enumerate(request_date_idx):
        this_dar = {
            "accession": phs_info[0],
            "study": phs_info[1],
        }
        # Check if the previous element contains a "DAR :" string.
        # If it is a new request, there is no DAR yet and this will not be present.
        m = re.match("^DAR", blocks[idx-1])
        if m:
            this_dar["DAR"] = m.string.split(" : ")[1]
        else:
            this_dar["DAR"] = None
        # Get the request and renewal dates.
        date_blocks = blocks[idx].replace(":\n", ": ").split("\n")
        tmp = {k.strip(): v.strip() for k, v in (xx.split(":") for xx in date_blocks)}
        this_dar.update(tmp)
        # Now find the consent group.
        j = idx
        try:
            loop_end = request_date_idx[i + 1]
        except IndexError:
            loop_end = len(blocks)
        done = False
        while not done:
            m = re.match("^Abbreviation :", blocks[j])
            if m:
                this_dar["Abbreviation"] = m.string.split(" : ")[1]
                done = True
            j += 1
            if j == loop_end:
                done = True
        dar_list.append(this_dar)
    return dar_list


if __name__ == "__main__":

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
            if page_text[-2].startswith("Project Request\n") or page_text[-2].startswith("Project Renewal\n"):
                blocks = blocks + page_text[:-3]
    len(blocks)

    # Remove all rows before "Consent Group(s) Information"
    idx = blocks.index("Consent Group(s) Information")
    blocks = blocks[idx:]

    # Find all rows containing a phs
    phs_regex = r"^phs\d{6}\.v\d+?\."
    #regex = r"phs002719.v1.p1"
    phs_idx = [i for i, item in enumerate(blocks) if re.search(phs_regex, item)]

    # Create variables to store the beginning and ending indices for each phs.
    idx_start = phs_idx
    idx_end = phs_idx[1:] + [len(blocks) - 1]
    # Create a list that will store one dictionary of information for each dar.
    dars = []
    for i in range(len(idx_start)):
        # Get the blocks associated with this phs.
        phs_blocks = blocks[(idx_start[i]):idx_end[i]]
        dar_list = parse_phs_blocks(phs_blocks)
        dars = dars + dar_list

    # Convert to pandas data frame and write to tsv.
    df = pd.DataFrame(dars)
    df = df.rename(columns={
        "Abbreviation": "consent_group",
        "Request Date": "request_date",
        "Last Renewal Date": "last_renewal_date",
    })

    # Replace newlines in study with spaces.
    df.replace("\n", " ", regex=True, inplace=True)

    df.to_csv(outfile, sep="\t", index=False)
