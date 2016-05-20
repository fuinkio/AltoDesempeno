# Universidad EAFIT, Ing de Sistemas, ST0263 Top Esp en Telematica
# Edwin Montoya - emontoya@eafit.edu.co
# 2016-1

# variables de configuracion

filename_in	= "data_in.txt"
max_items 	= 2000
max_users 	= 2000
umbral_cont 	= 1	# numero minimo de items en comun para tener en cuenta entre 2 usurios
max_diff = 	4 	# maxima diferencia entre rating para 2 usuarios.

	#funciones de utilidad

# funcion de correlacion entre el user i y el user j

def corr(i,j):
	cont=0
	diff=0
	for x in range(max_items):
		if matrix[i][x]*matrix[j][x] != 0:
			cont+=1
			diff=diff+max_diff-abs(matrix[i][x]-matrix[j][x])
	return cont,diff*cont

# funcion de ordenamiento de mayor a menor de relavancia de usuarios por fila (user) despues de calcular
#	todas las correlaciones de un usuario con todos los demas.

def sortUserCorr(userid, userRow):
	tmpUser=-1
	tmpCont=-1
	tmpDiff=-1

	for i in range(len(userRow)-1):
	    for j in range(i+1,len(userRow)):
		if userRow[i][2] < userRow[j][2]:
			tmpUser=userRow[i][0]
			tmpCont=userRow[i][1]
			tmpDiff=userRow[i][2]
			userRow[i][0] = userRow[j][0]
			userRow[i][1] = userRow[j][1]
			userRow[i][2] = userRow[j][2]
			userRow[j][0] = tmpUser
			userRow[j][1] = tmpCont
			userRow[j][2] = tmpDiff
	print ' userid=',userid, ' similar=',userRow[:5]

# PROGRAMA PRINCIPAL

#iniciar la matrix y cargar los datos del archivo

matrix = [[0 for i in xrange(max_users)] for i in xrange(max_items)]
f = open(filename_in,"r")
for line in f:
	user,movie,r,_=line.split()
	matrix[int(user)][int(movie)] = int(r)

matcorr = []
for y1 in range(max_users):
	matcorr.append([])
	for y2 in range(y1+1,max_users):
		c,d = corr(y1,y2)
		if c >= umbral_cont:
			matcorr[y1].append([y2,c,d])
	if len(matcorr[y1]) > 0:
		sortUserCorr(y1,matcorr[y1])

print matcorr[:1][:3]

