#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui


# For comments, please see ./minimal_keypad.py
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
        
 
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']
        
        positions = [(i,j) for i in range(5) for j in range(4)]
        
        for position, name in zip(positions, names):
            
            if name == '':
                continue
            elif name == 'Close':
                button = QtGui.QPushButton(name)
                grid.addWidget(button, 0,2, 1,2)
                continue
            
            button = QtGui.QPushButton(name)
            button.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
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
