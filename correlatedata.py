import pandas as pd
df = pd.read_excel("C:\\Users\\Groot\\Documents\\all data.xlsx", sheet = 1)
df.fillna(0, inplace=True)
df.replace("NA", 0)

def drop_x_row(df, x, column):
     df_true_false_values = df[df[column] == x]
     df = df.drop(df_true_false_values.index, axis=0)
     return df
#df = drop_x_row(df, 0,"bmi")
df = drop_x_row(df, "No", "family_mother_smoke_yes")
df = drop_x_row(df, "No", "family_father_smoke_yes")
print(df["family_mother_smoke_yes"])
arr = list(df)
"""
for i in range(51,143):
	for j in range(51, 143):
		corr = df[arr[i]].corr(df[arr[j]])
		if corr >= 0.5 and arr[i] != arr[j]:
			print(arr[i] + " to " + arr[j])
			print(corr)
"""

def add_two_columns_together(df, col1, col2):
	df["sum"] = df[col1] + df[col2]
	return df