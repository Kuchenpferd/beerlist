#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pyautogui import typewrite
from PyQt4 import QtGui, QtCore


# Defined a separate class for the NumPad keytype
class numKeyButton(QtGui.QPushButton):

    def __init__(self, priKey, parent=None):
        super(numKeyButton, self).__init__(parent)
        
        # As we will be using the grid environment, we set our size policy to 'Expanding'
        # in both directions. We also ensure that the buttons never take focus (from a LinEdit fx.
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Simply sets the label for the button, and sets the clicked action to emulate a keypress
        self.setText(priKey)
        self.clicked.connect(lambda: typewrite(priKey))

class Example(QtGui.QWidget):

    # A dummy Widget, resized to the expected size, moving and naming it and calling some UI
    def __init__(self):
        super(Example, self).__init__()
        self.resize(800,350)
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.initUI()

    def initUI(self):

        # Decided to contain the layout in a (invisible) frame to control geometry
        frame = QtGui.QFrame(self)
        frame.setFrameShape(0)
        frame.setGeometry(200,50,450,300)

        # Initializing the grid layout and connecting it to the beforementioned frame
        grid = QtGui.QGridLayout()
        frame.setLayout(grid)
        
        # Placing a simple LineEdit at the top of the grid, to test the keystrokes.
        # Also grabs the initial focus (Probably not stricly necessary)
        line_ed = QtGui.QLineEdit(self)
        line_ed.setFocus(True)
        grid.addWidget(line_ed, 0,1, 1,2)

        # Making a list of keynames
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']

        # Making a list of positions for the keynames
        positions = [(i,j) for i in range(1,5) for j in range(4)]

        for position, name in zip(positions, names):
            
            if name == '':
                continue
            elif name == 'Close':
                
                # Instanciating the button from our custom class and demonstrating the ability
                # to stretch a button across the grid as we add it
                button = numKeyButton(name)
                grid.addWidget(button, 1,2, 1,2)
                continue

            # Simply creating buttons and adding them to the grid
            button = numKeyButton(name)
            grid.addWidget(button, *position)
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
