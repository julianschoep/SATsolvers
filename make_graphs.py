import numpy as np
import matplotlib
import os
import simplejson as json
from simplejson.compat import StringIO
from collections import defaultdict
from scipy.interpolate import spline




def get_index_by_num_conflicts(dataset):
	d= defaultdict(list)
	i = 0
	for element in dataset:
		d[element].append(i)
		i+=1
	return d

def parse_str_to_list(input):
	io = StringIO(input)
	r = []
	for element in json.load(io):
		if type(element) == str:
			element = element.strip()
		r.append(float(element))
	return r

def parse_results(file):
	size = file.name.split('_')[1]
	if len(file.name.split('a')[1])>5:
		filename = size+'_CB'
	else:
		filename = size+'_2WL'
	file.readline() #conflict literals
	conf_lit = parse_str_to_list(file.readline())
	file.readline() #num conflicts
	num_conflicts = parse_str_to_list(file.readline())
	file.readline() #CPU time 
	CPU = parse_str_to_list(file.readline())
	file.readline() #parse time
	parse = parse_str_to_list(file.readline())
	file.readline() # bin ratio
	bin_rat = parse_str_to_list(file.readline())
	file.readline() # num clauses
	num_clauses = parse_str_to_list(file.readline())
	file.close()
	r = result(conf_lit,num_conflicts,CPU,parse,bin_rat,num_clauses,filename)
	return r

def get_num_conflicts_thing(dataset):
	d = get_index_by_num_conflicts(dataset.conflicts)
	x = []
	y = []
	for num_conflict in d:
		x.append(num_conflict)
		y.append(len(d[num_conflict]))
	return x,y


class result:
	conflict_literals=[]
	conflicts = []
	CPU_time = []#Sec
	parse_time = [] #sec
	bin_ratio = []
	num_clauses = []
	name = ''
	def __init__(self, conflict_literals,conflicts,CPU_time,parse_time,bin_ratio,num_clauses,name):
		self.conflict_literals=conflict_literals
		self.conflicts = conflicts
		self.CPU_time = CPU_time
		self.parse_time =parse_time
		self.bin_ratio = bin_ratio
		self.num_clauses = num_clauses
		self.name = name


no_watched_file_pre = open("OUTPUT_s4_adis-2LW.txt",'r')
watched_file_pre = open("OUTPUT_s4_a.txt",'r')



nwp4 = parse_results(open("OUTPUT_s4_adis-2LW.txt",'r'))
wp4 = parse_results(open("OUTPUT_s4_a.txt",'r'))
nwp5 = parse_results(open("OUTPUT_s5_adis-2LW.txt",'r'))
wp5 = parse_results(open("OUTPUT_s5_a.txt",'r'))
nwp6 = parse_results(open("OUTPUT_s6_adis-2LW.txt",'r'))
wp6 = parse_results(open("OUTPUT_s6_a.txt",'r'))

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#########################FIG 8 #######################
#size 6 had 10, size 5 and 4 had 100
def get_std_per_puzzle(dataset, step):
	puzzle_stds = []
	puzzle_means = []
	#print(dataset.name)
	#print(len(dataset.CPU_time))
	for i in range(0,len(dataset.CPU_time),step):
		puzzle_results = []
		for j in range(step):
			#print(i+j)
			puzzle_results.append(dataset.CPU_time[i+j])
		puzzle_stds.append(np.std(puzzle_results))
		puzzle_means.append(np.mean(puzzle_results))
	return puzzle_stds, puzzle_means



s4n,m4n = get_std_per_puzzle(nwp4,100)
s5n,m5n = get_std_per_puzzle(nwp5,100)
s6n,m6n=get_std_per_puzzle(nwp6,10)
s4w,m4w= get_std_per_puzzle(wp4,100)
s5w,m5w = get_std_per_puzzle(wp5,100)
s6w,m6w=get_std_per_puzzle(wp6,10)


db = '#013a96'
lb = '#afceff'
dr = '#960000'
lr = '#ff8787'
dg = '#00680a'
lg = '#4af74d'


