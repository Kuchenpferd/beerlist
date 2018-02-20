#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import inputWidgets
import userFuncs, refFuncs, statFuncs, mailFuncs
from PyQt5 import QtWidgets, QtCore, QtGui
from hashlib import sha256
from time import sleep

contact = 'mikkc13'
workFolder = './../'
resourceFolder = workFolder + 'Resources/'

changeFont = inputWidgets.changeFont

# List of UI ids:
uiIdList = ['mainMenu', 'multiMode', 'markDone', 'resetPwd',
            'login', 'loggedIn', 'changePwd', 'changeCard', 'payMode',
            'newUserInitial', 'newUserCard', 'newUserOldUsers',
            'newUserBalance', 'newUserFinal']

class expandButton(QtWidgets.QPushButton):
    def __init__(self, parent = None):
        super(expandButton, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        self = changeFont(self, 12, True)

class swipeLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent = None):
        super(swipeLineEdit, self).__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.text() != 'æ':
            if self.parent.cardSequence[0] != 'æ':
                super(swipeLineEdit, self).keyPressEvent(event)
        self.parent.keyPressEvent(event)
    

# A super class for the standard UI
class standardUI(QtWidgets.QWidget):
    def __init__(self, mainWidget, parent = None, backButton = True, menuButton = True):
        super(standardUI, self).__init__(parent)
        self.setGeometry(0,0,800,480)
        self.mainWidget = mainWidget
        self.id = 'None'

        self.cardSequence = ' '
        self.swipeActive = False

        if menuButton:
            menuBtn = QtWidgets.QPushButton(self)
            menuBtn.resize(80, 80)
            menuBtn.move(710, 10)
            menuBtn.setIcon(QtGui.QIcon(resourceFolder + 'home.svg'))
            menuBtn.clicked.connect(self.mainMenuDialog)

        if backButton:
            menuBtn = QtWidgets.QPushButton(self)
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
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(220,180)
        msg.setText('Do you want to return to the main menu?')
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('mainMenu')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtWidgets.QMessageBox.No:
            self.update()
        
    def backDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(220,180)
        msg.setText('Do you want to return to previous screen?')
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('back')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtWidgets.QMessageBox.No:
            self.update()

    def newUserDialog(self, update = True):
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True, 'c')
        msg.move(260,150)
        msg.setText('Unknown card swiped!\n\nDo you wish to create a new user?')
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('newUserInitial')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtWidgets.QMessageBox.No:
            if update:
                self.update()
            else:
                pass
    
    def swipeAction(self):
        pass
    
    # A function that updates the UI, will be empty for static UIs, and content will be
    # specified as each UI is set up
    def update(self):
        self.cardSequence = ' '



