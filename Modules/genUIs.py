#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import inputWidgets
from PyQt4 import QtGui, QtCore

workFolder = './../'
resourceFolder = workFolder + 'Resources/'

# List of UI ids:
uiIdList = ['None', 'mainMenu', 'multiMode', 'markDone', 'resetPwd',
            'login', 'loggedIn', 'changePwd', 'changeCard', 'payMode',
            'newUserInitial', 'newUserCard', 'newUserOldUsers',
            'newUser-balance', 'newUser-final']

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

class expandButton(QtGui.QPushButton):
    def __init__(self, parent = None):
        super(expandButton, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
        self = changeFont(self, 12, True)

# A super class for the standard UI
class standardUI(QtGui.QWidget):
    def __init__(self, mainWidget, parent = None, backButton = True, menuButton = True):
        super(standardUI, self).__init__(parent)
        self.setGeometry(0,0,800,480)
        self.mainWidget = mainWidget
        self.id = 'None'

        self.cardSequence = ''
        self.swipeActive = False

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
        msg = changeFont(msg, 12, True)
        msg.setGeometry(225,210,60,30)
        msg.setText('Do you want to return to the main menu?')
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtGui.QMessageBox.Yes:
            self.mainWidget.changeUI('mainMenu')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtGui.QMessageBox.No:
            self.update()
        
    def backDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtGui.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.setGeometry(220,210,60,30)
        msg.setText('Do you want to return to previous screen?')
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtGui.QMessageBox.Yes:
            self.mainWidget.changeUI('back')

        # Another check to so if the 'No' button was pressed
        elif pressedButton == QtGui.QMessageBox.No:
            self.update()
    
    def swipeAction(self):
        print(self.cardSequence)
        pass
    
    # A function that updates the UI, will be empty for static UIs, and content will be
    # specified as each UI is set up
    def update(self):
        pass

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

        titleLabel = QtGui.QLabel(self)
        titleLabel.setText('Welcome to Æters Beerlist system v. 2.0')
        titleLabel = changeFont(titleLabel, 14, True, 'c')

        contentLabel = QtGui.QLabel(self)
        contentLabel.setText('To grab a beer or soda please swipe your card!\nTo grab multiple, press "Multi Mode"!\nTo create a new user swipe your card or press "New User"!\nTo see your balance, grab beers without your card,\nchange your password or card, please login!')
        contentLabel = changeFont(contentLabel)

        grid = QtGui.QGridLayout()
        grid.addWidget(titleLabel, 0, 1, 1, 2)
        grid.addWidget(contentLabel, 1, 1, 1, 2)
        grid.addWidget(multiBtn, 2, 0, 1, 2)
        grid.addWidget(loginBtn, 2, 2, 1, 2)
        grid.addWidget(newUserBtn, 3, 0, 1, 2)
        grid.addWidget(resetBtn, 3, 2, 1, 2)

        self.setLayout(grid)



class multiMode(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(multiMode, self).__init__(mainWidget, parent)
        self.id = 'multiMode'
        self.swipeActive = True

        numPad = inputWidgets.inputFrame('numpad', self)
        numPad.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtGui.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please enter the wanted amount and swipe your card:',
                            'Please enter the wanted amount and press enter:']
        
        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = QtGui.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        inputEdit.setMaxLength(2)
        self.inputEdit = inputEdit
        
        vbox = QtGui.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def enterAction(self):
        self.mainWidget.changeUI('markDone')

    def update(self):
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

class markDone(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(markDone, self).__init__(mainWidget, parent, False, False)
        self.id = 'markDone'

        self.contentString = 'Hi {name}!\n{amount} kr was added to your balance, which is now {balance} kr!\nRemember to pay your debt regularly!'
        
        contentLabel = QtGui.QLabel(self)
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

        grid = QtGui.QGridLayout(self)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,2)
        grid.setRowStretch(2,2)
        grid.setRowStretch(3,1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(3,1)
        grid.addWidget(contentLabel, 1, 1, 1, 2)
        grid.addWidget(payBtn, 2, 1)
        grid.addWidget(menuBtn, 2, 2)

        self.setLayout(grid)

class resetPwd(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(resetPwd, self).__init__(mainWidget, parent)
        self.id = 'resetPwd'

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtGui.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        titleString = 'Please enter your SDU-ID to reset your password:'

        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')

        inputEdit = QtGui.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        vbox = QtGui.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def update(self):
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

    def enterAction(self):
        pass

class login(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(login, self).__init__(mainWidget, parent)
        self.id = 'login'
        self.swipeActive = True

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtGui.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please enter your SDU-ID or swipe your card to login:',
                            'Please enter your password:']

        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = QtGui.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        vbox = QtGui.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def update(self):
        self.input = 0
        self.titleLabel.setText(self.titleString[0])
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)
        self.inputEdit.setEchoMode(QtGui.QLineEdit.Normal)

    def enterAction(self):
        if self.input == 0:
            self.titleLabel.setText(self.titleString[1])
            self.input = 1
            self.inputEdit.setFocus(True)
            self.inputEdit.setEchoMode(QtGui.QLineEdit.Password)
            self.inputEdit.setText('')
        elif self.input == 1:
            self.mainWidget.changeUI('loggedIn')

class loggedIn(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(loggedIn, self).__init__(mainWidget, parent)
        self.id = 'loggedIn'

        self.titleString = 'Welcome {name}!\nYour current balance is {balance} kr!\nA negative balance is a good thing!'
        
        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel
        
        oneBtn = expandButton(self)
        oneBtn.setText('One mark')
        oneBtn.clicked.connect(lambda: self.mainWidget.changeUI('markDone'))
        
        multiBtn = expandButton(self)
        multiBtn.setText('Multi mode')
        multiBtn.clicked.connect(lambda: self.mainWidget.changeUI('multiMode'))

        payBtn = expandButton(self)
        payBtn.setText('Pay')
        payBtn.clicked.connect(lambda: self.mainWidget.changeUI('payMode'))

        chnPwdBtn = expandButton(self)
        chnPwdBtn.setText('Change Password')
        chnPwdBtn.clicked.connect(lambda: self.mainWidget.changeUI('changePwd'))

        chnCardBtn = expandButton(self)
        chnCardBtn.setText('Change Card')
        chnCardBtn.clicked.connect(lambda: self.mainWidget.changeUI('changeCard'))

        grid = QtGui.QGridLayout(self)
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

class changePwd(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(changePwd, self).__init__(mainWidget, parent)
        self.id = 'changePwd'

        self.input = 0

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtGui.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please your new password:',
                            'Please enter it again:']
        
        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')

        inputEdit = QtGui.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        inputEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.inputEdit = inputEdit
        
        vbox = QtGui.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def enterAction(self):
        if self.input == 0:
            self.titleLabel.setText(self.titleString[1])
            self.input = 1
            self.inputEdit.setText('')
            self.inputEdit.setFocus(True)
        elif self.input == 1:
            self.mainWidget.changeUI('loggedIn')

    def update(self):
        self.titleLabel.setText(self.titleString[0])
        self.input = 0
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

class changeCard(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(changeCard, self).__init__(mainWidget, parent)
        self.id = 'changeCard'
        self.swipeActive = True

        self.input = 0

        self.titleString = ['Hi {name}!\nTo register a new card please swipe it now!',
                            'Please swipe again to finally change your card!']
        
        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        vbox = QtGui.QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(titleLabel)
        vbox.addStretch(1)
        
        self.setLayout(vbox)

    def swipeAction(self):
        if self.input == 0:
            self.titleLabel.setText(self.titleString[1])
            self.input = 1
        elif self.input == 1:
            self.mainWidget.changeUI('loggedIn')

    def update(self):
        self.titleLabel.setText(self.titleString[0])
        self.input = 0

class payMode(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(payMode, self).__init__(mainWidget, parent)
        self.id = 'payMode'

        self.extraAmount = 50

        self.titleString = 'Scan this to pay your balance {operator} {extraAmount} kr,\nthat is {totalAmount} kr'
        
        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))
        self.titleLabel = titleLabel

        self.qrPixmap = QtGui.QPixmap(resourceFolder + 'qrcode.png').scaledToHeight(300)
        
        qrLabel = QtGui.QLabel(self)
        qrLabel.setPixmap(self.qrPixmap)
        qrLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))

        minusBtn = expandButton(self)
        minusBtn.setText('- 50')
        minusBtn.clicked.connect(lambda: self.updateQr('minus'))
        
        balBtn = expandButton(self)
        balBtn.setText('Exact balance')
        balBtn.clicked.connect(lambda: self.updateQr('balance'))
        
        plusBtn = expandButton(self)
        plusBtn.setText('+ 50')
        plusBtn.clicked.connect(lambda: self.updateQr('plus'))

        grid = QtGui.QGridLayout(self)
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
        pass

    def update(self):
        pass

class newUserInitial(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(newUserInitial, self).__init__(mainWidget, parent)
        self.id = 'newUserInitial'

        self.input = 'sduId'

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtGui.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please enter your SDU-ID:',
                            'Please enter your full name:',
                            'Please enter your preferred SDU-ID:',
                            'Please enter your sdu email:',
                            'Please enter a password (min. 6 chars):',
                            'Please enter the password again']

        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))
        self.titleLabel = titleLabel

        empBtn = expandButton(self)
        empBtn.setText('Employee')
        empBtn.clicked.connect(self.employeeMode)
        self.empBtn = empBtn

        inputEdit = QtGui.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        grid = QtGui.QGridLayout(contentFrame)
        grid.addWidget(titleLabel, 0, 0, 1, 3)
        grid.addWidget(empBtn, 0, 3)
        grid.addWidget(inputEdit, 1, 0, 1, 4)

        self.grid = grid
        contentFrame.setLayout(grid)

    def employeeMode(self):
        self.input = 'sduIdAlt'

        self.titleLabel.setText(self.titleString[2])
        
        self.empBtn.hide()

        self.grid.removeWidget(self.titleLabel)
        self.grid.addWidget(self.titleLabel, 0, 0, 1, 4)

        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

    def update(self):
        self.input = 'sduId'
        
        self.titleLabel.setText(self.titleString[0])

        self.empBtn.show()

        self.grid.removeWidget(self.titleLabel)
        self.grid.addWidget(self.titleLabel, 0, 0, 1, 3)
        
        self.inputEdit.setText('')
        self.inputEdit.setEchoMode(QtGui.QLineEdit.Normal)
        self.inputEdit.setFocus(True)

    def enterAction(self):
        if self.input == 'sduId':
            self.input = 'name'

            self.titleLabel.setText(self.titleString[1])

            self.empBtn.hide()

            self.grid.removeWidget(self.titleLabel)
            self.inputEdit.setEchoMode(QtGui.QLineEdit.Normal)
            self.grid.addWidget(self.titleLabel, 0, 0, 1, 4)
            self.inputEdit.setFocus(True)  
            
        elif self.input == 'sduIdAlt':
            self.input = 'name'

            self.titleLabel.setText(self.titleString[1])
            self.inputEdit.setEchoMode(QtGui.QLineEdit.Normal)
            self.inputEdit.setFocus(True)  
        
        elif self.input == 'name':
            self.input = 'mail'

            self.titleLabel.setText(self.titleString[3])
            self.inputEdit.setEchoMode(QtGui.QLineEdit.Normal)
            self.inputEdit.setFocus(True)  

        elif self.input == 'mail':
            self.input = 'firstPwd'

            self.titleLabel.setText(self.titleString[4])
            self.inputEdit.setEchoMode(QtGui.QLineEdit.Password)
            self.inputEdit.setFocus(True)

        elif self.input == 'firstPwd':
            self.input = 'secPwd'

            self.titleLabel.setText(self.titleString[5])
            self.inputEdit.setFocus(True)

        elif self.input == 'secPwd':
            self.mainWidget.changeUI('newUserCard')
            
        self.inputEdit.setText('')

