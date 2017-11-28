#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from loremipsum import get_paragraph, get_sentence
from PyQt4 import QtGui, QtCore
from random import randint

workFolder = './'
resourceFolder = workFolder + 'Resources/'

# List of UI ids:
uiIdList = ['None', 'mainMenu', 'multiMode', 'markDone', 'resetPwd',
            'login', 'loggedIn', 'ChangePwd', 'ChangeCard', 'payMode',
            'newUser-sduId', 'newUser-name', 'newUser-newCard',
            'newUser-oldUsers', 'newUser-balance', 'newUser-final']

class expandButton(QtGui.QPushButton):
    def __init__(self, parent = None):
        super(expandButton, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
        newFont = self.font()
        newFont.setPointSize(12)
        newFont.setBold(True)
        self.setFont(newFont)
        

# A super class for the standard UI
class standardUI(QtGui.QWidget):
    def __init__(self, mainWidget, parent = None, backButton = True, menuButton = True):
        super(standardUI, self).__init__(parent)
        self.setGeometry(0,0,800,480)
        self.mainWidget = mainWidget
        self.id = 'None'

        self.cardSequence = ''
        self.swipeActive = True

        if menuButton:
            menuBtn = QtGui.QPushButton(self)
            menuBtn.resize(80, 80)
            menuBtn.move(710, 10)
            menuBtn.setIcon(QtGui.QIcon(resourceFolder + 'home.svg'))
            menuBtn.clicked.connect(self.mainMenuDialog)

        if backButton:
            menuBtn = QtGui.QPushButton(self)
            menuBtn.resize(80, 80)
            menuBtn.move(10, 10)
            menuBtn.setIcon(QtGui.QIcon(resourceFolder + 'left-arrow.svg'))
            menuBtn.clicked.connect(self.backDialog)

        
    # Modifies the keyPressedEvent to specifically listen for SDU cards
    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if self.swipeActive:
                # Check if the pressed keycode matches the card initializer 'æ'
                if event.key() == 198:
                    # Clears the stored sequence, i.e. initialization
                    self.cardSequence = ''
                # Check if the pressed keycode matches the card terminator (Either 'Enter' key, should be cleaned later)
                elif event.key() == 16777221 or event.key() == 16777220:
                    # Placeholder for the event, where we can pass the card sequence, i.e. termination
                    self.swipeAction()
                # Always add the latest keypress at the end of the card sequence
                self.cardSequence += event.text()
            
            event.accept()
        else:
            event.ignore()

    def mainMenuDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtGui.QMessageBox(self.mainWidget)
        msg.setGeometry(370,225,60,30)
        msg.setText('Do you want to return to the main menu?')
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtGui.QMessageBox.Yes:
            self.mainWidget.changeUI('mainMenu')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtGui.QMessageBox.No:
            pass
        
    def backDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtGui.QMessageBox(self.mainWidget)
        msg.setGeometry(370,225,60,30)
        msg.setText('Do you want to return to previous screen?')
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtGui.QMessageBox.Yes:
            self.mainWidget.changeUI('back')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtGui.QMessageBox.No:
            pass
    
    def swipeAction(self):
        print(self.cardSequence)
        pass
    
    # A function that updates the UI, will be empty for static UIs, and content will be
    # specified as each UI is set up
    def update(self):
        pass

class mainMenuUI(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(mainMenuUI, self).__init__(mainWidget, parent, False, False)
        self.id = 'mainMenu'
        self.swipeActive = True

        multiBtn = expandButton(self)
        multiBtn.setText('Multi Mode')
        multiBtn.clicked.connect(lambda: self.mainWidget.changeUI('multiMode'))

        loginBtn = expandButton(self)
        loginBtn.setText('Login')
        loginBtn.clicked.connect(lambda: self.mainWidget.changeUI('login'))

        newUserBtn = expandButton(self)
        newUserBtn.setText('New User')
        newUserBtn.clicked.connect(lambda: self.mainWidget.changeUI('newUser-sduId'))

        resetBtn = expandButton(self)
        resetBtn.setText('Reset Password')
        resetBtn.clicked.connect(lambda: self.mainWidget.changeUI('resetPwd'))

        titleLabel = QtGui.QLabel(self)
        titleLabel.setText('Welcome to Æters Beerlist system v. 2.0')
        newFont = titleLabel.font()
        newFont.setPointSize(14)
        newFont.setBold(True)
        titleLabel.setFont(newFont)

        contentLabel = QtGui.QLabel(self)
        contentLabel.setText('To grab a beer or soda please swipe your card!\nTo grab multiple, press "Multi Mode"!\nTo create a new user swipe your card or press "New User"\n\nTo see your balance, change your password or card, please login')
        newFont = contentLabel.font()
        newFont.setPointSize(10)
        contentLabel.setFont(newFont)

        grid = QtGui.QGridLayout()
        grid.addWidget(titleLabel, 0, 1, 1, 2)
        grid.addWidget(contentLabel, 1, 1, 1, 2)
        grid.addWidget(multiBtn, 2, 0, 1, 2)
        grid.addWidget(loginBtn, 2, 2, 1, 2)
        grid.addWidget(newUserBtn, 3, 0, 1, 2)
        grid.addWidget(resetBtn, 3, 2, 1, 2)

        self.setLayout(grid)

        





# A class for the main UI
class genMainUI(standardUI):

    # The init function sets up the content of the UI, note that the main widget is passed
    # as well, and internalized for ease of use. The id is also specified
    def __init__(self, mainWidget, parent = None):
        super(genMainUI, self).__init__(parent)
        self.masterWidget = mainWidget
        self.id = 'mainUI'

        # Next the content of the screen is set up:
            
        # A button to move to the next screen is set up. The clicked signal is connected
        # to a function within the main window to change UI to secUI
        btn = QtGui.QPushButton('Next', self)
        btn.clicked.connect(lambda: self.masterWidget.changeUI('secUI'))

        # A few labels is set up
        l1 = QtGui.QLabel(self)
        l2 = QtGui.QLabel(self)

        # And given some content with the loremipsum package
        l1.setText(get_sentence(True))
        l2.setText(get_sentence(True) + get_sentence(True) + get_sentence(True) + get_sentence(True) + '\n\n' + get_sentence(True))
            
        l2.setWordWrap(True)

        # A vertical layout is set up, and the labels and button are added
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addStretch(2)
        vbox.addWidget(l2)
        vbox.addStretch()
        vbox.addWidget(btn)

        # At last the layout is added to the widget
        self.setLayout(vbox)

# The class to set up the secondary UI
class genSecUI(standardUI):

    # The main widget is once again internalized and the id of the UI is set
    def __init__(self, mainWidget, parent = None):
        super(genSecUI, self).__init__(parent)
        self.masterWidget = mainWidget
        self.id = 'secUI'
        
        # This UI also has a button to move back to the previous UI,
        # but it is connected to a dialog option (see below)
        btn1 = QtGui.QPushButton('Next', self)
        btn1.clicked.connect(self.toMainDialog)

        # The other button here only serves the purpose of updating content within the current UI
        btn2 = QtGui.QPushButton('Update', self)
        btn2.clicked.connect(self.update)

        # Once again a few labels is set up and everything is added to a VBox layout.
        # Note that if any conent is updateable, it should be added to self as an attribute
        l1 = QtGui.QLabel(self)
        l2 = QtGui.QLabel(self)
        self.l3 = QtGui.QLabel(self)
            
        l1.setText('Who and where?!')
        l2.setText('What is going on!??!')
        self.l3.setText(str(randint(0,100)))
        
        l2.setWordWrap(True)
    
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(l1)
        vbox.addWidget(l2)
        vbox.addWidget(self.l3)
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
            
        # At last the layout is added to the widget
        self.setLayout(vbox)

    # An example of a pop-up dialog, with a simple yes/no question
    def toMainDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtGui.QMessageBox(self.masterWidget)
        msg.setGeometry(50,100,60,30)
        msg.setText('Do you want to go move on?')
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtGui.QMessageBox.Yes:
            self.masterWidget.changeUI('mainUI')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtGui.QMessageBox.No:
            pass

    # The standard (empty) update method is updated to update the content of the UI
    def update(self):
        self.l3.setText(str(randint(0,100)))
        
def main():
    this = mainMenuUI(QtGui.QWidget(), QtGui.QWidget())
    pass
    
if __name__ == '__main__':
    main()
