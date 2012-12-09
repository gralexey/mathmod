# -*- coding: utf8 -*-

from Tkinter import *
from math import sqrt
from numpy import linalg
from time import sleep

def validatePoint(x, y):		# возвращает true, если точка принадлежит области, определенной неравенствами 
	if (y <= x and y >= 0 and y <= -x + 16.1):
		return True
	return False

def drawPoint(x, y, color):	
	x = x * scale_k			# масштабирование
	y = y * scale_k
	x_p = 20 + x
	y_p = height - 20 - y	
	c.create_rectangle(x_p, y_p, x_p, y_p, outline=color)

def drawCircle(x, y, temperature, color):	
	x = x * scale_k			# масштабирование
	y = y * scale_k
	x_p = 20 + x
	y_p = height - 20 - y
	#color = "#%06x" % int(temperature * (16711680 - 255) / (200 - 0) + 255)
	#color = color[:3] + "00" + color[5:]
	#radius = h * 10
	radius = temperature * h * 35 / 200
	c.create_rectangle(x_p - radius, y_p - radius, x_p + radius, y_p + radius, fill=color, width=0)

def drawBoldPoint(x, y, color):	
	x = x * scale_k			# масштабирование
	y = y * scale_k
	x_p = 20 + x
	y_p = height - 20 - y
	c.create_rectangle(x_p - 3, y_p - 3, x_p +3 , y_p + 3, outline=color, fill=color)

def drawBounds():				# рисуем границы для рабочего прямоугольника (0, 0, max_x, max_y) и координатные оси
	x = 0.0
	while (x <= max_x):
		drawPoint(x, max_y, "green")
		x = x + 0.1
	y = 0.0
	while (y <= max_y):
		drawPoint(max_x, y, "green")
		y = y + 0.1
	c.create_line(20, height - 20, width - 20, height - 20)
	c.create_line(20, height - 20, 20, 20)

def printMatrix(a, b):
	idx = 0
	for row in a:
		print row, b[idx]
		idx += 1

temperatureIn_t_idx = {}
def defineTopCondiments():
	# задаем граничные условия с верхней стороны фигуры
	x = 0.0
	y = max_y
	while (x <= max_x):
		y = max_y
		while (y >= 0):
			if validatePoint(x, y):
				t_border = xyt_dict[x, y]
				global temperatureIn_t_idx
				temperatureIn_t_idx[t_border] = 100
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
				global temperatureIn_t_idx
				temperatureIn_t_idx[t_border] = 50
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
				global temperatureIn_t_idx
				temperatureIn_t_idx[t_border] = 100
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
				global temperatureIn_t_idx
				temperatureIn_t_idx[t_border] = 200
				break						
			x = round(x + h, hr)
		y = round(y + h, hr)

root = Tk()
root.title('Model')

# настройки
height = 650
width = 1000
max_x = 16			# определяет рабочий прямоугольник для работы (0, 0, max_x, max_y)
max_y = 8
h = 0.2
hr = 2 				# шаг для округления погрешности сложения (втф!!!)
ht = 1.0			# шаг времени
a = 1.0				# коэффициенты дифференциального уравнения
b = 1.0				
scale_k = 60

c = Canvas(root, height=height, width=width)
c.pack()
drawBounds()


def getColorByScalar(temperature):	
	#temperature = (temperature - 50) * 2
	#temperature = temperature * 0.66 + 33				# для сужения цветового диапазона
	temperature = int(temperature)
	if temperature == 100:
		temperature	-= 1
	interval = temperature / 34														# номер интервала из цветовой шкалы: при изменении "температуры" от 0 до 100, мы прходим интервалы #00ffff - #00ff00 - #ffff00 - #ff0000							
	offsetFromInterval = temperature - interval * 33								# смещение от начала интервала
	color = "#00ffff"
	if interval == 0:
		color = "#00ff%02x" % (255 - offsetFromInterval * 255 / 33)
	if interval == 1:
		color = "#%02xff00" % (offsetFromInterval * 255 / 33 - 7)
	if interval == 2:
		color = "#ff%02x00" % (255 - offsetFromInterval * 255 / 33)
	return color

#for i in range(100):			# вывести цветовую гамму
#	x1 = i * 5
#	x2 = i * 5 + 5
#	color = getColorByScalar(i)
#	c.create_rectangle(x1 + 50, 30, x2 + 50, 50, fill=color, width=0)

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
tOfCurrentIterations = [0.0] * n 		# 0.0 — начальная температура во всех точках
tStore = []
tStore.append(tOfCurrentIterations)
#print tStore

def doLoop():
	time = 0.0
	iteration_n = 0     # номер итерации (как time, только целое число)
	while (time <= 25):
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
					T[rowCount][t_left] = -(a*ht) 			# тут задаем коэффициенты из разностного уравнения
					T[rowCount][t_current] = h**2 + 2*a*ht + 2*b*ht
					T[rowCount][t_right] = -(a*ht)
					T[rowCount][t_bottom] = -(b*ht)
					T[rowCount][t_top] = -(b*ht)
					F[rowCount] = h**2 * tStore[iteration_n][t_current]
					rowCount += 1
				x = round(x + h, hr)
			y = round(y + h, hr)

		#defineRightCondiments()
		defineBottomCondiments()
		defineTopCondiments()
		#defineLeftCondiments()

		# задаем граничные температуры точек в матрице 
		for idx in temperatureIn_t_idx:
			T[rowCount][idx] = 1
			F[rowCount] = temperatureIn_t_idx[idx]
			rowCount += 1

		t = linalg.solve(T, F)		# t содержит значения температур элементов (последовательно)
		tStore.append(t)

		c.delete(ALL)
		drawBounds()
		xyts = xyt_dict.items()
		for xyt in xyts:
			pointXY = xyt[0]	
			t_Idx = xyt[1]	
			tOfPoint = t[t_Idx]
			tOfPoint = (tOfPoint - 50) * 2
			drawCircle(pointXY[0], pointXY[1], scale_k * 2 + 40, getColorByScalar(tOfPoint))

		time += ht
		#print iteration_n, " finished"
		#sleep(0.1)
		root.update()
		#print tStore[iteration_n], " ", iteration_n, " finished"		
		iteration_n += 1

#	for i in range(10):							# эксперимент с индикацией температуры в точке
#		drawCircle(10, i/2.0, i/0.8, "brown")

goButton = Button (root, text="Modulate", command=doLoop)
goButton.pack()

mainloop()