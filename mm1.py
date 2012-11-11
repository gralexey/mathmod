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

root = Tk()
root.title('Model')

height = 450
width = 450
max_x = 10			# определяет рабочий прямоугольник для работы (0, 0, max_x, max_y)
max_y = 10
h = 0.4

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
			#point = round(x, 2), round(y, 2)
			xyt_dict[x, y] = t_idx		
			t_idx = t_idx + 1						
		x = round(x + h, 2)
	y = round(y + h, 2)


x = 0.0
y = 0.0
while (y <= max_y):
	x = 0.0
	while (x <= max_x):		# x, y  - координаты текущей точки, проверяемой на наличие соседей (для возможности вычислить 2-ю производную)
		left_n = round(x - h, 2)
		right_n = round(x + h, 2)
		top_n = round(y + h, 2)
		bottom_n = round(y - h, 2)
		if (
			(left_n, y)   in xyt_dict and
			(right_n, y)  in xyt_dict and
			(x, top_n)    in xyt_dict and
			(x, bottom_n) in xyt_dict
		   ):
			drawPoint(x ,y, "blue")		
		x = round(x + h, 2)
	y = round(y + h, 2)


#x = 5.2
#y = 3.6
#if ((x,y) in xyt_dict):
#	print (x,y), " in dict!!"
#	drawBoldPoint(x, y, "black")
#
#left_n = round(x - h, 2)
#right_n = round(x + h, 2)
#top_n = round(y + h, 2)
#bottom_n = round(y - h, 2)
#
#if ((left_n, y) in xyt_dict):
#	print (left_n, y), " left neighbour in dict"
#	drawBoldPoint(left_n, y, "orange")
#
#if ((round(right_n, 2), round(y, 2)) in xyt_dict):	
#	drawBoldPoint(right_n, y, "orange")	
#
#if ((x, top_n) in xyt_dict):
#	print (x, top_n), " top neighbour in dict"
#	drawBoldPoint(x, top_n, "orange")
#
#if ((x, bottom_n) in xyt_dict):
#	print (x, bottom_n), " bottom neighbour in dict"
#	drawBoldPoint(x, bottom_n, "orange")

drawBounds()


mainloop()