#!/usr/bin/python
import time
filename_in="data_in.txt"

#almacena los datos de entrada
data_in=[]

#almacena la matrix de similitud entre los objetos
matrix_out=[]

#carga el dataset en memoria -> data_in[][]
file=open(filename_in,"r+")
for line in file:
    data_in.append(line.split(","))
file.close();
	
matrix_out=[[0 for i in xrange(len(data_in))] for i in xrange(len(data_in))]

for i in range(len(data_in)):
	for j in range(len(data_in)):

		#calcula la suma de diferencias entre el objeto_i y el objeto_j
		#time.sleep(1)
		sumdiff=0
		for k in range(1,len(data_in[i])):
			sumdiff+=abs(int(data_in[i][k])-int(data_in[j][k]))

		#almacena la sumdiff
		matrix_out[i][j]=sumdiff

#imprime la matrix de similitud entre objetos
for i in range(len(matrix_out)):
	print i,matrix_out[i]
