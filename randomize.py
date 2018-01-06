import os
from os import listdir
import sys, getopt
import time
import simplejson
from random import shuffle


def main(argv):
	help_str = 'aut_parser.py -i <input_dir> -s <box-size> -a <minisat arguments, delimit with .  >'
	try:
		opts, args = getopt.getopt(argv,"hi:s:a:",["input_dir=","size=","args="])

	except getopt.GetoptError:
		print (help_str)
		sys.exit(2)
	arguments = None
	for opt, arg in opts:
		if opt == '-h':
			print (help_str)
			sys.exit()
		elif opt in ("-i", "--input_dir"):
			input_dir = arg
		elif opt in ("-s", "--size"):
			size = arg
		elif opt in ("-a", "--args"):
			arguments = arg

	minisat_arguments = parse_minisat_arguments(arguments)
	
	base_time = 0
	total_time = 0
	some_number = 10
	for i in range(some_number):
		
		d_time = check_base_time('test.txt')
		if(i>0):
			print(d_time)
			total_time += d_time
	base_time = total_time/some_number
	print(base_time)
	
	base_dir= os.path.abspath(os.path.dirname(__file__))
	
	dimacs_path = os.path.join(base_dir,input_dir)
	filenames = listdir(dimacs_path)
	dimacs = [f for f in filenames if f[-3:]=='txt']
	n = int(size)*int(size)
	num_binary = 2*n**4 - 2*n**3
	result_list = []
	total_time = 0
	num_sudokus = 0
	line_cntr = 0
	for dimac_file in dimacs:
		line_cntr +=1
		dimac_file_path = os.path.join(dimacs_path, dimac_file)
		original_file = open(dimac_file_path,'r')
		if(line_cntr >0):
			for i in range(20):
				num_sudokus +=1
				print("Solving the {0}th randomization of the {1}th file".format(i,line_cntr))
				temp_file, n_lines = randomize_file(original_file,i)

				#temp_path = os.path.realpath(original_file.name)
				#execution_line = './minisat_static {0} {1}'.format(temp_path, minisat_arguments)
				#s_time = time.process_time()
				#minisat_EXE = os.popen(execution_line)
				#e_time = time.process_time()
				#d_time = e_time - s_time - base_time
				#print(d_time)
				
				#total_time += (d_time)
				#minisat_out = minisat_EXE.read()
				#print(minisat_out)
				#result = get_stats(minisat_out, d_time,n_lines)
				#result_list.append(result)
	#output_name = "OUTPUT_s{0}_a{1}.txt".format(size,minisat_arguments)
	#output = open(output_name,"w")
	#parse_results(result_list, output, num_binary)
	#output.close()
	#print("{0} sudoks were solved in {1} seconds".format(num_sudokus, total_time))
	
def check_base_time(filename):
	s = time.process_time()
	minisat = os.popen('./minisat_static '+filename)
	e= time.process_time()
	return e-s
	
def parse_results(list, file, num_binary):
	conf_lit_list = []
	conflict_list = []
	CPU_list = [] 
	parse_list = [] 
	measured_time_list = []
	bin_ratio_list = []
	fk_clauses_list = []
	clauses_list = []
	for result in list:
		print(result.num_clauses)
		print(num_binary)
		bin_ratio =  num_binary/int(result.num_clauses)
		conflict_list.append(result.conflicts)
		conf_lit_list.append(result.conf_literals)
		CPU_list.append(result.CPU_time)
		parse_list.append(result.parse_time)
		bin_ratio_list.append(bin_ratio)
		#measured_time_list.append(result.measured_time)
		#fk_clauses_list.append(int(result.num_clauses_fk))
		clauses_list.append(result.num_clauses)
	file.write("Conflict literals \n")
	simplejson.dump(conf_lit_list,file)
	file.write("\n")
	file.write("Num conflicts \n")
	simplejson.dump(conflict_list,file)
	file.write("\n")
	file.write("CPU_LIST \n")
	simplejson.dump(CPU_list,file)
	file.write("\n")
	file.write("parse_list \n")
	simplejson.dump(parse_list,file)
	file.write("\n")
	#file.write("measured_time_list \n")
	#simplejson.dump(measured_time_list,file)
	#file.write("\n")
	file.write("bin_ratio_list \n")
	simplejson.dump(bin_ratio_list,file)
	file.write("\n")
	#file.write("fk_clauses_list \n")
	#simplejson.dump(fk_clauses_list,file)
	#file.write("\n")
	file.write("clauses_list \n")
	simplejson.dump(clauses_list,file)
	print("DONE")
	
