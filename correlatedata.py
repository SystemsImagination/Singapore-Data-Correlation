import pandas as pd
df = pd.read_excel("C:\\Users\\Groot\\Documents\\all data.xlsx", sheet = 1)
df.fillna(0, inplace=True)


def drop_x_row(df, x, column):
     df_true_false_values = df[df[column] == x]
     df = df.drop(df_true_false_values.index, axis=0)
     return df
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
print(len(df.axes[0]))

print(count1)
prob_of_c_in_b_in_a = count1/(len(df.axes[0]) * 3)
print(prob_of_c_in_b_in_a)

def sort_row(df,col):
	new_df = df[col]
	sorted_col = new_df.sort_index(ascending=True)
	df[col] = sorted_col
	return df
df2 = sort_row(df, "[sgp130]")
print(df2)
"""
def drop_middle_25(df, col):
	df = sort_row(df, col)
	total_values = len(df.axes[0])
	lower_bound = int(total_values * 0.25)
	upper_bound = int(total_values * 0.75)
	for i in range(lower_bound, upper_bound):
		df = df.drop(i, df.ix[arr.index(col)])
	return df
df2 = drop_middle_25(df, "[sgp130]")
print(df2["[sgp130]"])
"""
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
