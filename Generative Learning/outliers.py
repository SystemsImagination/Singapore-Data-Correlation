"""
  @author Suhas Vittal

  Script isolates outliers from each time step
"""

import numpy as np

if __name__ == "__main__":
    reader = open("gan_scores.tsv", "r")
    header = reader.readline().split("\t")

    """
        Process:
            1) Calculate MAD (median absolute deviation).
            2) Find values outside of 4.5*MAD
    """

    line = reader.readline()
    time_step = 0
    outliers = []
    writer = open("outliers.tsv", "w+")
    writer.write("Time Step\tOutliers")
    while line != "":
        line = line.strip()
        row = np.asarray([float(x) for x in line.split("\t")])
        median = np.median(row)
        array = np.abs(row-median)
        MAD = np.median(array)

        # now run through the data
        bound = 5*MAD
        for i in range(len(row)):
            score = row[i]
            diff = score - median
            if np.abs(diff) >= bound:
                outliers.append(header[i])
        print("TIME " + str(time_step) + ":\t" + ", ".join(outliers))
        writer.write("\n" + str(time_step) + "\t" + "\t".join(outliers))
        time_step += 1
        outliers = []
        line = reader.readline()
    reader.close()
    writer.close()
