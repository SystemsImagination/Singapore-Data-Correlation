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

list1 = sort_column(df, "[sIL-2Ra]")
list2 = sort_column(df, "[GM-CSF]")


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
	df3 = drop_x_row(df3, list2[i], "[GM-CSF]")
for i in range(0, len(list1)):
	df1 = drop_x_row(df1, list1[i], "[sIL-2Ra]")


df1.sort_values(["[sIL-2Ra]"], ascending = True, inplace = True)
df3.sort_values(["[GM-CSF]"], ascending = True, inplace = True)

print(df1["[sIL-2Ra]"])
print(df3["[GM-CSF]"])
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
	if df.ix[value_index[i], arr.index("mother_asthma")] == "Yes": #a
		if df.ix[value_index[i], arr.index("father_asthma")] == "Yes": #b
			if df.ix[value_index[i], arr.index("asthma_diagnosed")] == "Yes": #c
				count1 = count1 + 1
print((count1/(len(value_index) * 3))*100)




 
