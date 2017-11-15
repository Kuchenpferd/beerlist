#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pyautogui import typewrite
from PyQt4 import QtGui, QtCore

# Externalizes the lengthy setting of a few standard button settings.
# (Should probably be changed to a  superclass instead)
def setButtonParms(anyButton):
    anyButton.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
    anyButton.setFocusPolicy(QtCore.Qt.NoFocus)

# A dummy default checkable button.
# (Serves as a standard input, but might not be needed due to implementation)
class dummyButton():
        def isChecked():
            return False
        
# Basically a cleaned version of the ./minimal_keypad.py button,
# please refer there for further detail
class numKeyButton(QtGui.QPushButton):

    def __init__(self, priKey, parent = None):
        super(numKeyButton, self).__init__(parent)
        setButtonParms(self)
        
        self.priKey = priKey
        self.setText(priKey)
        self.clicked.connect(self.onClick)

    def onClick(self):
        typewrite(self.priKey)

# Class for the modifier keys (Shift and Alt), basically just a checkable QPushButton
class modKeyButton(QtGui.QPushButton):

    def __init__(self, labelText, parent = None):
        super(modKeyButton, self).__init__(parent)
        setButtonParms(self)
        
        self.setCheckable(True)
        self.setText(labelText)
    

# Class for alph keyboard, which should be passed the setup specific shift and alt mod button.
# Can thus emit 4 different symbols (primary low/cap and secondary low/cap)
class boardKeyButton(QtGui.QPushButton):

    def __init__(self, initKey, modShButton = dummyButton(), modAltButton = dummyButton(), parent = None):
        super(boardKeyButton, self).__init__(parent)
        setButtonParms(self)

        # Passing the modifier buttons to the current class
        self.modShButton = modShButton
        self.modAltButton = modAltButton

        # Determining if the button was passed a secondary key and from that defining the button label
        if len(initKey) == 1:
            self.priKey = initKey
            self.secKey = initKey
            labelText = self.priKey
        else:
            self.priKey = initKey[0]
            self.secKey = initKey[1]
            labelText = '{} / {}'.format(self.priKey, self.secKey)
            
        self.setText(labelText)

        # Connects the click to an internal function
        # (This should be superclassed along with other general button properties)
        self.clicked.connect(self.onClick)

    # Function which is called as the button is clicked
    def onClick(self):
        
        # Checks if the primary or secondary key should be emitted
        if not self.modAltButton.isChecked():
            Key = self.priKey
        else:
            Key = self.secKey

        # Determines if the key should be put in upper case
        if self.modShButton.isChecked():
            Key = Key.upper()
        typewrite(Key)


# Dummy widget to test. Basically the same as ./minimal_keypad.py
class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('Calculator')
        self.resize(800,480)
        self.move(300, 150)
        
        self.mainUI()

    def mainUI(self):

        # The LineEdit is no longer in the grid, but manually put atop the now two frames and grids
        line_ed = QtGui.QLineEdit(self)
        line_ed.setFocus(True)
        line_ed.move(20,10)
        line_ed.resize(760,30)

        frame_board = QtGui.QFrame(self)
        frame_board.setFrameShape(0)
        frame_board.setGeometry(400,50,390,430)
        
        grid_board = QtGui.QGridLayout()
        frame_board.setLayout(grid_board)

        # Modifer buttons should ALWAYS be instanciated BEFORE ordinary keys
        sh_btn = modKeyButton('Shift')
        alt_btn = modKeyButton('Alt')

        # Alternate keys are simply input in name by putting the two symbols next to each other
        names = ['aä', 'b', 'c', 'z',
                 '.', "'", '!', '-',
                'æ', 'ø', 'å', 'oö',
                 'iï', 'uû', 'Shift', '',
                '0', '.,', 'Alt', '']
        
        positions = [(i,j) for i in range(5) for j in range(4)]
        
        for position, name in zip(positions, names):
            
            if name == '':
                continue
            elif name == 'Shift':
                grid_board.addWidget(sh_btn, *position, 1,2)
                continue
            elif name == 'Alt':
                grid_board.addWidget(alt_btn, *position, 1,2)
                continue

            # The ordinary buttons are added, note that they need to be handed the instanciated modififer keys
            btn = boardKeyButton(name, sh_btn, alt_btn)
            grid_board.addWidget(btn, *position)


        # Setup of the numpad is almost identical to ./minimal_keypad.py
        frame_num = QtGui.QFrame(self)
        frame_num.setFrameShape(0)
        frame_num.setGeometry(10,50,390,430)
        
        grid_num = QtGui.QGridLayout()
        frame_num.setLayout(grid_num)
        
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
                button = numKeyButton(name)
                grid_num.addWidget(button, 0,2, 1,2)
                continue
            
            btn = numKeyButton(name)
            grid_num.addWidget(btn, *position)
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
