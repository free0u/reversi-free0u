# -*- coding: UTF-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import random
import math
import time
	
class Square(QtGui.QGraphicsItem):
	def __init__(self):
		QtGui.QGraphicsItem.__init__(self)

	def boundingRect(self):
		return QtCore.QRectF(0, 0, 64, 64)
	
	def paint(self, painter, option, widget):
		gradient = QtGui.QRadialGradient()
		c = QtGui.QColor(195,195,195,255)
		gradient.setColorAt(0, c)
		gradient.setColorAt(1, c)
		painter.setBrush(QtGui.QBrush(gradient))
		painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
		painter.drawRect(0, 0, 64, 64)			
		
	def mousePressEvent(self, event):
		pressed(self.x(), self.y())
		
class Chip(QtGui.QGraphicsItem):
	def __init__(self):
		QtGui.QGraphicsItem.__init__(self)
	colour = 0	
	def boundingRect(self):
		return QtCore.QRectF(6, 6, 52, 52)
	
	def paint(self, painter, option, widget):
		gradient = QtGui.QRadialGradient()
		if self.colour == 0: # black
			gradient.setColorAt(0, QtCore.Qt.black)
			gradient.setColorAt(1, QtCore.Qt.black)
		else: # white
			gradient.setColorAt(0, QtCore.Qt.white)
			gradient.setColorAt(1, QtCore.Qt.white)
		painter.setBrush(QtGui.QBrush(gradient))
		painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
		painter.drawEllipse(6, 6, 52, 52)		
	def mousePressEvent(self, event):
		pressed(self.x(), self.y())

