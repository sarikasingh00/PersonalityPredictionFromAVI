import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

metrics = pd.read_csv('metrics.csv')
metrics.set_index('Trait', inplace=True)
# print(metrics)


traits = ['O', 'C', 'E', 'A', 'N']
Y = ['Image','Audio']
Z = ['False', 'True']

metrics_dict = {}
for y in Y:
	metrics_dict[y] = {}
	for z in Z:
		metrics_dict[y][z] = {}
		for trait in traits:
				metrics_dict[y][z][trait]= metrics.loc[trait, str(y)+' ' + z]

print(metrics_dict)

sns.set()
for y in metrics_dict.keys():
	count= 0
	fig, axes = plt.subplots(nrows=1, ncols=1)
	# fig.suptitle("Audio Metrics for Y = "+str(y))
	# for z in metrics_dict[y].keys():
		# print(y,z,metrics_dict[y][z])
	df = pd.DataFrame(index=['Debiased Model', 'Traditional (Biased) Model'], columns=traits)
	df.loc['Debiased Model', :] = metrics_dict[y]['False']
	df.loc['Traditional (Biased) Model',:] = metrics_dict[y]['True']
	print(df)
		# df_T = df.transpose()
		# df_T = df_T.iloc[::-1]
	df.plot.barh()
	plt.show()
	# a = df.plot.barh(ax=axes[count], color = ['r','g'], legend=False)
	# axes[count].axvline(x=1)
	# 	# if z=='E':
	# 	# 	axes[count].set_title('Ethnicity')
	# 	# else:
	# 	# 	axes[count].set_title('Gender')
	# count+=1
	# for container in a.containers:
	# 		# print(container)
	# 	a.bar_label(container, fmt='%.2f')

	
	# lines = []
	# labels = []
	  
	# for ax in fig.axes:
	#     Line, Label = ax.get_legend_handles_labels()
	#     lines.extend(Line)
	#     labels.extend(Label)
	  

	# fig.legend(lines[0:3], labels[0:3], loc='upper right')
	# plt.show()
