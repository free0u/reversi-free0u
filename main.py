# -*- coding: UTF-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import random

	
class Kletka(QtGui.QGraphicsPixmapItem):
	def __init__(self):
		QtGui.QGraphicsPixmapItem.__init__(self)
		x = QtGui.QPixmap()
		x.load("kletka.jpg")			
		self.setPixmap(x)
	def mousePressEvent(self, event):
		pressed(self.x(), self.y())
		
class Fishka(QtGui.QGraphicsPixmapItem):
	def __init__(self,colour):
		QtGui.QGraphicsPixmapItem.__init__(self)
		x = QtGui.QPixmap()
		x.load(colour + ".jpg")			
		self.setPixmap(x)
	def mousePressEvent(self, event):
		pressed(self.x(), self.y())

class Window(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setWindowTitle(u"Reversi")
		
		# кнопка новая игра
		button1 = QtGui.QPushButton(rus("Новая игра"))
		QtCore.QObject.connect(button1, QtCore.SIGNAL("clicked()"), newGame)
		
		# кнопка закрытия
		button2 = QtGui.QPushButton(rus("Выйти"))
		QtCore.QObject.connect(button2, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()"))
		
		# метка, кто ходит. доступна извне, как атрибут
		self.label = QtGui.QLabel()
		
		# игровое поле
		self.scene = QtGui.QGraphicsScene()
		self.scene.setSceneRect(0, 0, 512, 512)
		
		# виджет игрового поля
		gamepole = QtGui.QGraphicsView(self.scene)
		
		# буковки (список)
		hlabel = []
		for i in range(8):
			c = QtGui.QLabel()
			c.setText(chr(ord('a') + i))
			hlabel.append(c)
		
		# циферки (список)
		vlabel = []
		for i in reversed(range(8)):
			c = QtGui.QLabel()
			c.setText(str(i + 1))
			vlabel.append(c)
			
		headbar = QtGui.QHBoxLayout()
		headbar.addWidget(button1)
		headbar.addWidget(button2)
		headbar.addWidget(self.label)
		
		grid = QtGui.QVBoxLayout()
		grid.addLayout(headbar)
		grid.addWidget(gamepole)
		
		self.setLayout(grid)

def win():
	b = getScore(0)
	w = getScore(1)
	global window
	global app
	if b == w:
		text = rus("Ничья.")
	elif b > w:
		text = rus("Победили <b>черные</b>. Счет " + str(b) + ":" + str(w))
	else:
		text = rus("Победили <b>белые</b>. Счет " + str(w) + ":" + str(b))
	
	QtGui.QMessageBox.information(window, rus("Игра закончена!"), "<center>" + text + "</center>", QtGui.QMessageBox.Ok)

	newGame()
		
def rus(s):
	return unicode(s, 'cp1251')
	
def currentPlayer():
	global player
	global window
	if player:
		window.label.setText(rus("<center><font size=4>Ходят <b>белые</b></font></center>"))
	else:
		window.label.setText(rus("<center><font size=4>Ходят <b>черные</b></font></center>"))
	
def getScore(p):
	score = 0
	global pole
	for i in range(8):
		for j in range(8):
			if pole[i][j] == p:
				score = score + 1
	return score
	
def AAA(node):
	node.hide()
	
def newKletki(scene):
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

def createFishki(scene):
	#создаем все фишки
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
	global player
	player = 0
	currentPlayer()
	pole = [
			[-1,-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1, 0, 1,-1,-1,-1,-1],
			[-1,-1,-1, 1, 0,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1,-1],
			[-1,-1,-1,-1,-1,-1,-1,-1,-1]
		]
	reloadPole()
	
		
def reloadPole():
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

def step(player, row, col, dir, act = 0):
	global pole
	me = player
	opp = rev(player)
	
	# если клетка пустая
	if pole[row][col] == -1:
		if (dir == "u") & (row != 0): # вверх
			m = row - 1
			change = 0			
			while (pole[m][col] == opp) & (m >= 0):
				m = m - 1
				change = 1			
			# можно ли сходить?
			if (pole[m][col] == me) & (change):
				# если требуется сходить
				if act:
					m = row - 1
					while (pole[m][col] == opp) & (m >= 0):
						pole[m][col] = rev(pole[m][col])
						m = m - 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "d") & (row != 7): # вниз
			m = row + 1
			change = 0			
			while (pole[m][col] == opp) & (m <= 7):
				m = m + 1
				change = 1			
			# можно ли сходить?
			if (pole[m][col] == me) & (change):
				# если требуется сходить
				if act:
					m = row + 1
					while (pole[m][col] == opp) & (m <= 7):
						pole[m][col] = rev(pole[m][col])
						m = m + 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "l") & (col != 0): # влево
			n = col - 1
			change = 0			
			while (pole[row][n] == opp) & (n >= 0):
				n = n - 1
				change = 1			
			# можно ли сходить?
			if (pole[row][n] == me) & (change):
				# если требуется сходить
				if act:
					n = col - 1
					while (pole[row][n] == opp) & (n >= 0):
						pole[row][n] = rev(pole[row][n])
						n = n - 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "r") & (col != 7): # вправо
			n = col + 1
			change = 0			
			while (n <= 7) & (pole[row][n] == opp):
				n = n + 1
				change = 1			
			# можно ли сходить?
			if (pole[row][n] == me) & (change):
				# если требуется сходить
				if act:
					n = col + 1
					while (pole[row][n] == opp) & (n <= 7):
						pole[row][n] = rev(pole[row][n])
						n = n + 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "ur") & (row != 0) & (col != 7): # вверх-вправо
			m = row - 1
			n = col + 1
			change = 0			
			while (pole[m][n] == opp) & (m >= 0) & (n <= 7):
				m = m - 1
				n = n + 1
				change = 1			
			# можно ли сходить?
			if (pole[m][n] == me) & (change):
				# если требуется сходить
				if act:
					m = row - 1
					n = col + 1
					while (pole[m][n] == opp) & (m >= 0) & (n <= 7):
						pole[m][n] = rev(pole[m][n])
						m = m - 1
						n = n + 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "ul") & (row != 0) & (col != 0): # вверх-влево
			m = row - 1
			n = col - 1
			change = 0		
			
			while (pole[m][n] == opp) & (m >= 0) & (n >= 0):
				m = m - 1
				n = n - 1
				change = 1		
			# можно ли сходить?
			if (pole[m][n] == me) & (change):
				# если требуется сходить
				if act:
					m = row - 1
					n = col - 1
					while (pole[m][n] == opp) & (m >= 0) & (n >= 0):
						pole[m][n] = rev(pole[m][n])
						m = m - 1
						n = n - 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "dr") & (row != 7) & (col != 7): # вниз-вправо
			m = row + 1
			n = col + 1
			change = 0			
			while (pole[m][n] == opp) & (m <= 7) & (n <= 7):
				m = m + 1
				n = n + 1
				change = 1			
			# можно ли сходить?
			if (pole[m][n] == me) & (change):
				# если требуется сходить
				if act:
					m = row + 1
					n = col + 1
					while (pole[m][n] == opp) & (m <= 7) & (n <= 7):
						pole[m][n] = rev(pole[m][n])
						m = m + 1
						n = n + 1
				# если ходить не требуется
				else:
					return 1
		elif (dir == "dl") & (row != 7) & (col != 0): # вниз-влево
			m = row + 1
			n = col - 1
			change = 0	
			while (pole[m][n] == opp) & (m <= 7) & (n >= 0):
				m = m + 1
				n = n - 1
				change = 1			
			# можно ли сходить?
			if (pole[m][n] == me) & (change):
				# если требуется сходить
				if act:					
					m = row + 1
					n = col - 1
					while (pole[m][n] == opp) & (m <= 7) & (n >= 0):
						pole[m][n] = rev(pole[m][n])
						m = m + 1
						n = n - 1
				# если ходить не требуется
				else:
					return 1
			
	return 0
		