class Window(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setWindowTitle(u"Reversi")
		
		# ������ ����� ����
		button1 = QtGui.QPushButton(rus("����� ����"))
		QtCore.QObject.connect(button1, QtCore.SIGNAL("clicked()"), newGame)
		
		# ������ ��������
		button2 = QtGui.QPushButton(rus("�����"))
		QtCore.QObject.connect(button2, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()"))
		
		# �����, ��� �����. �������� �����, ��� �������
		self.label = QtGui.QLabel()
		
		# ������� ����
		self.scene = QtGui.QGraphicsScene()
		self.scene.setSceneRect(0, 0, 512, 512)
		
		# ������ �������� ����
		gamearea = QtGui.QGraphicsView(self.scene)
		gamearea.setRenderHint(QtGui.QPainter.Antialiasing)
		# ������� (������)
		hlabel = []
		for i in range(8):
			c = QtGui.QLabel()
			c.setText(chr(ord('a') + i))
			hlabel.append(c)
		
		# ������� (������)
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
		grid.addWidget(gamearea)
		
		self.setLayout(grid)

def win():
	b = getScore(0)
	w = getScore(1)
	global window
	global app
	if b == w:
		text = rus("�����.")
	elif b > w:
		text = rus("�������� <b>������</b>. ���� " + str(b) + ":" + str(w))
	else:
		text = rus("�������� <b>�����</b>. ���� " + str(w) + ":" + str(b))
	
	QtGui.QMessageBox.information(window, rus("���� ���������!"), "<center>" + text + "</center>", QtGui.QMessageBox.Ok)

	newGame()
		
def rus(s):
	return unicode(s, 'cp1251')
	
def currentPlayer():
	global player
	global window
	if player:
		window.label.setText(rus("<center><font size=4>����� <b>�����</b></font></center>"))
	else:
		window.label.setText(rus("<center><font size=4>����� <b>������</b></font></center>"))
	
def getScore(p):
	score = 0
	global area
	for i in range(8):
		for j in range(8):
			if area[i][j] == p:
				score = score + 1
	return score
	
def AAA(node):
	node.hide()
	
def newKletki(scene):
	for i in range(8):
		for j in range(8):
			x = j * 64
			y = i * 64
			newS = Square()
			scene.addItem(newS)
			newS.setPos(x, y)

			
# -1 - ������ ����	
# 0 - ������ �����
# 1 - ����� �����

def createFishki(scene):
	#������� ��� �����
	global fishki
	for i in range(8):
		row = []
		for j in range(8):
			x = j * 64
			y = i * 64
			fish = []
			
			# black
			f = Chip()
			f.colour = 0 
			scene.addItem(f)
			f.setPos(x,y)
			fish.append(f)
			
			# white
			f = Chip()
			f.colour = 1
			scene.addItem(f)
			f.setPos(x,y)
			fish.append(f)
			
			row.append(fish)
		fishki.append(row)	
		
def newGame():
	# �������� ����
	global area
	global player
	player = 0
	currentPlayer()
	area = [
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
	reloadArea()
	
def delay():
	#x = 2 ** 100000
	time.sleep(1)
		
def reloadArea():
	global area
	for row in range(8):
		for col in range(8):
			fishki[row][col][0].hide()
			fishki[row][col][1].hide()
			if area[row][col] == 0:
				fishki[row][col][0].show()
			elif area[row][col] == 1:
				fishki[row][col][1].show()

def rev(c):
	if c == 0:
		return 1
	else:
		return 0

def step(player, row, col, dir, act = 0):
	global area
	me = player
	opp = rev(player)
	# ���� ������ ������
	if area[row][col] == -1:
		if (dir == "u") & (row != 0): # �����
			kol = 0
			m = row - 1
			change = 0			
			while (area[m][col] == opp) & (m >= 0):
				m = m - 1
				change = 1	
				kol = kol + 1			
			# ����� �� �������?
			if (area[m][col] == me) & (change):
				
				# ���� ��������� �������
				if act:
					m = row - 1
					while (area[m][col] == opp) & (m >= 0):
						area[m][col] = rev(area[m][col])
						m = m - 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "d") & (row != 7): # ����
			kol = 0
			m = row + 1
			change = 0			
			while (area[m][col] == opp) & (m <= 7):
				m = m + 1
				change = 1	
				kol = kol + 1
			# ����� �� �������?
			if (area[m][col] == me) & (change):
				
				# ���� ��������� �������
				if act:
					m = row + 1
					while (area[m][col] == opp) & (m <= 7):
						area[m][col] = rev(area[m][col])
						m = m + 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "l") & (col != 0): # �����
			kol = 0
			n = col - 1
			change = 0			
			while (area[row][n] == opp) & (n >= 0):
				n = n - 1
				change = 1
				kol = kol + 1
			# ����� �� �������?
			if (area[row][n] == me) & (change):
				
				# ���� ��������� �������
				if act:
					n = col - 1
					while (area[row][n] == opp) & (n >= 0):
						area[row][n] = rev(area[row][n])
						n = n - 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "r") & (col != 7): # ������
			kol = 0
			n = col + 1
			change = 0			
			while (n <= 7) & (area[row][n] == opp):
				n = n + 1
				change = 1	
				kol = kol + 1
			# ����� �� �������?
			if (area[row][n] == me) & (change):
				
				# ���� ��������� �������
				if act:
					n = col + 1
					while (area[row][n] == opp) & (n <= 7):
						area[row][n] = rev(area[row][n])
						n = n + 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "ur") & (row != 0) & (col != 7): # �����-������
			kol = 0
			m = row - 1
			n = col + 1
			change = 0			
			while (area[m][n] == opp) & (m >= 0) & (n <= 7):
				m = m - 1
				n = n + 1
				change = 1	
				kol = kol + 1
			# ����� �� �������?
			if (area[m][n] == me) & (change):
				
				# ���� ��������� �������
				if act:
					m = row - 1
					n = col + 1
					while (area[m][n] == opp) & (m >= 0) & (n <= 7):
						area[m][n] = rev(area[m][n])
						m = m - 1
						n = n + 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "ul") & (row != 0) & (col != 0): # �����-�����
			kol = 0
			m = row - 1
			n = col - 1
			change = 0		
			
			while (area[m][n] == opp) & (m >= 0) & (n >= 0):
				m = m - 1
				n = n - 1
				change = 1	
				kol = kol + 1
			# ����� �� �������?
			if (area[m][n] == me) & (change):
				
				# ���� ��������� �������
				if act:
					m = row - 1
					n = col - 1
					while (area[m][n] == opp) & (m >= 0) & (n >= 0):
						area[m][n] = rev(area[m][n])
						m = m - 1
						n = n - 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "dr") & (row != 7) & (col != 7): # ����-������
			kol = 0
			m = row + 1
			n = col + 1
			change = 0			
			while (area[m][n] == opp) & (m <= 7) & (n <= 7):
				m = m + 1
				n = n + 1
				change = 1	
				kol = kol + 1
			# ����� �� �������?
			if (area[m][n] == me) & (change):
				
				# ���� ��������� �������
				if act:
					m = row + 1
					n = col + 1
					while (area[m][n] == opp) & (m <= 7) & (n <= 7):
						area[m][n] = rev(area[m][n])
						m = m + 1
						n = n + 1
				# ���� ������ �� ���������
				else:
					return kol
		elif (dir == "dl") & (row != 7) & (col != 0): # ����-�����
			kol = 0
			m = row + 1
			n = col - 1
			change = 0	
			while (area[m][n] == opp) & (m <= 7) & (n >= 0):
				m = m + 1
				n = n - 1
				change = 1	
				kol = kol + 1
			# ����� �� �������?
			if (area[m][n] == me) & (change):
				
				# ���� ��������� �������
				if act:					
					m = row + 1
					n = col - 1
					while (area[m][n] == opp) & (m <= 7) & (n >= 0):
						area[m][n] = rev(area[m][n])
						m = m + 1
						n = n - 1
				# ���� ������ �� ���������
				else:
					return kol
	return 0