plt.scatter(s4n,m4n, color=db,s=2,label='size 4 CB')
plt.scatter(s4w,m4w, color=lb,s=2,alpha=0.8,label='size 4 2WL')
plt.scatter(s5n,m5n, color=dr,s=2,label='size 5 CB')
plt.scatter(s5w,m5w, color=lr,s=2,alpha=0.8,label='size 5 2WL')
plt.scatter(s6n,m6n, color=dg,s=2,label='size 6 CB')
plt.scatter(s6w,m6w, color=lg,s=2,alpha=0.8,label='size 6 2WL')

plt.xlabel('Average CPU time (sec)')
plt.ylabel('Standard deviation (sec)')
plt.title('Correlation of average CPU time with standard deviation.')
plt.legend(loc='upper left',prop={'size': 10})
plt.show()


def get_mean_difference_per_run(wp,nwp, step):
	puzzle_stds = []
	puzzle_means = []

	for i in range(0,len(wp.CPU_time),step):
		puzzle_results = []
		for j in range(step):
			#print(i+j)
			dif = nwp.CPU_time[i+j] - wp.CPU_time[i+j]
			puzzle_results.append(dif)
		puzzle_stds.append(np.std(puzzle_results))
		puzzle_means.append(np.mean(puzzle_results))
	return puzzle_stds, puzzle_means
################################# DISTRIBUTIONS ###########################
def plot_distribution(title,*args):
	
	colors = ['r','b','g','y','o']
	i = 0
	for dataset in args:
		mu = np.mean(dataset.CPU_time)
		sigma = np.std(dataset.CPU_time)
		x = dataset.CPU_time
		num_bins = 50
		n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor=colors[i], alpha=0.2)
		#print(bins)
		y = mlab.normpdf(bins, mu, sigma)
		plt.plot(bins, y, colors[i], label=str(dataset.name))
		i+=1
	plt.title(title)
	plt.legend(loc='upper left',prop={'size': 6})
	plt.xlabel('CPU_time')
	plt.axis((0,.5,0,150))
	plt.ylabel('Count')
	
#######population stds##########
# fig = plt.figure()
# plt.suptitle('Population CPU time distributions')
# plt.subplot(311)
# plot_distribution('size 4',wp4,nwp4)
# plt.subplot(312)
# plot_distribution('size 5',wp5,nwp5)
# plt.subplot(313)
# plot_distribution('size 6',wp6,nwp6)
# plt.show()
####################


# s4nw,m4nw = get_std_per_puzzle(nwp4,100)
# s4w,m4w = get_std_per_puzzle(wp4,100)

# s5nw,m5nw = get_std_per_puzzle(nwp5,100)
# s5w,m5w = get_std_per_puzzle(wp5,100)

# s6nw,m6nw = get_std_per_puzzle(nwp6,10)
# s6w,m6w = get_std_per_puzzle(wp6,10)

# s4dif_std,s4dif_mean = get_mean_difference_per_run(wp4,nwp4,100)
# s5dif_std,s5dif_mean = get_mean_difference_per_run(wp5,nwp5,100)
# s6dif_std,s6dif_mean = get_mean_difference_per_run(wp6,nwp6,10)

#plt.subplot(211)
#x = np.arange(1050)
#plt.scatter(x,s4nw,color='r',alpha=0.5)
#plt.scatter(x,s4w,color='b',alpha=0.5)
#plt.show()
#plt.show()

# print("This is the standard deviation of CPU time over 100 runs, averaged over all puzzles.")
# print("Average standard deviation size4 CB: {}".format(np.mean(s4nw)))
# print("Average standard deviation size4 2WL: {}".format(np.mean(s4w)))
# print("The average difference between 2wp run and cb run is: {}".format(np.mean(s4dif_mean))) 
# print('\n')
# print("Average standard deviation size5 CB: {}".format(np.mean(s5nw)))
# print("Average standard deviation size5 2WL: {}".format(np.mean(s5w)))
# print("The average difference between 2wp run and cb run is: {}".format(np.mean(s5dif_mean))) 
# print('\n')