class mainMenu(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(mainMenu, self).__init__(mainWidget, parent, False, False)
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
        newUserBtn.clicked.connect(lambda: self.mainWidget.changeUI('newUserInitial'))

        resetBtn = expandButton(self)
        resetBtn.setText('Reset Password')
        resetBtn.clicked.connect(lambda: self.mainWidget.changeUI('resetPwd'))

        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText('Welcome to Æters Beerlist system v. 2.0')
        titleLabel = changeFont(titleLabel, 14, True, 'c')

        contentLabel = QtWidgets.QLabel(self)
        contentLabel.setText(f"""To grab a beer or soda please swipe your card!\nTo grab multiple, press "Multi Mode"!\nTo create a new user swipe your card or press "New User"!\nTo see your balance, grab beers without your card,\nchange your password or card, please login!\nIf You have any problems, please contact {contact}!""")
        contentLabel = changeFont(contentLabel)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(titleLabel, 0, 1, 1, 2)
        grid.addWidget(contentLabel, 1, 1, 1, 2)
        grid.addWidget(multiBtn, 2, 0, 1, 2)
        grid.addWidget(loginBtn, 2, 2, 1, 2)
        grid.addWidget(newUserBtn, 3, 0, 1, 2)
        grid.addWidget(resetBtn, 3, 2, 1, 2)

        self.setLayout(grid)

    def update(self):
        super().update()
        self.mainWidget.currentUser = refFuncs.refUserInstance()
        self.mainWidget.currentRefUserList = []
        self.mainWidget.transfer = []

    def swipeAction(self):
        if self.cardSequence[0] == 'æ':
            swipedUser = userFuncs.findUserCard(self.cardSequence)
            if swipedUser is not None:
                swipedUser.addSome()
                swipedUser.saveUser()
                self.mainWidget.transfer.append(1)
                self.mainWidget.currentUser = swipedUser
                self.mainWidget.changeUI('markDone')
            else:
                self.mainWidget.currentUser.cardId = self.cardSequence
                self.newUserDialog()

    
class multiMode(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(multiMode, self).__init__(mainWidget, parent)
        self.id = 'multiMode'
        self.swipeActive = True

        numPad = inputWidgets.inputFrame('numpad', self)
        numPad.enterBtn.clicked.connect(self.enterAction)
        self.enterBtn = numPad.enterBtn

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please enter the wanted amount and swipe your card:',
                            'Please enter the wanted amount and press enter:']
                            
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = swipeLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        inputEdit.setMaxLength(2)
        self.inputEdit = inputEdit
        
        vbox = QtWidgets.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def swipeAction(self):
        if self.cardSequence[0] == 'æ':
            swipedUser = userFuncs.findUserCard(self.cardSequence)
            if swipedUser is not None:
                self.mainWidget.currentUser = swipedUser
                self.enterAction()
            else:
                self.mainWidget.currentUser.cardId = self.cardSequence
                self.newUserDialog(False)
    
    def enterAction(self):
        if self.inputEdit.text() == '':
            self.emptyLineDialog()
            self.update()
            return
        
        units = int(self.inputEdit.text())
                    
        self.mainWidget.currentUser.addSome(units)
        self.mainWidget.currentUser.saveUser()

        self.mainWidget.transfer.append(units)
        self.mainWidget.changeUI('markDone')

    def update(self):
        super().update()
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

        if self.mainWidget.lastWidgetId == 'mainMenu':
            self.titleLabel.setText(self.titleString[0])
            self.swipeActive = True
            self.enterBtn.setEnabled(False)
        elif self.mainWidget.lastWidgetId == 'loggedIn':
            self.titleLabel.setText(self.titleString[1])
            self.swipeActive = False
            self.enterBtn.setEnabled(True)

    def emptyLineDialog(self):

        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText('The input line seems empty!')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        

class markDone(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(markDone, self).__init__(mainWidget, parent, False, False)
        self.id = 'markDone'

        self.contentString = 'Hi {name}!\n{amount} kr was added to your balance, which is now {balance} kr!\nRemember to pay your debt regularly!'
        
        contentLabel = QtWidgets.QLabel(self)
        contentLabel = changeFont(contentLabel, 12, True, 'c')
        contentLabel.setText(self.contentString)
        self.contentLabel = contentLabel

        menuBtn = expandButton(self)
        menuBtn.setIcon(QtGui.QIcon(resourceFolder + 'home.svg'))
        menuBtn.clicked.connect(lambda: self.mainWidget.changeUI('mainMenu'))

        payBtn = expandButton(self)
        payBtn.setText('Pay debt')
        payBtn.clicked.connect(lambda: self.mainWidget.changeUI('payMode'))
        self.payBtn = payBtn

        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(contentLabel, 1, 1, 1, 2)
        grid.addWidget(payBtn, 2, 1)
        grid.addWidget(menuBtn, 2, 2)
        
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,2)
        grid.setRowStretch(2,2)
        grid.setRowStretch(3,1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(3,1)

        self.setLayout(grid)

    def update(self):
        try:
            units = self.mainWidget.transfer[0]
        except:
            units = 1
        amount = units*userFuncs.price
        self.mainWidget.transfer = []
        
        name = self.mainWidget.currentUser.name
        balance = self.mainWidget.currentUser.balance
        
        self.contentLabel.setText(f'Hi {name}!\n{amount} kr was added to your balance, which is now {balance} kr!\nRemember to pay your debt regularly!')

        

class resetPwd(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(resetPwd, self).__init__(mainWidget, parent)
        self.id = 'resetPwd'
        self.swipeActive = True

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(lambda: self.enterAction())

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        titleString = 'Please enter your SDU-ID or swipe your card to reset\nyour password:'

        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(titleString)
        titleLabel = changeFont(titleLabel, 11.5, True, 'c')

        inputEdit = swipeLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        vbox = QtWidgets.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def update(self):
        super().update()
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

    def swipeAction(self):
        if self.cardSequence[0] == 'æ':
            swipedUser = userFuncs.findUserCard(self.cardSequence)
            if swipedUser is not None:
                self.enterAction(swipedUser)
            else:
                self.mainWidget.currentUser.cardId = self.cardSequence
                self.newUserDialog(True)

    def enterAction(self, user = None):
        if user is None:
            user = userFuncs.findUserNoCard(self.inputEdit.text())
            if user is None:
                self.errorDialog()
                self.update()
                return
        self.newPwdDialog(user)

    def newPwdDialog(self, user):
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True, 'c')
        msg.move(260,150)
        msg.setText(f"""Hi {user.name.split(' ')[0]}, are you sure you\nwant to reset your password?""")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            mailFuncs.sendMail(user, 'Pwd')
            self.doneDialog()

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtWidgets.QMessageBox.No:
            self.update()

    def doneDialog(self):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText('Okay, we have sent a mail with\nyour new password!')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        self.mainWidget.changeUI('mainMenu')

    def errorDialog(self):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText("Sorry, but we couldn't find your SDU-ID!\nPlease try again.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return
        

class login(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(login, self).__init__(mainWidget, parent)
        self.id = 'login'
        self.swipeActive = True
        self.input = 0
        self.count = 1

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please enter your SDU-ID or swipe your card to login:',
                            'Please enter your password:']

        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = swipeLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        vbox = QtWidgets.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def update(self):
        super().update()
        self.input = 0
        self.count = 1
        self.swipeActive = True
        self.titleLabel.setText(self.titleString[0])
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)
        self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Normal)

    def swipeAction(self):
        if self.cardSequence[0] == 'æ':
            swipedUser = userFuncs.findUserCard(self.cardSequence)
            if swipedUser is not None:
                self.mainWidget.currentUser = swipedUser
                self.mainWidget.changeUI('loggedIn')
                
            else:
                self.mainWidget.currentUser.cardId = self.cardSequence
                self.newUserDialog(True)

    def enterAction(self):
        if self.input == 0:

            user = userFuncs.findUserNoCard(self.inputEdit.text())

            if user != None:
                self.mainWidget.currentUser = user
            else:
                self.errorDialog()
                self.update()
                return
            
            self.titleLabel.setText(self.titleString[1])
            self.inputEdit.setFocus(True)
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.inputEdit.setText('')
            self.input = 1
            self.swipeActive = False
            
        elif self.input == 1:

            inputPwd = sha256(self.inputEdit.text().encode()).hexdigest()
            userPwd = self.mainWidget.currentUser.pwd

            if inputPwd == userPwd:
                self.mainWidget.changeUI('loggedIn')
                
            else:
                self.errorDialog()
                if self.count == 3:
                    self.update()
                else:
                    self.inputEdit.setText('')
                    self.count += 1
                
    def errorDialog(self):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        if self.input == 0:
            msg.setText("Sorry, but we couldn't find your SDU-ID!\nPlease try again.")
        elif self.input == 1 and self.count != 3:
            msg.setText("Password incorrect!\nPlease try again.")
        else:
            msg.setText("Password thrice incorrect!\nPlease enter SDU-ID again.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return

class loggedIn(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(loggedIn, self).__init__(mainWidget, parent)
        self.id = 'loggedIn'

        self.titleString = 'Welcome {name}!\nYour current balance is {balance} kr!\nA negative balance is a good thing!'
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel
        
        oneBtn = expandButton(self)
        oneBtn.setText('One mark')
        oneBtn.clicked.connect(self.markOne)
        
        multiBtn = expandButton(self)
        multiBtn.setText('Multi mode')
        multiBtn.clicked.connect(lambda: self.mainWidget.changeUI('multiMode'))

        payBtn = expandButton(self)
        payBtn.setText('Pay')
        payBtn.clicked.connect(lambda: self.mainWidget.changeUI('payMode'))

        chnPwdBtn = expandButton(self)
        chnPwdBtn.setText('Change Password')
        chnPwdBtn.clicked.connect(self.changePwdDialog)

        chnCardBtn = expandButton(self)
        chnCardBtn.setText('Change Card')
        chnCardBtn.clicked.connect(self.changeCardDialog)

        grid = QtWidgets.QGridLayout(self)
        grid.setRowStretch(0,1.1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)
        grid.addWidget(titleLabel, 0, 1, 1, 4)
        grid.addWidget(oneBtn, 1, 0, 1, 2)
        grid.addWidget(multiBtn, 1, 2, 1, 2)
        grid.addWidget(payBtn, 1, 4, 1, 2)
        grid.addWidget(chnPwdBtn, 2, 1, 1, 2)
        grid.addWidget(chnCardBtn, 2, 3, 1, 2)

        self.setLayout(grid)

    def markOne(self):
        self.mainWidget.currentUser.addSome()
        self.mainWidget.currentUser.saveUser()
        self.mainWidget.changeUI('markDone')
        
    def update(self):
        name = self.mainWidget.currentUser.name
        balance = self.mainWidget.currentUser.balance
        self.titleLabel.setText(f'Welcome {name}!\nYour current balance is {balance} kr!\nA negative balance is a good thing!')

    def changePwdDialog(self):

        user = self.mainWidget.currentUser
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True, 'c')
        msg.move(260,150)
        msg.setText(f"""Hi {user.name.split(' ')[0]}, are you sure you\nwant to change your password?""")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('changePwd')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtWidgets.QMessageBox.No:
            self.update()

    def changeCardDialog(self):

        user = self.mainWidget.currentUser
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True, 'c')
        msg.move(260,150)
        msg.setText(f"""Hi {user.name.split(' ')[0]}, are you sure you\nwant to change your card?""")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('changeCard')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtWidgets.QMessageBox.No:
            self.update()

class changePwd(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(changePwd, self).__init__(mainWidget, parent)
        self.id = 'changePwd'
        self.pwd = ''

        self.input = 0

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please your new password:',
                            'Please enter it again:']
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = swipeLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        inputEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputEdit = inputEdit
        
        vbox = QtWidgets.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def enterAction(self):
        if self.input == 0:
            inputPwd = self.inputEdit.text()

            if len(inputPwd) >= 4:
                self.pwd = sha256(inputPwd.encode()).hexdigest()
            else:
                self.errorDialog()
                self.update()
                return
            
            self.titleLabel.setText(self.titleString[1])
            self.input = 1
            self.inputEdit.setText('')
            self.inputEdit.setFocus(True)
        elif self.input == 1:
            if self.pwd == sha256(self.inputEdit.text().encode()).hexdigest():
                self.mainWidget.currentUser.pwd = self.pwd
                self.mainWidget.currentUser.saveUser()
                self.mainWidget.changeUI('loggedIn')
            else:
                self.errorDialog()
                self.update()

    def update(self):
        self.titleLabel.setText(self.titleString[0])
        self.input = 0
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

    def errorDialog(self):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        if self.input == 0:
            msg.setText("The password should be at least\n4 characters long!")
        else:
            msg.setText("Sorry, but the two passwords didn't match!\nPlease try again!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return

class changeCard(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(changeCard, self).__init__(mainWidget, parent)
        self.id = 'changeCard'
        self.swipeActive = True
        self.cardString = ' '

        self.input = 0

        self.titleString = ['Hi {name}!\nTo register a new card please swipe it now!',
                            'Please swipe again to finally change your card!']
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(titleLabel)
        vbox.addStretch(1)
        
        self.setLayout(vbox)

    def swipeAction(self):
        if self.input == 0:
            if self.cardSequence[0] == 'æ':
                self.cardString = self.cardSequence
                self.titleLabel.setText(self.titleString[1])
                self.input = 1
            else:
                self.errorDialog()
                self.update()
        elif self.input == 1:
            if self.cardSequence[0] == 'æ':
                if self.cardSequence == self.cardString:
                    self.mainWidget.currentUser.cardId = self.cardSequence
                    self.mainWidget.currentUser.saveUser()
                    self.mainWidget.changeUI('loggedIn')
                else:
                    self.errorDialog()
                    self.update()
            else:
                self.input = 0
                self.errorDialog()
                self.update()
                    

    def update(self):
        super().update()
        name = self.mainWidget.currentUser.name
        self.titleLabel.setText(f"Hi {name}!\nTo register a new card please swipe it now!")
        self.input = 0

    def errorDialog(self):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        if self.input == 0:
            msg.setText("Your card was not recognized as\na student card!")
        else:
            msg.setText("Sorry, but the swiped cards didn't match!\nPlease try again!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return

class payMode(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(payMode, self).__init__(mainWidget, parent)
        self.id = 'payMode'

        self.extraAmount = 50

        self.titleString = 'Scan this to pay your balance{operator} {extraAmount} kr,\nthat is {totalAmount} kr'
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))
        self.titleLabel = titleLabel

        qrPixmap = QtGui.QPixmap(resourceFolder + 'qrcode.png').scaledToHeight(300)
        
        qrLabel = QtWidgets.QLabel(self)
        qrLabel.setPixmap(qrPixmap)
        qrLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))
        self.qrLabel = qrLabel

        minusBtn = expandButton(self)
        minusBtn.setText('- 50')
        minusBtn.clicked.connect(lambda: self.updateQr('minus'))
        
        balBtn = expandButton(self)
        balBtn.setText('Exact balance')
        balBtn.clicked.connect(lambda: self.updateQr('balance'))
        
        plusBtn = expandButton(self)
        plusBtn.setText('+ 50')
        plusBtn.clicked.connect(lambda: self.updateQr('plus'))

        grid = QtWidgets.QGridLayout(self)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 3)
        grid.setRowStretch(3, 1)
        grid.addWidget(titleLabel, 1, 1, 1, 4)
        grid.addWidget(qrLabel, 2, 1, 1, 4)
        grid.addWidget(minusBtn, 3, 0, 1, 2)
        grid.addWidget(balBtn, 3, 2, 1, 2)
        grid.addWidget(plusBtn, 3, 4, 1, 2)

        self.setLayout(grid)

    def updateQr(self, operator):
        user = self.mainWidget.currentUser
        if operator == 'plus':
            self.extraAmount += 50
        elif operator == 'minus':
            self.extraAmount -= 50
            if self.extraAmount + user.balance < 0:
                self.extraAmount = - user.balance
        else:
            self.extraAmount = 0

        totalAmount = self.extraAmount + user.balance
        
        if self.extraAmount < 0:
            self.titleLabel.setText(f'Scan this to pay your balance minus {-self.extraAmount} kr,\nthat is {totalAmount} kr')
        else:
            self.titleLabel.setText(f'Scan this to pay your balance plus {self.extraAmount} kr,\nthat is {totalAmount} kr')

        qrPath = mailFuncs.generateQR(user, self.extraAmount)
        
        qrPixmap = QtGui.QPixmap(qrPath).scaledToHeight(300)
        self.qrLabel.setPixmap(qrPixmap)

    def update(self):
        user = self.mainWidget.currentUser
        operator = ' plus'
        self.extraAmount = 50
        totalAmount = user.balance + self.extraAmount
        qrPath = mailFuncs.generateQR(user, self.extraAmount)
        
        qrPixmap = QtGui.QPixmap(qrPath).scaledToHeight(300)

        self.qrLabel.setPixmap(qrPixmap)
        self.titleLabel.setText(f'Scan this to pay your balance{operator} {self.extraAmount} kr,\nthat is {totalAmount} kr')
        pass
        
def main():
    pass
    
if __name__ == '__main__':
    main()