def canStep(p):
	for row in range(8):
		for col in range(8):
			if step(p, row, col, "u"):
				return 1
			elif step(p, row, col, "d"):
				return 1
			elif step(p, row, col, "l"):
				return 1
			elif step(p, row, col, "r"):
				return 1
			elif step(p, row, col, "ul"):
				return 1
			elif step(p, row, col, "ur"):
				return 1
			elif step(p, row, col, "dl"):
				return 1
			elif step(p, row, col, "dr"):
				return 1
	return 0
		
def pressed(x,y):
	row = int(y / 64)
	col = int(x / 64)
	go = 0
	global player
	
	# вверх
	if step(player, row, col, "u"):
		step(player, row, col, "u", 1)
		go = 1
		
	# вниз
	if step(player, row, col, "d"):
		step(player, row, col, "d", 1)
		go = 1
		
	# влево
	if step(player, row, col, "l"):
		step(player, row, col, "l", 1)
		go = 1
		
	# вправо
	if step(player, row, col, "r"):
		step(player, row, col, "r", 1)
		go = 1
		
	# вверх-влево
	if step(player, row, col, "ul"):
		step(player, row, col, "ul", 1)
		go = 1
		
	# вверх-вправо
	if step(player, row, col, "ur"):
		step(player, row, col, "ur", 1)
		go = 1
		
	# вниз-влево
	if step(player, row, col, "dl"):
		step(player, row, col, "dl", 1)
		go = 1
		
	# вниз-вправо
	if step(player, row, col, "dr"):
		step(player, row, col, "dr", 1)
		go = 1
	
	if go:
		pole[row][col] = player
		if canStep(rev(player)):
			player = rev(player)
			currentPlayer()	
	reloadPole()

	if (not canStep(rev(player))) & (not canStep(player)):
		win()
	
app = QtGui.QApplication(sys.argv)

# 0 - ходят черные, 1 -  белые
player = 1
fishki = []
pole = []

window = Window()
window.show()

newKletki(window.scene)
createFishki(window.scene)
newGame()

sys.exit(app.exec_())


