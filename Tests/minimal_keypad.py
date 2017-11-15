#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pyautogui import typewrite
from PyQt4 import QtGui, QtCore

class numKeyButton(QtGui.QPushButton):

    def __init__(self, priKey, parent=None):
        super(numKeyButton, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setText(priKey)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
        self.clicked.connect(lambda: typewrite(priKey))

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.resize(800,350)
        
        self.initUI()
        
    def initUI(self):

        frame = QtGui.QFrame(self)
        frame.setFrameShape(0)
        frame.setGeometry(200,50,450,300)
        
        grid = QtGui.QGridLayout()
        frame.setLayout(grid)
        

        line_ed = QtGui.QLineEdit(self)
        line_ed.setFocus(True)
        grid.addWidget(line_ed, 0,1, 1,2)

        
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']
        
        positions = [(i,j) for i in range(1,5) for j in range(4)]
        
        for position, name in zip(positions, names):
            
            if name == '':
                continue
            elif name == 'Close':
                button = numKeyButton(name)
                grid.addWidget(button, 1,2, 1,2)
                continue
            
            button = numKeyButton(name)
            grid.addWidget(button, *position)
            
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
