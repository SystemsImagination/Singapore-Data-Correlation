import pandas as pd
df = pd.read_excel("C:\\Users\\Groot\\Documents\\all data.xlsx", sheet = 1)

df.fillna(0, inplace=True)


def drop_x_row(df, x, column):
     df_true_false_values = df[df[column] == x]
     df = df.drop(df_true_false_values.index, axis=0)
     return df

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

list1 = sort_column(df, "[IL-23]")
list2 = sort_column(df, "[EGF]")


def drop_middle_25(arr):
	upper_bound = int(0.75*len(arr) - 1)
	lower_bound = int(0.25*len(arr) - 1)
	arr1 = []
	for i in range(lower_bound, upper_bound):
		arr1.append(arr[i])
	return arr1
list1 = drop_middle_25(list1)
list2 = drop_middle_25(list2)
df1 = df
df3 = df
for i in range(0, len(list2)):
	df3 = drop_x_row(df3, list2[i], "[EGF]")
for i in range(0, len(list1)):
	df1 = drop_x_row(df1, list1[i], "[IL-23]")


df1.sort_values(["[IL-23]"], ascending = True, inplace = True)
df3.sort_values(["[EGF]"], ascending = True, inplace = True)

print(df1["[IL-23]"])
print(df3["[EGF]"])
indeces1 = list(df1.index.values)
indeces2 = list(df3.index.values)
value_index = []
for i in range(0, len(indeces2)):
	for j in range(0, len(indeces1)):
		if indeces2[i] == indeces1[j]:
			value_index.append(indeces2[i])
print(value_index)



for i in range(int(len(value_index)/2), int(len(value_index))):
	arr = list(df)
	if df.ix[value_index[i], arr.index("allergic_rhinitis_any_nose_problem")] == "Yes":
		if df.ix[value_index[i], arr.index("allergic_rhinitis_itchy_eyes")] == "Yes":
			if df.ix[value_index[i], arr.index("allergic_rhinitis_nose_troublesome_symptoms")] == "Yes":
				count1 = count1 + 1
print(count1/(len(value_index) * 3))

 
