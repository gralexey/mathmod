# -*- coding: utf8 -*-

from Tkinter import *
from math import sqrt

def validatePoint(x, y):		# возвращает true, если точка принадлежит области, определенной неравенствами 
	if (x >= 0 and y >=0 and x <= 8 and y <= 6 and ((x - 5)**2 + (y - 3)**2 <= 3**2 or x <= 5 or y <= 3)):
		return True
	return False

def drawPoint(x, y, color):	
	x = x * 40			# масштабирование
	y = y * 40
	x_p = 20 + x
	y_p = height - 20 - y
	c.create_rectangle(x_p, y_p, x_p, y_p, outline=color)

def drawCircle(x, y, radius, color):	
	x = x * 40			# масштабирование
	y = y * 40
	x_p = 20 + x
	y_p = height - 20 - y
	c.create_oval(x_p - radius, y_p - radius, x_p + radius, y_p + radius, outline=color, fill=color)

def drawBoldPoint(x, y, color):	
	x = x * 40			# масштабирование
	y = y * 40
	x_p = 20 + x
	y_p = height - 20 - y
	c.create_rectangle(x_p - 3, y_p - 3, x_p +3 , y_p + 3, outline=color, fill=color)

def drawBounds():				# рисуем границы для рабочего прямоугольника (0, 0, max_x, max_y)
	x = 0.0
	while (x <= max_x):
		drawPoint(x, max_y, "green")
		x = x + 0.1
	y = 0.0
	while (y <= max_y):
		drawPoint(max_x, y, "green")
		y = y + 0.1

def printMatrix(a, b):
	idx = 0
	for row in a:
		print row, b[idx]
		idx += 1

def defineTopCondiments():
	# задаем граничные условия с верхней стороны фигуры
	x = 0.0
	y = max_y
	while (x <= max_x):
		y = max_y
		while (y >= 0):
			if validatePoint(x, y):
				t_border = xyt_dict[x, y]
				temperatureInPoint[t_border] = 100
				break						
			y = round(y - h, hr)
		x = round(x + h, hr)

def defineBottomCondiments():
	# задаем граничные условия с нижней стороны фигуры
	x = 0.0
	y = 0.0
	while (x <= max_x):
		y = 0.0
		while (y <= max_y):
			if validatePoint(x, y):
				t_border = xyt_dict[x, y]
				temperatureInPoint[t_border] = 50
				break						
			y = round(y + h, hr)
		x = round(x + h, hr)

def defineRightCondiments():
	# задаем граничные условия с правой стороны фигуры
	x = max_x
	y = 0.0
	while (y <= max_y):
		x = max_x
		while (x >= 0):
			if validatePoint(x, y):
				t_border = xyt_dict[x, y]
				temperatureInPoint[t_border] = 100
				break						
			x = round(x - h, hr)
		y = round(y + h, hr)

def defineLeftCondiments():
	# задаем граничные условия с левой стороны фигуры
	x = 0.0
	y = 0.0
	while (y <= max_y):
		x = 0.0
		while (x <= max_x):
			if validatePoint(x, y):
				t_border = xyt_dict[x, y]
				temperatureInPoint[t_border] = 200
				break						
			x = round(x + h, hr)
		y = round(y + h, hr)

root = Tk()
root.title('Model')

height = 450
width = 450
max_x = 10			# определяет рабочий прямоугольник для работы (0, 0, max_x, max_y)
max_y = 10
h = 0.5
hr = 2 				# шаг для округления погрешности сложения (втф!!!!!)

c = Canvas(root, height=height, width=width)
c.create_line(20, height - 20, width - 20, height - 20)
c.create_line(20, height - 20, 20, 20)
c.pack()
drawBounds()


# русуем заданную в validatePoint() фигуру и задаем словарь xyt_dict соответствия
# координаты номеру соответствующего элемента (x, y => t) для использования с матрицой
xyt_dict = {}
t_idx = 0
x = 0.0
y = 0.0
while (y <= max_y):
	x = 0.0
	while (x <= max_x):
		#drawPoint(x, y, "gray")			# внешние нерабочие точки, для наглядности
		if validatePoint(x, y):
			drawPoint(x, y, "red")
			xyt_dict[x, y] = t_idx		
			t_idx += 1						
		x = round(x + h, hr)
	y = round(y + h, hr)


n = t_idx						# размер матрицы
T = range(n)
for i in range(n):
	T[i] = range(n)

for i in range(n):
	for j in range(n):
		T[i][j] = 0


F = range(n)
for i in range(n):
	F[i] = 0

print "matrix size: ", n
tStore = array('f', 0)
print tStore

rowCount = 0
x = 0.0
y = 0.0
while (y <= max_y):
	x = 0.0
	while (x <= max_x):		
	# x, y  - координаты текущей точки, проверяемой на наличие соседей (для возможности вычислить 2-ю производную)
		left_n = round(x - h, hr)
		right_n = round(x + h, hr)
		top_n = round(y + h, hr)
		bottom_n = round(y - h, hr)
		if (
			(left_n, y)   in xyt_dict and
			(right_n, y)  in xyt_dict and
			(x, top_n)    in xyt_dict and
			(x, bottom_n) in xyt_dict
		   ):
			drawPoint(x , y, "blue")			# для синенькой точки можно посчитать производную
			t_current = xyt_dict[x, y]			# индексы текущей точки и прилежащих
			t_left    = xyt_dict[left_n, y]
			t_right   = xyt_dict[right_n, y]
			t_top     = xyt_dict[x, top_n]
			t_bottom  = xyt_dict[x, bottom_n]
			T[rowCount][t_left] = 1 			# тут задаем коэффициенты из разностного уравнения
			T[rowCount][t_current] = -4
			T[rowCount][t_right] = 1
			T[rowCount][t_bottom] = 1
			T[rowCount][t_top] = 1
			rowCount += 1
		x = round(x + h, hr)
	y = round(y + h, hr)

temperatureInPoint = {}


defineLeftCondiments()
defineRightCondiments()
defineBottomCondiments()
defineTopCondiments()

# задаем температуры точек в матрице 
for point in temperatureInPoint:
	T[rowCount][point] = 1
	F[rowCount] = temperatureInPoint[point]
	rowCount += 1

#printMatrix(T, F)

import numpy
t = numpy.linalg.solve(T, F)		# t содержит значения температур элементов (последовательно)
#print t



temp = xyt_dict.items()
for item in temp:
	pointXY = item[0]	
	t_Idx = item[1]	
	tOfPoint = t[t_Idx]
	#print pointXY, t_Idx, tOfPoint
	temperatureRadius = tOfPoint * 10.0 / 200.0
	drawCircle(pointXY[0], pointXY[1], temperatureRadius, "red")


mainloop()