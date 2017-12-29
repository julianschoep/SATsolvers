from bs4 import BeautifulSoup
import numpy as np
import re
import requests

import os.path
import sys, getopt


regex = re.compile(r'(?:<a.*?>\s*(.*?)\s*</a>)|(\w+)', re.IGNORECASE)




def main(argv):
	
	#print(str)
	XWING = False
	CROSSHATCHING = False
	ALTERN_PAIRS = False
	help_str = 'script.py -d <difficulty> -o <outdir> -n <number> -s <box-size>'
	try:
		opts, args = getopt.getopt(argv,"hd:o:n:s:",["difficulty=", "outdir=", "number=","size="])

	except getopt.GetoptError:
		print (help_str)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print (help_str)
			sys.exit()
		elif opt in ("-d", "--difficulty"):
			difficulty = arg
		elif opt in ("-o", "--outdir"):
			outdir = arg
			if not os.path.exists(outdir):
				os.makedirs(outdir)
		elif opt in ("-n", "--number"):
			N = int(arg)
		elif opt in ("-s", "--block-size"):
			size = int(arg)

	assert (int(difficulty) >=0 and int(difficulty) <= 9), "difficulty ranges between 0 and 9!"
	assert (N >= 0), "the number of sudokus must be non negative"
	s_list = []
	i=0
	dim = size**2
	while i <N:    
		if(dim == 9):
			page = requests.get('http://www.menneske.no/sudoku/eng/random.html?diff='+difficulty)
		else:
			page = requests.get('http://www.menneske.no/sudoku/'+str(size)+'/eng/random.html?diff='+difficulty)
		#soup = BeautifulSoup(page.text)
		soup = BeautifulSoup(page.text, "lxml")
		s_id=str(soup.body).split("number: ")
		if len(s_id) < 2:
			print("Sudoku not found")
			break
		s_id = s_id[1][0:7].split('<')[0]
		
		table = soup.find('div', class_='grid')
		if s_id in s_list:
			print(s_id," is a copy\n")
		else:
			i+=1
			print("Importing Sudoku # ",i," on ",N," ----- ID: ",s_id)
			s_list.append(s_id)
			sudoku = np.zeros((dim, dim))
			
			encoding=""
			num_clauses = calculate_standard_num_clauses(size)
			num_variables = (size*size)**3
			encoding = add_full_cnf(encoding,size)
			r=0
			for row in table.find_all('tr'):
				c=0
				for col in row.find_all('td'):
					
					x=(str(col).split('>',1)[1].split('<')[0])
					dum = x
					if not dum.strip():
						x = str(0)
						
					#x = x.replace(" ","0")
					#print(i,r,c)
					
					sudoku[r][c]=int(x)
                    
					if x!="0":
						
						encoding+= str(r+1)+'.'+str(c+1)+'.'+x+" 0\n"
						num_clauses +=1
						#for d in range(1,10):
							#if str(d) != x: #print negative clauses
								#encoding += '-'+str(r+1)+str(c+1)+str(d)+" 0\n"
								
					c+=1
				r+=1
            
			dimac_first_line = 'p cnf {0} {1}\n'.format(num_variables, num_clauses)
			tmp = str(soup.body).split("Solution methods:  ")        
			tech = []
			if len(tmp) > 1:
				tmp =regex.findall(tmp[1].split("<br/>")[0])
				for t in tmp:
					if t[0] == '':
						tech.append(t[1])
					else:
						tech.append(t[0])
            
            #print("Printing Sudoku # ",i," on ",N," ----- ID: ",s_id)
            #print(sudoku)
            #print(encoding)
            #print(tech)        
			#print(s_id)
			# with open(os.path.join(outdir, s_id+"_sudoku.txt"), "w") as myfile:
				# for r in range(size*size):
					# for c in range(size*size):
						# myfile.write(str(int(sudoku[r][c]))+" ")
					# myfile.write("\n")
				# myfile.close()
					
			# with open(os.path.join(outdir, s_id+"_encoded.txt"), "w") as myfile:
				# myfile.write(encoding)
				# myfile.close()
				
			with open(os.path.join(outdir, "dif"+str(difficulty)+"size"+str(size)+"_dimac"+s_id+".txt"), "w") as f:
				encoding = convert_encoding_to_dimac(encoding,size)
				encoding = dimac_first_line + encoding
				f.write(encoding)
				f.close()
			# with open(os.path.join(outdir, s_id + '_info.txt'), 'w') as f:
				# for t in tech:
					# f.write(t + '\n')
				# f.close()


			print("     Done")

	print('Finished!')
	
def calculate_standard_num_clauses(size):	
	n = size*size
	return 2*(n**4)-2*(n**3)+4*(n**2)
	
def convert_chron(x,y,z, size):
	dim = size*size
	result = (dim*dim)*(x-1)+(dim*(y-1))+z
	return result
	
