package iomics.modifier;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CohortModifier {
	public static void isolateBinaryValues(String file) {
		// look at columns with binary values
		// check if column is binary
		// add column number to list of binary columns to see
		// add data for valid participants (participants that do not have ? or DO NOT KNOW as answer)
		
		// phenotypes start from 115
		try {
			BufferedReader reader = new BufferedReader(new FileReader(file));			
			
			Map<String, List<String>> binMap = new HashMap<String, List<String>>();
			List<String> lines = new ArrayList<String>(100);
			
			String line;
			String[] header = null;
			boolean first = true;
			while ((line=reader.readLine()) != null) {
				line = line.trim();
				
				if (line.equals("")) {
					continue;
				} else {
					String[] data = line.split(",");
					if (first) {
						header = data;
					}
					for (int i = 115; i < data.length; i++) {
						if (first) {
							binMap.put(header[i], new ArrayList<String>());
						} else {
							lines.add(line); // for l8r
							// add to binMap value if value is new.
							String value = data[i];
							String head = header[i];
							
							List<String> list = binMap.get(head);
							if (!list.contains(value) && 
									!(value.equals("?") || value.equalsIgnoreCase("do not know"))) {
								list.add(value);
								binMap.put(head, list);
							}
						}
					}
					first = false;
				}
			}
			reader.close();
			BufferedWriter writer = new BufferedWriter(new FileWriter("cohort_binary.csv"));
			String headln = "";
			for (int i = 0; i < header.length; i++) {
				if (i == 0) {
					headln = header[i];
				} else if (i >= 115) {
					// check if header has 2 values
					if (binMap.get(header[i]).size() == 2) {
						headln += "," + header[i];
					}
				} else {
					headln += "," + header[i];
				}
			}
			
			// now that the header is set up...
			writer.write(headln);
			line = "\n";
			for (String ln : lines) {
				String[] data = ln.split(",");
				first = true;
				line += String.join(",", data);
				System.out.println(line);
				if (line != null) {
					writer.write(line);
				}
			}
			
			writer.close();
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		String filename = "cohort.csv";
		isolateBinaryValues(filename);
	}
}
