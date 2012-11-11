# -*- coding: utf8 -*-

from Tkinter import *
from math import sqrt

def validatePoint(x, y):		# возвращает true, если точка принадлежит области, определенной неравенствами 
	if (x >= 0 and y >=0 and x <= 8 and y <= 5 and y <= sqrt(-x + 8)):
		return True
	return False

def drawPoint(x, y, color):	
	x = x * 40			# масштабирование
	y = y * 40
	print "drawing point: (%f, %f)" % (x, y)
	x_p = 20 + x
	y_p = height - 20 - y
	c.create_rectangle(x_p, y_p, x_p, y_p, outline=color)

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
h = 0.5

c = Canvas(root, height=height, width=width)
c.create_line(20, height - 20, width - 20, height - 20)
c.create_line(20, height - 20, 20, 20)
c.pack()

x = 0.0
y = 0.0
while (y <= max_y):
	x = 0.0
	while (x <= max_x):
		drawPoint(x, y, "red")
		x = x + h
	y = y + h

drawBounds()

drawPoint(0, 5, "green")
mainloop()