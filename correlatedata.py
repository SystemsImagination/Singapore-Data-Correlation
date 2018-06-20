import pandas as pd
df = pd.read_excel("C:\\Users\\Groot\\Documents\\all data.xlsx", sheet = 1)
df.fillna(0, inplace=True)


def drop_x_row(df, x, column):
     df_true_false_values = df[df[column] == x]
     df = df.drop(df_true_false_values.index, axis=0)
     return df
"""
df = drop_x_row(df, 0,"family_mother_smoke_yes")
df = drop_x_row(df, 0, "family_father_smoke_yes")
df = drop_x_row(df, "No", "family_mother_smoke_yes")
df = drop_x_row(df, "No", "family_father_smoke_yes")
print(df)
arr = list(df)
"""
"""
for i in range(51,143):
	for j in range(51, 143):
		corr = df[arr[i]].corr(df[arr[j]])
		if corr >= 0.5 and arr[i] != arr[j]:
			print(arr[i] + " to " + arr[j])
			print(corr)
"""

count1 = 0
for i in range(0, len(df.axes[0])):
	arr = list(df)
	if df.ix[i, arr.index("allergic_rhinitis_any_nose_problem")] == "Yes":
		if df.ix[i, arr.index("allergic_rhinitis_itchy_eyes")] == "Yes":
			if df.ix[i, arr.index("allergic_rhinitis_itchy_nose_intermittent")] == "Yes":
				count1 = count1 + 1
print(count1)
prob_of_b_in_a = count1/(len(df.axes[0]) * 3)
print(prob_of_b_in_a)
def add_two_columns_together(df, col1, col2):
	df["sum"] = df[col1] + df[col2]
	return df

"""
def probability_of_b_including_a(df, a, b, col1, col2):
	arr = list(df)
	a_count = 0
	b_count = 0
	loc_of_col1 = arr.index(col1)
	loc_of_col2 = arr.index(col2)
	for i in range(0, len(df.index)):
		if df.ix[i, loc_of_col1] == b:
			b_count = b_count + 1
	for i in range(0, len(df.index)):
		if df.ix[i, loc_of_col2] == a:
			a_count = a_count + 1
	prob_of_b_and_a = (a_count/len(df.axes[0])) * (b_count/len(df.axes[0]))
	return prob_of_b_and_a
	print(probability_of_b_including_a(df, "Yes", "Yes", "allergic_rhinitis_nose_bleed_no", "allergic_rhinitis_nose_bleed_persistent"))
#def probability(df, col1, col2):
"""
