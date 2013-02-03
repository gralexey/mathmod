# -*- coding: utf8 -*-
# скрипт для ансамблирования СЛАУ и ее решения

# настройки
n = 8					# количество узлов
segmentSize = 11		# длина рассматриваемого интервала

l = segmentSize / 4		# длина конечного элемента

print "l = ", l
# коэффициенты уравнения конечного элемента, когда известны первые производные на концах элемента
a11 = (5*l*l + 1) / l
a12 = (5*l*l - 2) / l
a21 = (5*l*l - 2) / l
a22 = (5*l*l + 1) / l

b1 = 2*l
b2 = 2*l

deriv1 = 123			# в решаемом варианте (23) это значение нам не известно
deriv2 = 1
u0 = 10
u_end = 123				# в решаемом варианте (23) это значение нам не известно

def printMatrix(a, b):
	idx = 0
	for row in a:
		print row, b[idx]
		idx += 1
	print " "

# Matrix = [[0 for x in xrange(5)] for x in xrange(5)] 

T = range(n)
F = range(n)
for i in range(n):
	T[i] = range(n)
	F[i] = 0

for i in range(n):
	for j in range(n):
		T[i][j] = 0

for i in range(n - 1):
	T[i][i] += a11
	T[i][i+1] += a12
	T[i+1][i] += a21
	T[i+1][i+1] += a22
	F[i] += b1
	F[i+1] = b2
F[0] += -deriv1
F[n-1] += deriv2 

# теперь, если решить СЛАУ TU = F относительно U, в U будут искомые значения функции в соответствующих точках при условии, что нам известны первые производные на концах интервала.
# так как первая производная (deriv1) на начале интервала нам не известна, но известно само значение (U[0]), можно исключить первый столбец матрицы T домножив его на U[0]
# и перенеся в правую часть (F); теперь можно исключить и первую строчку с неизвестной первой производной

#printMatrix(T, F)

# учет u0 в F
for i in range(1, n):
	F[i] += T[i][0]*u0 

# учет u_end в F
#for i in range(0, n - 1):
#	F[i] += T[i][n-1]*u0 
#	print i	

#printMatrix(T, F)

for i in range (n):		# удаление первого столбца
	T[i].pop(0)	
T.pop(0)				# удаление первой строчки
F.pop(0)

#printMatrix(T, F)

from numpy import linalg
U = linalg.solve(T, F)
print u0, U

# графика
from Tkinter import *
from math import sqrt, exp
root = Tk()
root.title('Model')

scale_k = 50
height = 500
width = 600

c = Canvas(root, height=height, width=width)
c.pack()

def drawPoint(x, y, w,color):	
	x = x * scale_k			# масштабирование
	y = y * scale_k
	x_p = 2 + x
	y_p = height - 2 - y	
	c.create_oval(x_p, y_p, x_p + w, y_p + w, outline=color)

def f(x):
	return 2*(10**(-20))*exp(4*x) + 9.73*exp(-4*x) + 0.27

y = 0.0
while(y <= 11):
	drawPoint(0, y, 1,'black')
	y += 0.1

x = 0.0
while(x <= 11):
	drawPoint(x, 0, 1,'black')
	drawPoint(x, f(x), 1,'red')
	x += 0.01

drawPoint(0, u0, 7,'green')
for i in range(1, n):
	print i
	drawPoint(i*l, U[i - 1], 7,'green')

mainloop()
