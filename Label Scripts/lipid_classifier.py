# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:03:10 2018

@author: Suhas Vittal
"""

import re
import os

# This script classifies a lipid into its category.

category_dict = {0:"glycerophospholipid",1:"sphingolipid",2:"sterol",3:"glycerolipid",4:"fatty acid"}

def classify_lipid(lipid):
    # lipid is a string.
    
    # We use regex to identify the structures of lipids. The following structures
    # are capable of being recognized:
    #   glycerophospholipids (0)
    #   sphingolipids (1)
    #   sterols (2)
    #   glycerolipids (3)
    #   fatty acid (4)
    
    # If the lipid is not one of the above, then the output is -1 (NOT a LIPID).
    
    if re.match(".G", lipid):
        return 3
    elif re.match("BMP", lipid) or re.match("(.*?)P(.*?)", lipid) or re.match("P(.*?)P", lipid):
        return 0
    elif re.match("(.*?)Cer", lipid) or re.match(".1P", lipid) or re.match("SPH", lipid) or re.match("SM", lipid):
        return 1
    elif re.match("S[ET]", lipid) or re.match("FC", lipid) or re.match("C.?", lipid) or re.match(".?[DGLT]?CA", lipid):
        return 2
    elif re.match("FA", lipid):
        return 4
    else:
        return -1
    
# The main run would read a file of lipids, each on a newline, and then output a tsv,
# in the format <lipid>\t<category>.
    
if __name__ == "__main__":
    file = "important_lipids.txt"
    fname = os.path.splitext(file)[0]
    
    reader = open(file, "r")
    writer = open(fname + "-classified.tsv", "w+")
    
    lipids = reader.readlines()
    reader.close()
    
    writer.write("Lipid\tCategory")
    for lipid in lipids:
        catnum = classify_lipid(lipid)
        category = category_dict[catnum]
        writer.write("\n" + lipid.strip() + "\t" + category)
        
    writer.close()