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

print(len(df.axes[0]))



def column_to_list(df, col):
	array = list(df)
	arr = []
	for i in range(0, len(df.axes[0])):
		arr.append(df.ix[i, col])
	return arr
def sort_column(df,col): #bubble sort algorithm
	bad_list = column_to_list(df, col) 
	length = len(bad_list) - 1
	sorted = False
	while not sorted:
		sorted = True
		for i in range(length):
			if bad_list[i] > bad_list[i+1]:
				sorted = False
				bad_list[i], bad_list[i+1] = bad_list[i+1], bad_list[i]
	return bad_list

df2 = sort_column(df, "[sgp130]")


def drop_middle_25(arr):
	upper_bound = int(0.75*len(arr) - 1)
	lower_bound = int(0.25*len(arr) - 1)
	arr1 = []
	for i in range(lower_bound, upper_bound):
		arr1.append(arr[i])
	return arr1
df2 = drop_middle_25(df2)

for i in range(0, len(df2)):
	df = drop_x_row(df, df2[i], "[sgp130]")


df.sort_values(["[sgp130]"], ascending = True, inplace = True)

print(df["[sgp130]"])
indeces = list(df.index.values)


for i in range(0, int((len(df.axes[0]))/2)):
	arr = list(df)
	if df.ix[indeces[i], arr.index("allergic_rhinitis_any_nose_problem")] == "Yes":
		if df.ix[indeces[i], arr.index("allergic_rhinitis_itchy_eyes")] == "Yes":
			if df.ix[indeces[i], arr.index("allergic_rhinitis_itchy_nose_intermittent")] == "Yes":
				count1 = count1 + 1
print(count1/(len(df.axes[0]) * 3))

"""
def add_two_columns_together(df, col1, col2):
	df["sum"] = df[col1] + df[col2]
	return df

"""
"""
def probability_of_b_including_a(df, a, b, col1, col2):
	arr = list(df)
	a_count = 0
	loc_of_col1 = arr.index(col1)
	loc_of_col2 = arr.index(col2)	b_count = 0

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