def eated(row, col, player):
	global area
	if area[row][col] != -1:
		return 255
	else:
		kol = 0
		kol = kol + step(player, row, col, "u")
		kol = kol + step(player, row, col, "d")
		kol = kol + step(player, row, col, "l")
		kol = kol + step(player, row, col, "r")
		kol = kol + step(player, row, col, "ur")
		kol = kol + step(player, row, col, "ul")
		kol = kol + step(player, row, col, "dr")
		kol = kol + step(player, row, col, "dl")
		return kol
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
	
def makeStep(player, row, col):
	if step(player, row, col, "u"):
		step(player, row, col, "u", 1)
	if step(player, row, col, "d"):
		step(player, row, col, "d", 1)
	if step(player, row, col, "l"):
		step(player, row, col, "l", 1)
	if step(player, row, col, "r"):
		step(player, row, col, "r", 1)
	if step(player, row, col, "ul"):
		step(player, row, col, "ul", 1)
	if step(player, row, col, "ur"):
		step(player, row, col, "ur", 1)
	if step(player, row, col, "dl"):
		step(player, row, col, "dl", 1)
	if step(player, row, col, "dr"):
		step(player, row, col, "dr", 1)
	
def pressed(x,y):
	row = int(y / 64)
	col = int(x / 64)
	go = 0
	global player
	
	# �����
	if step(player, row, col, "u"):
		step(player, row, col, "u", 1)
		go = 1
		
	# ����
	if step(player, row, col, "d"):
		step(player, row, col, "d", 1)
		go = 1
		
	# �����
	if step(player, row, col, "l"):
		step(player, row, col, "l", 1)
		go = 1
		
	# ������
	if step(player, row, col, "r"):
		step(player, row, col, "r", 1)
		go = 1
		
	# �����-�����
	if step(player, row, col, "ul"):
		step(player, row, col, "ul", 1)
		go = 1
		
	# �����-������
	if step(player, row, col, "ur"):
		step(player, row, col, "ur", 1)
		go = 1
		
	# ����-�����
	if step(player, row, col, "dl"):
		step(player, row, col, "dl", 1)
		go = 1
		
	# ����-������
	if step(player, row, col, "dr"):
		step(player, row, col, "dr", 1)
		go = 1
	
	if go:
		area[row][col] = player
		if canStep(rev(player)):
			player = rev(player)
			currentPlayer()	
		reloadArea()
	
	if player == 1:
		compStep(player)
		player = rev(player)
		currentPlayer()	
		reloadArea()
	if (not canStep(rev(player))) & (not canStep(player)):
		win()
	
def compStep(player):
	table = [
				[1, 8, 2, 2, 2, 2, 8, 1],
				[8, 8, 6, 5, 5, 6, 8, 8],
				[2, 6, 4, 3, 3, 4, 6, 2],
				[2, 5, 3, 1, 1, 3, 5, 2],
				[2, 5, 3, 1, 1, 3, 5, 2],
				[2, 6, 4, 3, 3, 4, 6, 2],
				[8, 8, 6, 5, 5, 6, 8, 8],
				[1, 8, 2, 2, 2, 2, 8, 1]
			]
	pX = [0] * 61
	pY = [0] * 61
	minE = 9
	maxE = 0
	NP = 0
	for row in range(8):
		for col in range(8):
			E = eated(row, col, player)
			if (minE > table[row][col]) & (E < 255) & (E > 0):
				minE = table[row][col]
				NP = 0
				maxE = 0
			if (minE == table[row][col]) & (E < 255):
				if E > maxE:
					maxE = E
					NP = 1
					pX[NP] = row
					pY[NP] = col
				elif E == maxE:
					NP = NP + 1
					pX[NP] = row
					pY[NP] = col
	E = math.trunc(random.random() * NP) + 1
	E = 1
	# print pX[E], pY[E]
	makeStep(player, pX[E], pY[E])	
	area[pX[E]][pY[E]] = player
	
app = QtGui.QApplication(sys.argv)

# 0 - ����� ������, 1 -  �����
player = 0
fishki = []
area = []

window = Window()
window.show()

newKletki(window.scene)
createFishki(window.scene)
newGame()

sys.exit(app.exec_())


