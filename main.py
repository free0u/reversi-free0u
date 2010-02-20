# -*- coding: UTF-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import time
import random

app = QtGui.QApplication(sys.argv)

scene = QtGui.QGraphicsScene()
scene.setSceneRect(0, 0, 512, 512)
	
class Kletka(QtGui.QGraphicsPixmapItem):
	def __init__(self):
		QtGui.QGraphicsPixmapItem.__init__(self)
		x = QtGui.QPixmap()
		x.load("kletka.jpg")			
		self.setPixmap(x)
	def mousePressEvent(self, event):
		Pressed(self.x(), self.y())
		
class Fishka(QtGui.QGraphicsPixmapItem):
	def __init__(self,colour):
		QtGui.QGraphicsPixmapItem.__init__(self)
		x = QtGui.QPixmap()
		x.load(colour + ".jpg")			
		self.setPixmap(x)
	def mousePressEvent(self, event):
		Pressed(self.x(), self.y())
		#AAA(self)

def AAA(node):
	node.hide()
	
def newKletki():
	global scene
	for i in range(8):
		for j in range(8):
			x = j * 64
			y = i * 64
			newk = Kletka()
			scene.addItem(newk)			
			newk.setPos(x, y)

			
# -1 - пустое поле	
# 0 - черная фишка
# 1 - белая фишка
def newGame():
	# обнуляем поле (убираем фишки)
	global pole
	pole = [
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1, 0, 1,-1,-1,-1],
			[-1,-1,-1, 1, 0,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
		]
		
	#создаем все фишки
	global scene
	global fishki
	for i in range(8):
		row = []
		for j in range(8):
			x = j * 64
			y = i * 64
			fish = []
			
			# белые
			f = Fishka("black")
			scene.addItem(f)
			f.setPos(x,y)
			f.hide()
			fish.append(f)
			
			# черные
			f = Fishka("white")
			scene.addItem(f)
			f.setPos(x,y)
			f.hide()
			fish.append(f)
			
			row.append(fish)
		fishki.append(row)	
		
def reloadPole():
	global scene
	global pole
	for row in range(8):
		for col in range(8):
			fishki[row][col][0].hide()
			fishki[row][col][1].hide()
			if pole[row][col] == 0:
				fishki[row][col][0].show()
			elif pole[row][col] == 1:
				fishki[row][col][1].show()

def Pressed(x,y):
	row = int(y / 64)
	col = int(x / 64)
	global pole
	
				
newKletki()

# 0 - ходят черные
# 1 - ходят белые
player = 0

pole = []
fishki = []
newGame()
reloadPole()



view = QtGui.QGraphicsView(scene)
view.setWindowTitle("Reversi")
view.show()

sys.exit(app.exec_())
