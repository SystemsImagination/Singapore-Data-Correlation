# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:03:10 2018

@author: groot
"""

import re

# This script classifies a lipid into its category.

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
    elif re.match("BMP", lipid) or re.match("P(.*?)", lipid) or re.match("P(.*?)P", lipid):
        return 0
    elif re.match(".+?Cer", lipid) or re.match(".1P", lipid) or re.match("SPH", lipid) or re.match("SM", lipid):
        return 1
    elif re.match("S[ET]", lipid) or re.match("FC", lipid) or re.match("C.?", lipid) or re.match(".?[DGLT]?CA", lipid):
        return 2
    elif re.match("FA", lipid):
        return 4
    else:
        return -1
    