"""
import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

label = QtGui.QLabel("Hello World!")
label.show()

sys.exit(app.exec_())
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
# PyQt sample 4.4
 
import sys
from PyQt4 import QtGui
 
class GridLayout2(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
 
        self.setWindowTitle(self.trUtf8('1'))
 
        title = QtGui.QLabel(self.trUtf8('2'))
        author = QtGui.QLabel(self.trUtf8('3'))
        review = QtGui.QLabel(self.trUtf8('4'))
 
        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()
 
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
 
        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)
 
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
 
        self.setLayout(grid)
        self.resize(350, 300)
 
app = QtGui.QApplication(sys.argv)
qb = GridLayout2()
qb.show()
sys.exit(app.exec_())