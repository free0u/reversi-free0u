#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import time
import random
import sys

	
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
		AAA(self)

def rus(s):
	return unicode(s, 'cp1251')
	
def currentPlayer():
	global label
	global player
	if player:
		str = rus("’од€т белые")
	else:
		str = rus("<font size=4>’од€т черные</font>")
	label.setText(str)
		
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
# 0 - черна€ фишка
# 1 - бела€ фишка

def createFishki():
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
			fish.append(f)
			
			# черные
			f = Fishka("white")
			scene.addItem(f)
			f.setPos(x,y)
			fish.append(f)
			
			row.append(fish)
		fishki.append(row)	
		
def newGame():
	# обнул€ем поле
	global pole
	global scene
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
	reloadPole()
		
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
	


app = QtGui.QApplication(sys.argv)

scene = QtGui.QGraphicsScene()
scene.setSceneRect(0, 0, 512, 512)
gamepole = QtGui.QGraphicsView(scene)

newgamebutton = QtGui.QPushButton(rus("Ќова€ игра"))
QtCore.QObject.connect(newgamebutton, QtCore.SIGNAL("clicked()"), newGame)
closebutton = QtGui.QPushButton(rus("¬ыйти"))
QtCore.QObject.connect(closebutton, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()"))

# 0 - ход€т черные
# 1 - ход€т белые
player = 0

label = QtGui.QLabel()
currentPlayer()
hbox = QtGui.QHBoxLayout()
hbox.addWidget(newgamebutton)
hbox.addWidget(closebutton)
hbox.addWidget(label)
hbox.addStretch(1)

vbox = QtGui.QVBoxLayout()
vbox.addLayout(hbox)
vbox.addWidget(gamepole)
vbox.addStretch(1)

window = QtGui.QWidget()
window.setLayout(vbox)
window.setWindowTitle(u"Reversi")
window.show()


newKletki()

# 0 - ход€т черные
# 1 - ход€т белые
player = 0

fishki = []
createFishki()

pole = []
newGame()




sys.exit(app.exec_())






