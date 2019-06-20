package iomics.compiler;

/**
 * @author Suhas Vittal
 * 
 * Script to compile data from all trials in Generative Learning Test.
 * 
 * */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;

public class OutlierCompiler {
	public static void main(String[] args) {
		String folderName = "Better Trials";
		
		File folder = new File(folderName);
		File[] trials = folder.listFiles();
		
		List<String> outliers = new ArrayList<String>();
		// We want to compute the union of the outliers in all trials.
		
		for (File t : trials) {
			// It just so happens that each trial is a folder.
			String outlierFileName = t.getAbsolutePath() + "/outliers.tsv";
			System.out.println(outlierFileName);
			try {
				BufferedReader reader = new BufferedReader(
						new FileReader(outlierFileName));
				String line;
				reader.readLine(); // skip header
				
				while ((line = reader.readLine()) != null) {
					String[] data = line.trim().split("\t");
					System.out.println(outliers.isEmpty());
					if (outliers.isEmpty()) {
						// Then just append it to the list
						for (int i = 1; i < data.length; i++) {
							outliers.add(data[i]);
						}
					} else {
						// create new list, then check after if each element in the
						// new list was in old. If so, keep it.
						List<String> tempList = 
								new ArrayList<String>(outliers.size());
						for (String d : data) {
							if (outliers.contains(d)) {
								tempList.add(d);
							}
						}
						
						outliers = tempList;
					}
				}
				
				reader.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		
		try {
			// now create writer
			BufferedWriter writer = new BufferedWriter(
					new FileWriter(folderName + ".tsv"));
			
			
			for (int i = 0; i < outliers.size(); i++) {
				if (i == 0) {
					writer.write(outliers.get(i));
				} else {
					writer.write("\n" + outliers.get(i));
				}
			}
			
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
