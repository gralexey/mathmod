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

def printMatrix(matrix):
	for row in matrix:
		print row

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
			t_idx = t_idx + 1						
		x = round(x + h, hr)
	y = round(y + h, hr)


n = t_idx						# размер матрицы
T = range(n)
for i in range(n):
	T[i] = range(n)

for i in range(n):
	for j in range(n):
		T[i][j] = 0

#printMatrix(T)

print t_idx

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
			

		x = round(x + h, hr)
	y = round(y + h, hr)




drawBounds()
mainloop()