def get_stats(minisat_out, measured_time, n_lines):
	restarts= None; conficts= None; decisions= None;
	propagations= None;mem_used= None; CPU_time= None; 
	parse_time= None; num_vars= None; num_cl= None
	for line in minisat_out.splitlines():
		
		if "Number of variables" in line:
			num_vars = line.split(':')[1].strip().split('|')[0]
			#print('Number of variables is {}'.format(num_vars))
		if "Number of clauses" in line:
			num_cl = line.split(':')[1].strip().split('|')[0]
			#print('Number of variables is {}'.format(num_cl))	
		if "Parse time" in line:
			parse_time = line.split(':')[1].strip().split('s')[0]
			#print('Parse time is {}'.format(parse_time))	
		if "CPU time" in line:
			CPU_time = line.split(':')[1].strip().split('s')[0]
			#print("CPU TIME: "+CPU_time)	
		if "conflicts" in line:
			conflicts = line.split(':')[1].strip().split('(')[0]
		if "conflict literals" in line:
			conf_literals = line.split(':')[1].strip().split('(')[0]
	return Minisat_result(conf_literals, conflicts, CPU_time, parse_time, num_vars, num_cl, measured_time,n_lines-1)


def randomize_file(input_file,index):
	
	clauses_list = []
	first_line = ''
	num_lines = 0
	input_file.seek(0)
	inputs = input_file.read()
	#print(len(inputs.splitlines()))
	##print("HO")
	for line in inputs.splitlines():
		#print(line)
		num_lines +=1

		if line[0]=='p':
			first_line = line
		else:
			line = reorder(line)
			clauses_list.append(line)
	#print("clauses lsit before suffle"+str(len(clauses_list)))
	shuffle(clauses_list)
	#print("clauses lsit after suffle"+str(len(clauses_list)))
	random_file_name = input_file.name.split(".txt")[0]+"_"+str(index)+"_.txt"
	#print(first_line)
	#print(len(clauses_list))
	f = open(random_file_name,"w")
	f.write(first_line+'\n')
	for n_line in clauses_list:
		#print(n_line)
		f.write(n_line)
	f.close()
	return None, num_lines
	
	
def reorder(line):
	new_line = ''
	lit_list = []
	
	for literal in line.split():
		if literal != '0':
			lit_list.append(literal)
	shuffle(lit_list)
	for i in lit_list:
		new_line += i+' '
	new_line += '0\n'
	return new_line

class Minisat_result:
	conflicts = 0
	CPU_time = 0 #Sec
	parse_time = 0 #sec
	num_vars = 0
	num_clauses_fk = 0
	num_clauses = 0
	measured_time = 0
	def __init__(self, conf_literals,conflicts, CPU_time, parse_time, num_vars, num_clauses_fk, measured_time, num_clauses):
		self.conf_literals = conf_literals
		self.conflicts = conflicts
		self.CPU_time = CPU_time
		self.parse_time = parse_time
		self.num_vars = num_vars
		self.num_clauses_fk = num_clauses_fk
		self.num_clauses = num_clauses
		self.measured_time = measured_time
		
		
def parse_minisat_arguments(arguments):	
		if not arguments:
			print("no arguments given")
			result = ''
		else:
			result = ''
			args = arguments.split('.')
			for arg in args:
				result += arg
			
		return result
		

		
		
		
if __name__ == "__main__":
	main(sys.argv[1:])