def convert_encoding_to_dimac(encoding,size):
	result =''
	lines = encoding.splitlines()
	for line in lines:
		literals = line.split()
		for literal in literals:
			if literal[0] != '0': #End of line char
				if literal[0] == '-': #is negative
				
					x,y,z = literal[1:].split('.')
					new_lit = convert_chron(int(x),int(y),int(z),size)*-1
					result += str(new_lit)+' '
				else:
					x,y,z = literal.split('.')
					new_lit = convert_chron(int(x),int(y),int(z),size)
					result += str(new_lit)+' '
		result+='0\n'
	return result
	
def add_full_cnf(string,size):
	string = col_at_least_one(string,size)
	string = row_at_least_one(string,size)
	string = val_at_least_one(string,size)
	string = block_at_least_one(string,size)
	string = row_at_most_one(string,size)
	string = col_at_most_one(string,size)
	string = val_at_most_one(string,size)
	string = block_at_most_one(string,size)
	return string
	#print(string)
	#print( len(string.split('\n')))

				
	return string
def val_at_least_one(string,size):
	size_sq = size*size
	for r in range(1,size_sq+1):	#at least one per cell
		for c in range(1,size_sq+1):
			line = ''
			for v in range(1,size_sq+1):
				line+= str(r)+'.'+str(c)+'.'+str(v)+' ' 
			string += line + '0\n'
			
	return string
def val_at_most_one(string,size):
	size_sq = size*size
	for r in range(1,size_sq+1):	#at most one per cell
		for c in range(1,size_sq+1):
			for v1 in range(1,size_sq+1):
				for v2 in range(v1+1,size_sq+1):
					line = '-'+str(r)+'.'+str(c)+'.'+str(v1) +' ' +'-'+str(r)+'.'+str(c)+'.'+str(v2)
					string += line + ' 0\n'
	return string
def col_at_least_one(string,size):
	size_sq = size*size
	for r in range(1,size_sq+1):	#at least one per column
		for c in range(1,size_sq+1):
			line = ''
			for v in range(1,size_sq+1):
				line+= str(r)+'.'+str(v)+'.'+str(c)+' ' 
			string += line + '0\n'
			
	return string
def col_at_most_one(string,size):
	size_sq = size*size
	for r in range(1,size_sq+1):	#at most one per column
		for c in range(1,size_sq+1):
			for v1 in range(1,size_sq+1):
				for v2 in range(v1+1,size_sq+1):
					line = '-'+str(r)+'.'+str(v1)+'.'+str(c) +' ' +'-'+str(r)+'.'+str(v2)+'.'+str(c)
					string += line + ' 0\n'
				
	return string
def row_at_least_one(string,size):
	size_sq = size*size
	for r in range(1,size_sq+1):	#at least one per row
		for c in range(1,size_sq+1):
			line = ''
			for v in range(1,size_sq+1):
				line+= str(v)+'.'+str(c)+'.'+str(r)+' '
			string += line + '0\n'
			
	return string
def row_at_most_one(string, size):
	size_sq = size*size
	for r in range(1,size_sq+1):	#at most one per row
		for c in range(1,size_sq+1):
			for v1 in range(1,size_sq+1):
				for v2 in range(v1+1,size_sq+1):
					line = '-'+str(v1)+'.'+str(c)+'.'+str(r) +' ' +'-'+str(v2)+'.'+str(c)+'.'+str(r)
					string += line + ' 0\n'
					
	return string
	
def block_at_least_one(string, size):
	size_sq = size*size
	for v in range(1,size_sq+1): #at least one per block
		
		for r_i in range(0,size_sq, size): #0,3,6
			for c_i in range(0, size_sq, size): #0,3,6
				line = ''
				for r in range(1,size+1): #1,2,3
					for c in range(1,size+1): #1,2,3
						line+= str(r+r_i)+'.'+str(c+c_i)+'.'+str(v)+' '
				string += line+ '0\n'
				
	return string

	
def block_at_most_one(string, size):
	size_sq = size*size
	for v in range(1,size_sq+1): #at most one per block
		
		for r_i in range(0,size_sq, size): #0,3,6
			for c_i in range(0, size_sq, size): #0,3,6
				for r in range(1,size+1): #1,2,3
					for c in range(1,size+1): #1,2,3
						gen = block_generator(size,r_i,c_i)
						while True:
							tuple = next(gen,None)
							if not tuple: #generator empty
								break
							r_2,c_2 = tuple
							if(r_2*100+c_2) > ((r_i+r)*100+(c+c_i)):
								line = '-'+str(r_i+r)+'.'+str(c_i+c)+'.'+str(v)+' -'+str(r_2)+'.'+str(c_2)+'.'+str(v)
								string += line+ ' 0 \n'
	return string
								
def block_generator(size, r_i, c_i):
	for r in range(1, size+1):
		for c in range(1, size+1):
			yield r+r_i, c+c_i
	
	
if __name__ == "__main__":
	main(sys.argv[1:])
