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
		#AAA(self)

def rus(s):
	return unicode(s, 'cp1251')
	
def currentPlayer():
	global label
	global player
	if player:
		str = rus("<center><font size=4>Ходят <b>белые</b></font></center>")
	else:
		str = rus("<center><font size=4>Ходят <b>черные</b></font></center>")
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
# 0 - черная фишка
# 1 - белая фишка

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
	# обнуляем поле
	global pole
	global scene
	global player
	player = 0
	pole = [
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1, 1, 0,-1,-1,-1],
			[-1,-1,-1, 1, 0,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1],
		]
	reloadPole()
	currentPlayer()
		
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

def rev(c):
	if c == 0:
		return 1
	else:
		return 0
				
def Pressed(x,y):
	row = int(y / 64)
	col = int(x / 64)
	global pole
	global player
	me = player
	opp = rev(player)
	step = 0
	if pole[row][col] == -1:
		
		# вверх
		m = row - 1
		change = 0
		# надо ли переворачивать?
		while (pole[m][col] == opp) & (m >= 0):
			m = m - 1
			change = 1
		# ага, надо
		if (pole[m][col] == me) & (change):
			pole[row][col] = me
			m = row - 1
			while (pole[m][col] == opp) & (m >= 0):
				pole[m][col] = rev(pole[m][col])
				m = m - 1
			step = 1
		
		# вниз
		m = row + 1
		change = 0
		# надо ли переворачивать?
		while (pole[m][col] == opp) & (m <= 7):
			m = m + 1
			change = 1
		# ага, надо
		if (pole[m][col] == me) & (change):
			pole[row][col] = me
			m = row + 1
			while (pole[m][col] == opp) & (m <= 7):
				pole[m][col] = rev(pole[m][col])
				m = m + 1
			step = 1
			
		# вправо
		n = col + 1
		change = 0
		# надо ли переворачивать?
		while (pole[row][n] == opp) & (n <= 7):
			n = n + 1
			change = 1
		# ага, надо
		if (pole[row][n] == me) & (change):
			pole[row][col] = me
			n = col + 1
			while (pole[row][n] == opp) & (n <= 7):
				pole[row][n] = rev(pole[row][n])
				n = n + 1
			step = 1

		# влево
		n = col - 1
		change = 0
		# надо ли переворачивать?
		while (pole[row][n] == opp) & (n >= 0):
			n = n - 1
			change = 1
		# ага, надо
		if (pole[row][n] == me) & (change):
			pole[row][col] = me
			n = col - 1
			while (pole[row][n] == opp) & (n >= 0):
				pole[row][n] = rev(pole[row][n])
				n = n - 1
			step = 1

		# вверх-вправо
		m = row - 1
		n = col + 1
		change = 0
		# надо ли переворачивать?
		while (pole[m][n] == opp) & (m >= 0) & (n >= 0):
			m = m - 1
			n = n + 1
			change = 1
		# ага, надо
		if (pole[m][n] == me) & (change):
			pole[row][col] = me
			m = row - 1
			n = col + 1
			while (pole[m][n] == opp) & (m >= 0) & (n >= 0):
				pole[m][n] = rev(pole[m][n])
				m = m -1
				n = n + 1
			step = 1

		# вверх-влево
		# вниз-вправо
		# вниз-влево
		pass
	if step:
		player = rev(player)
		currentPlayer()
		reloadPole()


app = QtGui.QApplication(sys.argv)

scene = QtGui.QGraphicsScene()
scene.setSceneRect(0, 0, 512, 512)
gamepole = QtGui.QGraphicsView(scene)

newgamebutton = QtGui.QPushButton(rus("Новая игра"))
QtCore.QObject.connect(newgamebutton, QtCore.SIGNAL("clicked()"), newGame)
closebutton = QtGui.QPushButton(rus("Выйти"))
QtCore.QObject.connect(closebutton, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()"))

label = QtGui.QLabel()

hbox = QtGui.QHBoxLayout()
hbox.addWidget(newgamebutton)
hbox.addWidget(closebutton)
hbox.addWidget(label)
#hbox.addStretch(1)

vbox = QtGui.QVBoxLayout()
vbox.addLayout(hbox)
vbox.addWidget(gamepole)
vbox.addStretch(100)

window = QtGui.QWidget()
window.setLayout(vbox)
window.setWindowTitle(u"Reversi")
window.show()

newKletki()

# 0 - ходят черные
# 1 - ходят белые
player = 0

fishki = []
createFishki()

pole = []
newGame()

sys.exit(app.exec_())


