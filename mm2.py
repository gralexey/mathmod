# -*- coding: utf8 -*-
# скрипт для ансамблирования глобальной матрицы жесткости и решения СЛАУ

# настройки
n = 21					# количество узлов
segmentSize = 16.0		# длина рассматриваемого интервала

l = segmentSize / (n - 1)		# длина конечного элемента

print "l = ", l
# коэффициенты уравнения конечного элемента, когда известны первые производные на концах элемента

form = 3 								# 3 — кубическая функция формы, 1 — линейная функция формы
if form == 1:
	a11 = 1/l - 0.5
	a12 = -1/l + 0.5
	a21 = -1/l - 0.5
	a22 = 1/l + 0.5
	b1 = 2*l
	b2 = 2*l

if form == 3:
	v1 = -(60*l + l**3 - 120 - 12*l**2) / (2*l*(60 + l**2))				# переменные для удобства
	v2 = -(60*l + l**3 + 120 + 12*l**2) / (2*l*(60 + l**2))
	v3 = 2*l*(60 + l**2 - 10*l) / (l**2 + 60)
	a11 = v1
	a12 = -v1
	a21 = v2
	a22 = -v2
	b1 = v3
	b2 = v3

deriv1 = 123			# в решаемом варианте (23) это значение нам не известно
deriv2 = 12
u0 = 1
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

#printMatrix(T, F)

for i in range (n):		# удаление первого столбца
	T[i].pop(0)	
T.pop(0)				# удаление первой строчки
F.pop(0)

#printMatrix(T, F)

from numpy import linalg
U = linalg.solve(T, F)
#print U

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

scale_xk = 50
scale_yk = 10
height = 800
width = 850
minus_height = 0

c = Canvas(root, height=height+minus_height, width=width)
c.pack()

def drawPoint(x, y, w,color):
	ex = w / 2				# эксцентриситет
	x = x * scale_xk		# масштабирование
	y = y * scale_yk
	x_p = 2 + x
	y_p = height - 2 - y	
	c.create_oval(x_p - ex, y_p - ex, x_p + w - ex, y_p + w - ex, outline=color, fill=color)

def f(x):
	return 4*x + 8*exp(x - 16) - 8*exp(-16) + 1

y = 0.0
while(y <= segmentSize):
	drawPoint(0, y, 1,'black')
	y += 0.01

x = 0.0
while(x <= segmentSize):
	drawPoint(x, 0, 1,'black')
	drawPoint(x, f(x), 1,'red')
	x += 0.01

# отрисовка полученного решения
drawPoint(0, u0, 7,'green')
for i in range(1, n):
	x = i*l
	#print i*l, "\t\t:\t\t", U[i - 1]
	print "%f.3\t: %f.3\t diff: %f" % (x, U[i - 1], abs(f(x) - U[i - 1]))
	drawPoint(x, U[i - 1], 7,'green')

mainloop()