# print("Average standard deviation size6 CB: {}".format(np.mean(s6nw)))
# print("Average standard deviation size6 2WL: {}".format(np.mean(s6w)))
# print("The average difference between 2wp run and cb run is: {}".format(np.mean(s6dif_mean))) 
# print('\n')



# print("Average standard deviation of difference per puzzle run size 4: {}".format(np.mean(s4dif_std)))
# print("Average standard deviation of difference per puzzle run size 5: {}".format(np.mean(s5dif_std)))
# print("Average standard deviation of difference per puzzle run size 6: {}".format(np.mean(s6dif_std)))



# print("Average mean of difference per puzzle run size 4: {}".format(np.mean(s4dif_mean)))
# print("Average mean of difference per puzzle run size 5: {}".format(np.mean(s5dif_mean)))
# print("Average mean of difference per puzzle run size 6: {}".format(np.mean(s6dif_mean)))

# print("s4 CB mean: {}".format(np.mean(m4nw)))
# print("s4 2LW mean: {}".format(np.mean(m4w)))

# print("s5 CB mean: {}".format(np.mean(m5nw)))
# print("s5 2LW mean: {}".format(np.mean(m5w)))

# print("s6 CB mean: {}".format(np.mean(m6nw)))
# print("s6 2LW mean: {}".format(np.mean(m6w)))

# print("s4 dif std {}".format(np.mean(s4dif_std)))

# print("s5 dif std {}".format(np.mean(s5dif_std)))

# print("s6 dif std {}".format(np.mean(s6dif_std)))

# s4dif_std

# mu4 = np.mean(nwp4.conflicts)
# sigma4 = np.std(nwp4.conflicts)
# x4 = nwp4.conflicts
# num_bins = 50
# n, bins4, patches = plt.hist(x4, num_bins, normed=1, facecolor='r', alpha=0.2)
# #print(bins)
# y4 = mlab.normpdf(bins4, mu4, sigma4)
# plt.plot(bins4, y4, 'r', label='size 4')


# mu5 = np.mean(nwp5.conflicts)
# sigma5 = np.std(nwp5.conflicts)
# x5 = nwp5.conflicts
# num_bins = 50
# n, bins5, patches = plt.hist(x5, num_bins, normed=1, facecolor='b', alpha=0.2)
# #print(bins)
# y5 = mlab.normpdf(bins5, mu5, sigma5)
# plt.plot(bins5, y5, 'b', label='size 5')

# mu6 = np.mean(nwp6.conflicts)
# sigma6 = np.std(nwp6.conflicts)
# x6 = nwp6.conflicts
# num_bins = 50
# n, bins6, patches = plt.hist(x6, num_bins, normed=1, facecolor='g', alpha=0.2)
# #print(bins)
# y6 = mlab.normpdf(bins6, mu6, sigma6)
# plt.plot(bins6, y6, 'g', label='size 6')

# plt.ylabel('Count')
# plt.xlabel('Number of conflicts')
#plt.show()
# d = get_index_by_num_conflicts(nwp.conflicts)
# stds = []
# means = []
# num_conflicts = []
# for num_conflict in d:
# 	temp_list = []
# 	num_conflicts.append(num_conflict)
# 	for index in d[num_conflict]: #for each index associated with that conflict number
# 		temp_list.append(nwp.CPU_time[index] - wp.CPU_time[index])
# 	stds.append(np.std(temp_list))
# 	means.append(np.mean(temp_list))
# ##########FIG 6 ################ #subtracted CPU times BLACK BOTTOM
# y = means
# e = stds
# x = num_conflicts
# fig = plt.figure()
# fig.suptitle("Solving time against number of conflicts (size 4)", fontsize=16)
# plt.subplot(223)
# plt.errorbar(x,y,yerr=e,fmt='o',capsize=5,color='black', errorevery=1, markevery=1)
# #plt.axis((0,25,-0.015,.015))
# #plt.subplot(212)
# y = np.array(nwp.CPU_time)-np.array(wp.CPU_time)
# x = nwp.conflictsgit 
# plt.scatter(x,y, s=3, alpha=0.002,color='darkgrey')
# plt.ylabel('Difference CPU time (CB - 2WL)')
# plt.xlabel('Number of conflicts')
# #upper_bound = 1.1*np.amax(y)
# #lower_bound = avg1- 1.1*stdavg1
# plt.axis((-0.5,15,-0.01,0.01))
# plt.axhline(y=0, color='k',linewidth=0.1)