class newUserCard(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(newUserCard, self).__init__(mainWidget, parent)
        self.id = 'newUserCard'
        self.swipeActive = True

        self.input = 0

        self.titleString = ['Hi {name}!\nPlease swipe your card!',
                            'Please swipe it again!']
        
        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        vbox = QtGui.QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(titleLabel)
        vbox.addStretch(1)
        
        self.setLayout(vbox)

    def swipeAction(self):
        if self.input == 0:
            self.titleLabel.setText(self.titleString[1])
            self.input = 1
        elif self.input == 1:
            self.mainWidget.changeUI('newUserOldUsers')

    def update(self):
        self.titleLabel.setText(self.titleString[0])
        self.input = 0

class newUserOldUsers(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(newUserOldUsers, self).__init__(mainWidget, parent)
        self.id = 'newUserOldUsers'

        self.titleString = 'Please find try to find yourself on the list:'

        self.noItems = 8

        titleLabel = QtGui.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))

        headerString = ['Name:',
                         'Mail:',
                         'Balance:']

        headerLabel = [QtGui.QLabel(self), QtGui.QLabel(self), QtGui.QLabel(self)]

        for i in range(3):
            headerLabel[i].setText(headerString[i])
            headerLabel[i] = changeFont(headerLabel[i], 10, True)
            #headerLabel[i].setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))

        nextBtn = expandButton(self)
        nextBtn.setText('Next page!')
        nextBtn = changeFont(nextBtn, 12, True, 'c')
        self.nextBtn = nextBtn
        
        prevBtn = expandButton(self)
        prevBtn.setText('Previous page!')
        prevBtn = changeFont(prevBtn, 12, True, 'c')
        self.prevBtn = prevBtn
        
        grid = QtGui.QGridLayout(self)
        grid.addWidget(titleLabel, 0, 1, 1, 4)
        grid.addWidget(headerLabel[0], 1, 0, 1, 2)
        grid.addWidget(headerLabel[1], 1, 2, 1, 2)
        grid.addWidget(headerLabel[2], 1, 4)
        grid.addWidget(prevBtn, self.noItems + 3, 0, 1, 3)
        grid.addWidget(nextBtn, self.noItems + 3, 3, 1, 3)

        nameLabels = []
        self.nameLabels = nameLabels
        mailLabels = []
        self.mailLabels = mailLabels
        balanceLabels = []
        self.balanceLabels = balanceLabels
        meBtns = []
        self.meBtns = meBtns
        
        for i in range(self.noItems):
            grid.setRowStretch(i + 2, 1)
            
            nameLabels.append(QtGui.QLabel(self))
            nameLabels[i].setText('{name}')
            nameLabels[i] = changeFont(nameLabels[i], 10)
            
            mailLabels.append(QtGui.QLabel(self))
            mailLabels[i].setText('{mail}')
            mailLabels[i] = changeFont(mailLabels[i], 10)
            
            balanceLabels.append(QtGui.QLabel(self))
            balanceLabels[i].setText('{balance}')
            balanceLabels[i] = changeFont(balanceLabels[i], 10)

            meBtns.append(expandButton(self))
            meBtns[i].setText('Me!')
            meBtns[i] = changeFont(meBtns[i], 10)
            meBtns[i].clicked.connect(lambda: self.foundAction('id'))

            grid.addWidget(nameLabels[i], i + 2, 0, 1, 2)
            grid.addWidget(mailLabels[i], i + 2, 2, 1, 2)
            grid.addWidget(balanceLabels[i], i + 2, 4)
            grid.addWidget(meBtns[i], i + 2, 5)

        grid.setRowStretch(0, 3)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(self.noItems + 3, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)
        grid.setColumnStretch(3, 2)
        grid.setColumnStretch(4, 2)
        grid.setColumnStretch(5, 1)
        
        self.setLayout(grid)

    def foundAction(self, identifier):
        pass
            
            
            
            
    
        
def main():
    pass
    
if __name__ == '__main__':
    main()
