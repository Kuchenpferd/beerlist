#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyautogui as pag
from PyQt5 import QtWidgets, QtCore, QtGui

# Path to determine the resource folder (Should be changed, when imported
workFolder = './../'
resourceFolder = workFolder + 'Resources/'

keyDict = {
    '1':QtCore.Qt.Key_1,
    '2':QtCore.Qt.Key_2,
    '3':QtCore.Qt.Key_3,
    '4':QtCore.Qt.Key_4,
    '5':QtCore.Qt.Key_5,
    '6':QtCore.Qt.Key_6,
    '7':QtCore.Qt.Key_7,
    '8':QtCore.Qt.Key_8,
    '9':QtCore.Qt.Key_9,
    '0':QtCore.Qt.Key_0,
    'a':QtCore.Qt.Key_A,
    'b':QtCore.Qt.Key_B,
    'c':QtCore.Qt.Key_C,
    'd':QtCore.Qt.Key_D,
    'e':QtCore.Qt.Key_E,
    'f':QtCore.Qt.Key_F,
    'g':QtCore.Qt.Key_G,
    'h':QtCore.Qt.Key_H,
    'i':QtCore.Qt.Key_I,
    'j':QtCore.Qt.Key_J,
    'k':QtCore.Qt.Key_K,
    'l':QtCore.Qt.Key_L,
    'm':QtCore.Qt.Key_M,
    'n':QtCore.Qt.Key_N,
    'o':QtCore.Qt.Key_O,
    'p':QtCore.Qt.Key_P,
    'q':QtCore.Qt.Key_Q,
    'r':QtCore.Qt.Key_R,
    's':QtCore.Qt.Key_S,
    't':QtCore.Qt.Key_T,
    'u':QtCore.Qt.Key_U,
    'v':QtCore.Qt.Key_V,
    'w':QtCore.Qt.Key_W,
    'x':QtCore.Qt.Key_X,
    'y':QtCore.Qt.Key_Y,
    'z':QtCore.Qt.Key_Z,
    'æ':QtCore.Qt.Key_AE,
    'ø':QtCore.Qt.Key_Ooblique,
    'å':QtCore.Qt.Key_Aring,
    '-':QtCore.Qt.Key_Minus,
    ".":QtCore.Qt.Key_Period,
    '@':QtCore.Qt.Key_At,
    'space':QtCore.Qt.Key_Space,
    'backspace':QtCore.Qt.Key_Backspace}

def changeFont(someLabel, size = 10, bold = False, align = 'l'):
    if align == 'l':
        alignment = QtCore.Qt.Alignment(QtCore.Qt.AlignLeft)
    elif align == 'c':
        alignment = QtCore.Qt.Alignment(QtCore.Qt.AlignHCenter)
    elif align == 'r':
        alignment = QtCore.Qt.Alignment(QtCore.Qt.AlignRight)
        
    newFont = someLabel.font()
    newFont.setPointSize(size)
    newFont.setBold(bold)
    someLabel.setFont(newFont)
    
    try:
        someLabel.setAlignment(alignment)
    except:
        pass
    
    return someLabel

# Emulate a keypress of non-standard utf8 keys
def emuKeyPress(target, Key):
    if Key.isupper():
        modKey = QtCore.Qt.ShiftModifier
    else:
        modKey = QtCore.Qt.NoModifier
    key = Key.lower()

    event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, keyDict[key], modKey, text=Key)

    target.keyPressEvent(event)

# Superclass of the rest of the keyButtons with some standard settings
class keyButton(QtWidgets.QPushButton):
    def __init__(self, parent = None):
        super(keyButton, self).__init__(parent)
        if parent is not None:
            self.target = parent.target
        else:
            self.target = None
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(self.onClick)
        self = changeFont(self, 10)

    def onClick(self):
        pass
        
# Basically a cleaned version of the ./minimal_keypad.py button,
# please refer there for further detail
class numKeyButton(keyButton):

    def __init__(self, priKey, parent = None):
        super(numKeyButton, self).__init__(parent)
        self = changeFont(self, 12)
        self.priKey = priKey
        self.setText(priKey)

    def onClick(self):
        emuKeyPress(self.target, self.priKey)

# Class for the modifier keys (Shift and Alt), basically just a checkable QPushButton
class modKeyButton(keyButton):

    def __init__(self, labelText, parent = None):
        super(modKeyButton, self).__init__(parent)
        
        self.setCheckable(True)
        self.labelText = labelText
        self.parent = parent
        self.affKeys = None

        # Uses an icon for shift instead of a text label
        if labelText == 'Shift':
            self.setIcon(QtGui.QIcon(resourceFolder + 'shift-arrow.svg'))
        elif labelText == 'Alt':
            self.setText(labelText)

    # On click the mod button will change the text of the affected keys
    def onClick(self):

        # On first click we determine which buttons will be affected (on a set of lists from the parent)
        if self.affKeys is None:
            btnNames = zip(self.parent.btnNames[0], self.parent.btnNames[1])
            affKeys = []
            self.affKeys = affKeys
            for btn, name in btnNames:
                if self.labelText == 'Shift' and len(name) == 1:
                    affKeys.append((btn, name))
                elif self.labelText == 'Alt' and len(name) == 2:
                    affKeys.append((btn, f'{name[0]} / {name[1]}'))

        # Every affected button gets a new text according to the type of mod this button is
        for btn, name in self.affKeys:
            if self.isChecked():
                if self.labelText == 'Shift':
                    btn.setText(name.title())
                elif self.labelText == 'Alt':
                    btn.setText(name[::-1])
            else:
                btn.setText(name)


