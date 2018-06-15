package iomics.compiler;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** @author Suhas Vittal
 *  @version 0.1
 *  
 *  @since 13 June 2018
 *  
 *  Purpose of code is to combine different data files in the iOmics
 *  dataset.
 *  
 *  PRECONDITION:
 *  	Files are tab-delimited. This should not be an issue as most
 *  	of the iOmics data is tab-delimited. This pre-condition applies
 *  	to generated files.
 *  
 *  Given that iOmics data is tab-delimited, we will return a 
 *  tab-delimited file as well.
 * */

public class DataCompiler {
	public static void main(String[] args) {
		String outputFileName = "Lipid-Transcript";
		
		String[] fs1 = new String[] {"119Indian_274miRNAs.txt","117Chinese_274miRNAs.txt","115Malay_274miRNAs.txt"};
		String[] fs2 = new String[] {"98Chinese_21649probesets.txt","96Indian_21649probesets.txt","75Malay_21649probesets.txt"};
		// "fs" stands for file set. Both of these variables store an array of files with a common
		// data type (i.e. lipid concentrations). 
		
		// NOTE all files in the same fileset must have the same labels.
	
		Map<String, String[]> idMap1 = new HashMap<String, String[]>(); // a dict that contains a 
				// map btwn object ids and data.
		Map<String, String[]> idMap2 = new HashMap<String, String[]>();
		
		// Our goal is to populate these two hashmaps, and then compile the values in both
		// to create a new .tsv file.
		
		String[] labels1 = null;
		String[] labels2 = null;
		
		try {
			BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName + ".tsv"));

			boolean first = true;
			for (String file : fs1) {
				BufferedReader reader = new BufferedReader(new FileReader(file));
				
				String line;
				if (first) {
					first = false;
					labels1 = reader.readLine().split("\t"); // get labels for fs1 grp.
				} else {
					reader.readLine(); // skip the first line.
				}
				
				while ((line = reader.readLine()) != null) {
					String[] data = line.split("\t");
					String id = data[0];
					
					String[] temp = new String[data.length - 1]; // because we don't want the id.
					for (int i = 1; i < data.length; i++) {
						temp[i - 1] = data[i];
					}
					
					idMap1.put(id, temp);
				}
				
				reader.close();
			}
			
			first = true; // reset, cuz we have another for loop for the second fs grp.
			for (String file : fs2) {
				BufferedReader reader = new BufferedReader(new FileReader(file));
				
				String line;
				if (first) {
					first = false;
					labels2 = reader.readLine().split("\t"); 
				} else {
					reader.readLine(); // skip the first line.
				}
				
				while ((line = reader.readLine()) != null) {
					String[] data = line.split("\t");
					String id = data[0];
					
					String[] temp = new String[data.length - 1]; // because we don't want the id.
					for (int i = 1; i < data.length; i++) {
						temp[i - 1] = data[i];
					}
					
					idMap2.put(id, temp);
				}
				
				reader.close();
			}
			
			// Now we will combine the data. First we must combine the labels.
			String[] newLabels = new String[labels1.length + labels2.length - 1]; // -1 because
			// we do not want to repeat the id label.
			for (int i = 0; i < newLabels.length; i++) {
				if (i < labels1.length) {
					newLabels[i] = labels1[i];
				} else {
					int _i = i - labels1.length + 1;
					newLabels[i] = labels2[_i];
				}
			}
			
			String ln_lbls = String.join("\t", newLabels);
			
			writer.write(ln_lbls); // write the labels as the first line of the new file.
			
			Set<String> ids = intersect(idMap1.keySet(), idMap2.keySet());
			
			for (String id : ids) {
				String[] row1 = idMap1.get(id);
				String[] row2 = idMap2.get(id);
				
				String line = id + "\t" + String.join("\t", row1) + "\t" + String.join("\t", row2);
				
				writer.write("\n" + line);
			}
			
			writer.close();
			
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static <T> Set<T> intersect(Set<T> A, Set<T> B) {
		Set<T> AB = new HashSet<T>();
		
		for (T a : A) {
			for (T b : B) {
				
				if (a.equals(b)) {
					AB.add(a);
				}
			}
		}
		
		return AB;
	}
}