# plt.title("Solving time difference")

# plt.subplot(224)
# avg1 = np.mean(y)
# stdavg1=np.std(y)
# x_avg = np.arange(1)
# plt.errorbar(x_avg,avg1,yerr=stdavg1,fmt='o',color='black',capsize=5)
# plt.xlabel('avg')
# plt.ylabel('Average CPU time difference')
# upper_bound = avg1 + 1.1*stdavg1
# lower_bound = avg1- 1.1*stdavg1
# plt.axis((-1,1,lower_bound,upper_bound))
# plt.tick_params(
#     axis='both',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom='off',      # ticks along the bottom edge are off
#     top='off',         # ticks along the top edge are off
#     labelbottom='off')

# plt.axhline(y=0, color='k',linewidth=0.1)
# stds1 = []
# means1 = []
# stds2 = []
# means2 = []

# num_conflicts = []
# num_num_conflicts = []
# for num_conflict in d:
# 	temp_list1 = []
# 	temp_list2 = []
# 	num_conflicts.append(num_conflict)
# 	num_num_conflicts.append(len(d[num_conflict]))
# 	for index in d[num_conflict]: #for each index associated with that conflict number
# 		temp_list1.append(nwp.CPU_time[index])
# 		temp_list2.append(wp.CPU_time[index])

# 	stds1.append(np.std(temp_list1))
# 	means1.append(np.mean(temp_list1))
# 	stds2.append(np.std(temp_list2))
# 	means2.append(np.mean(temp_list2))

# ################ #seperate CPU times RED BLUE TOP
# y1 = means1
# y2 = means2

# e1 = stds1
# e2  = stds2
# x = num_conflicts
# plt.subplot(221)
# plt.errorbar(x,y1,yerr=e1,fmt='o',color='r',capsize=5,label='CB',markersize=3, errorevery=1, markevery=1)
# plt.errorbar(x,y2,yerr=e2,fmt='o', color='b',capsize=5,label='2WL', alpha=0.6, markersize=3, errorevery=1,markevery=1)
# #plt.scatter(x,y1,color='r',label='CB')
# #plt.scatter(x,y2, color='b',label='2WL', alpha=0.6)
# plt.legend(loc='upper left',prop={'size': 6})
# plt.axis((-.5,15,0.005,0.02))
# #plt.subplot(212)
# y1 = np.array(nwp.CPU_time)
# y2 = np.array(wp.CPU_time)
# x = nwp.conflicts
# plt.scatter(x,y1,color='r', s=3, alpha=0.002)
# plt.scatter(x,y2,color='b', s=3, alpha=0.002)
# plt.ylabel('CPU time')
# plt.xlabel('Number of conflicts')
# #plt.axis((-0.5,10,0,.03))
# plt.title("Solving time for both schemes")
# plt.subplot(222)
# avg1 = np.mean(nwp.CPU_time)
# avg2 = np.mean(wp.CPU_time)
# stdavg1=np.std(nwp.CPU_time)
# stdavg2=np.std(wp.CPU_time)
# x_avg = np.arange(1)
# plt.errorbar(x_avg,avg1,yerr=stdavg1,fmt='o',color='r',capsize=5,label='CB')
# plt.errorbar(x_avg,avg1,yerr=stdavg2,fmt='o', color='b',capsize=5,label='2WL', alpha=0.6)
# plt.xlabel('avg')
# plt.ylabel('Average CPU times')
# upper_bound = np.amax((avg1 + 1.1*stdavg1,avg2 + 1.1*stdavg2))
# lower_bound = np.amin((avg1 - 1.1*stdavg1,avg2 - 1.1*stdavg2))
# plt.axis((-1,1,lower_bound,upper_bound))
# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom='off',      # ticks along the bottom edge are off
#     top='off',         # ticks along the top edge are off
#     labelbottom='off')

