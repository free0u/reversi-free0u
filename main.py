import sys
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)

scene = QtGui.QGraphicsScene()
scene.setSceneRect(-200, -200, 400, 400)

class Pic(QtGui.QGraphicsItem):
	
	def boundingRect(self):
		ad = 2
		return QtCore.QRectF(-10 - ad, -10 - ad, 23 + ad, 23 + ad)
	def paint(self, painter, option, widget):
		painter.drawEllipse(0, 0, 20, 20)
	def mousePressEvent(self, event):
		print "AAA"
		
node = Pic()
node.setPos(-50, 50)
scene.addItem(node)


view = QtGui.QGraphicsView(scene)
view.show()


sys.exit(app.exec_())
