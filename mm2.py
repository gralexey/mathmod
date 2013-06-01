# -*- coding: utf8 -*-
# скрипт для ансамблирования глобальной матрицы жесткости и решения СЛАУ

import sys

# настройки
n = 41					# количество узлов
form = 1 								# 3 — кубическая функция формы, 1 — линейная функция формы

if len(sys.argv) == 3:
	n = int(sys.argv[1])
	form = int(sys.argv[2])
	if form != 1 and form != 3:
		exit('wrong form choice')
else:
	print "give first arg n, second — form (1 or 3)"
	exit()

segmentSize = 11.0		# длина рассматриваемого интервала

l = segmentSize / (n - 1)		# длина конечного элемента

print "l = ", l, "n = ", n, "form: ", form
# коэффициенты уравнения конечного элемента, когда известны первые производные на концах элемента


if form == 1:
	a11 = (5*l*l + 1) / l
	a12 = (5*l*l - 2) / (2*l)
	a21 = (5*l*l - 2) / (2*l)
	a22 = (5*l*l + 1) / l
	b1 = 2*l
	b2 = 2*l

if form == 3:
	v1 = (15*l**6 + 135*l**4 + 192*l**2 + 28) / (l*(15*l**4 + 52*l**2 + 28))		# переменные для удобства
	v2 = (15*l**6 - 30*l**4 + 72*l**2 - 112) / (4*l*(15*l**4 + 52*l**2 + 28))
	v3 = l*(l**2 + 4) / (3*l**2 + 2)
	a11 = v1
	a12 = v2
	a21 = v2
	a22 = v1
	b1 = v3
	b2 = v3

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
	F[i] -= T[i][0]*u0 
for i in range (n):		# удаление первого столбца
	T[i].pop(0)	
T.pop(0)				# удаление первой строчки
F.pop(0)

printMatrix(T, F)

# добавление строки и столбца
for i in range (n - 1):						# добавление столбца
	T[i].append(0)
T.append([0 for x in range(n)])				# добавление строчки
F.append(0)									# добвление единичной строчки к правой части

T[n - 2][n - 1] = -1
F[n - 2] = 0
T[n - 1][n - 2] = -1
T[n - 1][n - 1] = 1
F[n - 1] = 0

printMatrix(T, F)

from numpy import linalg
U = linalg.solve(T, F)
print U

# тест солвера слау
#total_error = 0
#for i in range(n-1):
#	sum = 0
#	for j in range(n-1):
#		sum += T[i][j] * U[j]
#	local_error = abs(F[i] - sum)
#	total_error += local_error
#print "total_error: ", total_error

# графика
from Tkinter import *
from math import sqrt, exp
root = Tk()
root.title('Model')

scale_k = 50
height = 600
width = 800
minus_height = 0

c = Canvas(root, height=height+minus_height, width=width)
c.pack()

def drawPoint(x, y, w,color):
	ex = w / 2				# эксцентриситет
	x = x * scale_k			# масштабирование
	y = y * scale_k
	x_p = 2 + x
	y_p = height - 2 - y	
	c.create_oval(x_p - ex, y_p - ex, x_p + w - ex, y_p + w - ex, outline=color, fill=color)

#def f(x):
#	return 2*(10**(-20))*exp(4*x) + 9.73*exp(-4*x) + 0.27

#def f(x):		# orig func
#	return (1/(15*(1 + exp(22*sqrt(15)))) ) * exp(-sqrt(15) * x) * (4*exp(sqrt(15)*x) + 146*exp(2*sqrt(15)*x) + 4*exp(sqrt(15)*(x+22)) + sqrt(15)*exp(sqrt(15)*(2*x+11)) - sqrt(15)*exp(11*sqrt(15)) + 146*exp(22*sqrt(15)))

def f(x):		# решение д.у. с граничным условием 3 рода на правой границе
	return (2*exp(-sqrt(15)*x) * (2*exp(sqrt(15)*x) + 2*sqrt(15)*exp(sqrt(15)*x) + 73*exp(2*sqrt(15)*x) + 73*sqrt(15)*exp(2*sqrt(15)*x) - 2*exp(sqrt(15)*x+22*sqrt(15)) + 2*sqrt(15)*exp(sqrt(15)*x+22*sqrt(15)) + 2*exp(2*sqrt(15)*x+11*sqrt(15)) - 2*exp(11*sqrt(15)) - 73*exp(22*sqrt(15)) + 73*sqrt(15)*exp(22*sqrt(15)))) / (15*(1 + sqrt(15) - exp(22*sqrt(15)) + sqrt(15)*exp(22*sqrt(15))))

y = 0.0
while(y <= segmentSize):
	drawPoint(0, y, 1,'black')
	y += 0.01

x = 0.0
while(x <= segmentSize):
	drawPoint(x, 0, 1,'black')
	drawPoint(x, f(x), 1,'red')
	x += 0.01

# отрисовка полученного решения и вывод численного решения
maxErr = 0.0
idxWithMaxErr = -1
drawPoint(0, u0, 7,'green')
for i in range(1, n):
	x = i*l
	currErr = abs(f(x) - U[i - 1])
	if currErr > maxErr:
		maxErr = currErr
		idxWithMaxErr = i
	print "x: %f\tf: %f.3\tu: %f.3\t\tdiff: %f" % (x, f(x), U[i - 1], currErr)
	drawPoint(x, U[i - 1], 7,'green')
print "maxErr: ", maxErr

mainloop()