# Class for alph keyboard, which should be passed the setup specific shift and alt mod button.
# Can thus emit 4 different symbols (primary low/cap and secondary low/cap)
class boardKeyButton(keyButton):

    def __init__(self, initKey, modShButton, modAltButton, parent = None):
        super(boardKeyButton, self).__init__(parent)

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
            self.modShButton.click()
        emuKeyPress(self.target, Key)

# The class that contains the input layout
class inputFrame(QtWidgets.QFrame):

    # Takes an input type and a parent in; disables drawing of the frame
    def __init__(self, target, inputType = '', parent = None):
        super(inputFrame, self).__init__(parent)
        self.target = target
        self.setFrameShape(0)

        # Calls the appropriate layout setup according to the input type
        if inputType == 'full' or inputType == 1:
            self.setupFull()
        elif inputType == 'numpad' or inputType == 2:
            self.setupNumpad()
        else:
            return 'Input type not recognized!'

    # Sets up the full keyboard layout, including geometry and size
    def setupFull(self):
        self.setGeometry(0,100,800,380)
        grid = QtWidgets.QGridLayout(self)

        # The keyboard key layout
        names =    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-',
                    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å',
                    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'æ', 'ø',
                    'z', 'x', 'c', 'v', 'b', 'n', 'm', ".", '@', 'enter', '',
                    'Shift', '', 'space', '', '', '', '', 'backspace', '', '', '']

        # List of key positions
        positions = [(i,j) for i in range(5) for j in range(11)]

        # Setting up modifier buttons prior to instanciating buttons
        shButton = modKeyButton('Shift', self)
        altButton = modKeyButton('Alt', self)
        altButton.hide()

        buttons = []
        
        for position, name in zip(positions, names):

            # If the label is empty, dont make a button
            if name == '':
                continue

            # Instanciates the backspace key, including icon and action on click
            elif name == 'backspace':
                btn = keyButton(self)
                btn.setIcon(QtGui.QIcon(resourceFolder + 'backspace.svg'))
                btn.clicked.connect(lambda: emuKeyPress(btn.target, 'backspace'))                
                grid.addWidget(btn, *position, 1, 2)

            # Instanciates the enter key, including icon and sets it as a property
            # of the frame, so that it can be reached in order to specify on click action later
            elif name == 'enter':
                btn = keyButton(self)
                btn.setIcon(QtGui.QIcon(resourceFolder + 'enter-arrow.svg'))
                self.enterBtn = btn                
                grid.addWidget(btn, *position, 2, 2)
                
            # Merely places the modfier keys in the grid
            elif name == 'Shift':
                grid.addWidget(shButton, *position, 1, 2)
            elif name == 'Alt':
                grid.addWidget(altButton, *position)

            # Creates the spacebar including action.
            elif name == 'space':
                btn = keyButton(self)
                btn.clicked.connect(lambda: emuKeyPress(btn.target, 'space'))                
                grid.addWidget(btn, *position, 1, 5)

            # Generates the ordinary keys, handing them the modifier keys
            else:
                btn = boardKeyButton(name, shButton, altButton, self)
                grid.addWidget(btn, *position)

            if name != '':
                buttons.append(btn)

        # Finally the layout is connected to the frame
        self.setLayout(grid)

        # The buttons and thier names are connected to the frame (so that mod buttons can access those lists)
        self.btnNames = (buttons, names)

    # Sets up the numpad layout including geometry and size
    def setupNumpad(self):
        self.setGeometry(200,100,400,380)
        grid = QtWidgets.QGridLayout(self)

        # The name layout for the keypad
        names =    ['1', '2', '3',
                    '4', '5', '6',
                    '7', '8', '9',
                    'backspace', '0', 'enter']

        # List of grid positions
        positions = [(i,j) for i in range(4) for j in range(3)]

        for position, name in zip(positions, names):

            # Creates the backspace button, including icon and on click action
            if name == 'backspace':
                btn = keyButton(self)
                btn.setIcon(QtGui.QIcon(resourceFolder + 'backspace.svg'))
                btn.clicked.connect(lambda: emuKeyPress(btn.target, 'backspace'))

            # Creates the enter key, including icon and sets it as a property
            # of the frame, so that it can be reached in order to specify on click action later
            elif name == 'enter':
                btn = keyButton(self)
                btn.setIcon(QtGui.QIcon(resourceFolder + 'enter-arrow.svg'))
                self.enterBtn = btn

            # Creating the ordinary buttons
            else:
                btn = numKeyButton(name, self)

            # Placing all the buttons in the grid
            grid.addWidget(btn, *position)

        # Finally connects the layout to the grid
        self.setLayout(grid)
      
def main():
    pass

if __name__ == '__main__':
    main()
