import sys
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)

scene = QtGui.QGraphicsScene()
scene.setSceneRect(-200, -200, 400, 400)
i = 0
def AAA():
	global i
	i = i + 1
	print i

class Pic(QtGui.QGraphicsItem):
	
	def boundingRect(self):
		return QtCore.QRectF(-50, -50, 100, 100)
	def paint(self, painter, option, widget):
		painter.drawRect(-50, -50, 100, 100)
	def mousePressEvent(self, event):
		AAA()
	


node = Pic()
#node.setPos(-50, 50)
scene.addItem(node)


view = QtGui.QGraphicsView(scene)
view.show()


sys.exit(app.exec_())