# plt.show()

##############FIG 7 ########
# wp4 = parse_results(open("OUTPUT_s4_a.txt",'r'))
# wp5 = parse_results(open("OUTPUT_s5_a.txt",'r'))
# wp6 = parse_results(open("OUTPUT_s6_a.txt",'r'))

# x4,y4=get_num_conflicts_thing(wp4)
# x5,y5=get_num_conflicts_thing(wp5)
# x6,y6=get_num_conflicts_thing(wp6)

# plt.suptitle('Distribution over number of conflicts')
# plt.subplot(311)
# plt.title('Size 4')
# plt.scatter(x4,y4,color='g',s=3)
# plt.ylabel('Number sudokus')
# plt.xlabel('Number of conflicts')

# plt.subplot(312)
# plt.title('Size 5')
# plt.scatter(x5,y5,color='g',s=3)
# plt.ylabel('Number sudokus')
# plt.xlabel('Number of conflicts')

# plt.subplot(313)
# plt.title('Size 6')
# plt.scatter(x6,y6,color='g',s=3)
# plt.ylabel('Number sudokus')
# plt.xlabel('Number of conflicts')
# plt.show()
##############################3

#for i in range(np.max(nwp.conflicts)): #for each no of conflicts
	


# objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
# y_pos = np.arange(len(w_num_conflicts))
# performance = w_num_conflicts
# performance2 = nw_num_conflicts
# plt.bar(y_pos, performance, color='r',align='center', alpha=0.5)
# plt.bar(y_pos, performance2, color='b',align='center', alpha=0.5)
# plt.ylabel('Usage')
# plt.title('Programming language usage')
 
# plt.show()

#plt.subplot(211)
#plt.plot(x,np.divide(nwp.conflicts,nwp.CPU_time),color='#b30000',label='no watched literals')
#plt.plot(x,np.divide(wp.conflicts,wp.CPU_time),color='#003399',label='watched literals')

#plt.bar(x,wp.conflicts, color='#003399',label='watched literals', alpha=0.7)
#plt.legend(loc='upper left',prop={'size': 6})


# plt.subplot(212)
# plt.bar(x,nwp.CPU_time,color='#b30000',label='no watched literals')
# #plt.plot(x,wnp.conflicts,color='#4d88ff')
# plt.bar(x,wp.CPU_time,color='#003399',label='watched literals')
# plt.legend(loc='upper left',prop={'size': 6})
# plt.ylabel('Execution time')




######FIG 5 ####################
# x = np.arange(10490)
# y = np.array(nwp.conflicts)-np.array(wp.conflicts)
# plt.plot(x,y, color='#b30000')
# plt.ylabel('Difference between number of conflicts with and without 2WL')
# plt.xlabel('Sudoku puzzle index')
# plt.show()
#################################


# nw_conf_mean = np.mean(np.divide(nwp.conflicts,nwp.CPU_time))
# w_conf_mean = np.mean(np.divide(wp.conflicts,wp.CPU_time))

# nw_conf_std = np.std(np.divide(nwp.conflicts,nwp.CPU_time))
# w_conf_std = np.std(np.divide(wp.conflicts,wp.CPU_time))
# x = np.array([1, 2])
# y = np.array([w_conf_mean,nw_conf_mean])# Effectively y = x**2
# e = np.array([w_conf_std/2, nw_conf_std/2])
# plt.errorbar(x, y, yerr=e, fmt='o')
# plt.show()


# x = nw_num_conflicts
# y = w_num_conflicts
# data = np.vstack([x, y]).T
# bins = np.linspace(-10, 10, 30)
# =[]
# plt.hist(data, bins, alpha=0.7, label=['x', 'y'])
# plt.legend(loc='upper right')
# plt.show()