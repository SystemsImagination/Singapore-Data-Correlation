import pandas as pd
import numpy as np
import sys

print(sys.argv)

if len(sys.argv) < 7:
	print("You didn't pass all parameters (6)")

"""
file_destination = sys.argv[1]
file_destination2 = sys.argv[2]

df4 = pd.read_excel(file_destination)
df5 = pd.read_excel(file_destination2)
df4 = pd.concat([df4, df5], axis=1, sort=False)
df4.fillna(0).replace(" ",0)
list_of_correlations = []
correlation_constants = []
def correlate_data(df):
    arr = list(df)
    for i in range(sys.argv[3],sys.argv[4]): #miRNA to transcriptonomics
        for j in range(sys.argv[5], sys.argv[6]):
            corr = df[arr[j]].corr(df[arr[i]])
            if corr >= 0.6 or corr <= -0.6:
                print(arr[i])
		print("to")
		print(arr[j])
                print(corr)
               
       
correlate_data(df4)
""" 
