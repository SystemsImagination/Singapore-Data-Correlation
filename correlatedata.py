import pandas as pd
df = pd.read_excel("C:\\Users\\Groot\\Documents\\all data.xlsx", sheet = 1)

df.fillna(0, inplace=True)


def drop_x_row(df, x, column):
     df_true_false_values = df[df[column] == x]
     df = df.drop(df_true_false_values.index, axis=0)
     return df
def drop_row_by_index(df, row_index):
	arr = list(df)
	df = df.drop(row_index, axis = 0)
	return df
count1 = 0
count2 = 0
count3 = 0
count4 = 0

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

list1 = sort_column(df, "[MIP-1b]")
list2 = sort_column(df, "[MIP-1a]")
#print(len(list1))
#print(len(list2))

def drop_middle_25(arr):
	upper_bound = int(0.75*len(arr) - 1)
	lower_bound = int(0.25*len(arr) - 1)
	arr1 = []
	for i in range(lower_bound, upper_bound):
		arr1.append(arr[i])
	return arr1
list1 = drop_middle_25(list1)
list2 = drop_middle_25(list2)
middle_indeces1 = []
middle_indeces2 = []
df1 = df
df3 = df
arr2 = list(df)
indeces = list(df.index.values)
for i in range(0, int(len(df.axes[0])/2)):
	for j in range(0, len(list1)):
		if df.ix[indeces[i], arr2.index("[MIP-1b]")] == list1[j]:
			middle_indeces1.append(indeces[i])
for i in range(0, int(len(df.axes[0])/2)):
	for j in range(0, len(list2)):
		if df.ix[indeces[i], arr2.index("[MIP-1a]")] == list2[j]:
			middle_indeces2.append(indeces[i])
duplicates1 = []
duplicates2 = []
for i in range(0,len(middle_indeces1) - 1):
	if middle_indeces1[i] == middle_indeces1[i + 1]:
		duplicates1.append(middle_indeces1[i])
for item in duplicates1:
	middle_indeces1.remove(item)
for i in range(0,len(middle_indeces2) - 1):
	if middle_indeces2[i] == middle_indeces2[i + 1]:
		duplicates2.append(middle_indeces2[i])
for item in duplicates2:
	middle_indeces2.remove(item)
#print(middle_indeces1)
#print(middle_indeces2)

df1 = df
df3 = df
for item in middle_indeces2:
	df3 = drop_row_by_index(df3, item)
print(df3["[MIP-1a]"])
for item in middle_indeces1:
	df1 = drop_row_by_index(df1, item)
print(df1["[MIP-1b]"])



df1.sort_values(["[MIP-1a]"], ascending = True, inplace = True)
df3.sort_values(["[MIP-1b]"], ascending = True, inplace = True)

print(df1["[MIP-1a]"])
print(df3["[MIP-1b]"])
indeces1 = list(df1.index.values)
indeces2 = list(df3.index.values)

value_index = []
for i in range(0, len(indeces2)):
	for j in range(0, len(indeces1)):
		if indeces2[i] == indeces1[j]:
			value_index.append(indeces2[i])

for i in range(0, len(value_index)):
	arr = list(df)

"""
for i in range(int(len(value_index)/2), int(len(value_index))):
	arr = list(df)
	if df.ix[value_index[i], arr.index("mother_asthma")] == "Yes": #a
		if df.ix[value_index[i], arr.index("father_asthma")] == "Yes": #b
			count1 = count1 + 1
percentage_a_b = (count1/len(indeces1))*100
print("A to B")

print(percentage_a_b)

for i in range(int(len(value_index)/2), int(len(value_index))):
	if df.ix[value_index[i], arr.index("asthma_diagnosed")] == "Yes": #c
		if df.ix[value_index[i], arr.index("mother_asthma")] == "Yes": #a
			count2 = count2 + 1
percentage_a_c = (count2/len(value_index))*100
print("A to C")
print(percentage_a_c)

for i in range(int(len(value_index)/2), int(len(value_index))):
	arr = list(df)
	if df.ix[value_index[i], arr.index("asthma_diagnosed")] == "Yes": #c
		if df.ix[value_index[i], arr.index("father_asthma")] == "Yes": #b
			count3 = count3 + 1
percentage_b_c = (count3/len(value_index))*100
print("B to C")
print(percentage_b_c)
"""
for i in range(int(len(value_index)/2), ):
	if df.ix[value_index[i], arr.index("diet_burgers_fast_food")] == "Most or all days": #a
		if df.ix[value_index[i], arr.index("allergic_rhinitis_snore_no")] == "Yes": #b
			if df.ix[value_index[i], arr.index("asthma_after_exercise")] == "Yes": #c
				if df.ix[value_index[i], arr.index("asthma_limit_speech")] == "Yes":
					count4 = count4 + 1

percentage_a_b_c_d = (count4/(len(value_index))* 100)
print("A to B to C to D")
print(percentage_a_b_c_d)
#4 way probability




 
