#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import inputWidgets
import userFuncs, refFuncs, mailFuncs
from genUIs import expandButton, swipeLineEdit, standardUI
from hashlib import sha256
from math import ceil
from copy import deepcopy
from PyQt5 import QtWidgets, QtCore

contact = 'mikkc13'
workFolder = './../'
resourceFolder = workFolder + 'Resources/'

changeFont = inputWidgets.changeFont

# List of UI ids:
uiIdList = ['newUserInitial', 'newUserCard', 'newUserOldUsers',
            'newUserBalance', 'newUserFinal']

class newUserInitial(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(newUserInitial, self).__init__(mainWidget, parent)
        self.id = 'newUserInitial'

        self.pwd = ' '

        self.input = 'sduId'

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        titleLabel = QtWidgets.QLabel(self)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))
        self.titleLabel = titleLabel

        empBtn = expandButton(self)
        empBtn.setText('Employee')
        empBtn.clicked.connect(lambda: self.updateMode('sduIdAlt'))
        self.empBtn = empBtn

        inputEdit = swipeLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        grid = QtWidgets.QGridLayout(contentFrame)
        grid.addWidget(titleLabel, 0, 0, 1, 3)
        grid.addWidget(empBtn, 0, 3)
        grid.addWidget(inputEdit, 1, 0, 1, 4)

        self.grid = grid
        contentFrame.setLayout(grid)

    def update(self):
        self.updateMode('sduId')
        self.pwd = ' '

        if self.mainWidget.lastWidgetId == 'newUserFinal':
            self.mainWidget.lastWidgetId = 'mainMenu'

        emptyCard = self.mainWidget.currentUser.cardId is not None
        if 'newUser' not in self.mainWidget.lastWidgetId and emptyCard:
            cardId = self.mainWidget.currentUser.cardId
        else:
            cardId = None
        self.mainWidget.currentUser = refFuncs.refUserInstance()
        self.mainWidget.currentUser.cardId = cardId
        self.mainWidget.currentRefUserList = []
        self.mainWidget.transfer = []

    def updateMode(self, inputMode):
        if inputMode == 'sduId':
            self.input = 'sduId'
        
            self.empBtn.show()
            self.grid.removeWidget(self.titleLabel)
            self.grid.addWidget(self.titleLabel, 0, 0, 1, 3)
            
            self.titleLabel.setText('Please enter your SDU-ID:')
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            
        elif inputMode == 'sduIdAlt':
            self.input = 'sduIdAlt'

            self.empBtn.hide()
            self.grid.removeWidget(self.titleLabel)
            self.grid.addWidget(self.titleLabel, 0, 0, 1, 4)

            self.titleLabel.setText('Please enter your preferred SDU-ID:')

        elif inputMode == 'mail':
            self.input = 'mail'

            self.titleLabel.setText('Please enter your sdu email:')

        elif inputMode == 'name':
            self.input = 'name'

            self.empBtn.hide()
            self.grid.removeWidget(self.titleLabel)
            self.grid.addWidget(self.titleLabel, 0, 0, 1, 4)

            self.titleLabel.setText('Please enter your full name:')

        elif inputMode == 'firstPwd':
            self.input = 'firstPwd'

            self.empBtn.hide()
            self.grid.removeWidget(self.titleLabel)
            self.grid.addWidget(self.titleLabel, 0, 0, 1, 4)

            self.titleLabel.setText('Please enter a password (min. 6 chars):')
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            

        elif inputMode == 'secPwd':
            self.input = 'secPwd'

            self.titleLabel.setText('Please enter the password again')

        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)


    def enterAction(self):
        currentUser = self.mainWidget.currentUser
        if self.input == 'sduId':

            sduId = self.inputEdit.text().lower()

            if sduId is '':
                self.errorDialog('The prompt appears to be empty!')
                self.updateMode('sduId')
                return

            elif userFuncs.findUserNoCard(sduId) is not None:
                self.errorDialog('The entered SDU-ID is already in use!')
                self.updateMode('sduId')
                return

            elif not userFuncs.validSduId(sduId):
                self.errorDialog('The format of the SDU-ID was wrong!\nThe allowed formats are "abcde12" or "abcd123"!')
                self.updateMode('sduId')
                return

            name = refFuncs.findName(sduId)
            refUser, refUserList = refFuncs.findRefUser(sduId)
            self.mainWidget.currentRefUserList = refUserList

            try:
                if name is not None:
                    refUser.name = name
                self.errorDialog(f"""Hi {refUser.name},\nYou previously had a balance of {refUser.balance}.\nWelcome to the new system!""")
                currentUser.name = refUser.name
                currentUser.sduId = refUser.sduId
                currentUser.mail = f'{refUser.sduId}@student.sdu.dk'
                currentUser.balance = refUser.balance
                self.updateMode('firstPwd')

            except AttributeError:
                if name is not None:
                    self.errorDialog(f"""Hi {name},\nWe found your name using your SDU-ID!""")
                    currentUser.name = name
                    currentUser.sduId = sduId
                    currentUser.mail = f'{sduId}@student.sdu.dk'
                    self.updateMode('firstPwd')
                else:
                    self.errorDialog("""Sorry we couldn't find your name automatically,\nPlease enter it manually!""")
                    currentUser.sduId = sduId
                    currentUser.mail = f'{sduId}@student.sdu.dk'
                    self.updateMode('name')
                
        elif self.input == 'sduIdAlt':

            sduId = self.inputEdit.text().lower()

            if sduId is '':
                self.errorDialog('The prompt appears to be empty!')
                self.updateMode('sduIdAlt')
                return

            elif userFuncs.findUserNoCard(sduId) is not None:
                self.errorDialog('The entered SDU-ID is already in use!')
                self.updateMode('sduIdAlt')
                return

            name, mail = refFuncs.findEmpolyee(sduId)
            if name is None:
                name = refFuncs.findName(sduId)
            refUser, refUserList = refFuncs.findRefUser(sduId)
            self.mainWidget.currentRefUserList = refUserList
            
            try:
                if name is not None:
                    refUser.name = name
                    if mail is not None:
                        refUser.mail = mail
                    else:
                        refUser.mail = f'{sduId}@student.sdu.dk'
                self.errorDialog(f"""Hi {refUser.name},\nYou previously had a balance of {refUser.balance}.\nWelcome to the new system!""")
                currentUser.name = refUser.name
                currentUser.sduId = refUser.sduId
                currentUser.mail = refUser.mail
                currentUser.balance = refUser.balance
                self.updateMode('firstPwd')

            except AttributeError:
                if name is not None:
                    if mail is None:
                        mail = f'{sduId}@student.sdu.dk'
                    self.errorDialog(f"""Hi {name},\nWe found your name using your SDU-ID!""")
                    currentUser.name = name
                    currentUser.sduId = sduId
                    currentUser.mail = mail
                    self.updateMode('firstPwd')
                else:
                    self.errorDialog("""Sorry we couldn't find your mail automatically,\nPlease enter it manually!""")
                    currentUser.sduId = sduId
                    self.updateMode('mail')

            if refUser is not None:
                self.errorDialog(f"""Hi {refUser.name},\n
                                     You previously had a balance of {refUser.balance}.\n
                                     Welcome to the new system!""")
                currentUser.name = refUser.name
                currentUser.balance = refUser.balance

        
        elif self.input == 'mail':

            mail = self.inputEdit.text().lower()
            mailComp = mail.split('@')

            if len(mailComp) is not 2 or len(mailComp[0]) is 0:
                self.errorDialog('Your mail should follow the format "some@thing.sdu.dk"!')
                self.updateMode('mail')

            elif 'sdu.dk' not in mail:
                self.errorDialog('Please enter an SDU mail!')
                self.updateMode('mail')

            else:
                currentUser.mail = mail
                self.updateMode('name')

        elif self.input == 'name':
            
            name = self.inputEdit.text().title()

            if name is '':
                self.errorDialog('The prompt appears to be empty!')
                self.updateMode('firstPwd')

            elif len(name.split()) < 2:
                self.errorDialog('You need to enter at least two names!')
                self.updateMode('firstPwd')

            else:
                currentUser.name = name
                self.updateMode('firstPwd')

        elif self.input == 'firstPwd':

            self.pwd = self.inputEdit.text()

            if len(self.pwd) < 6:
                self.errorDialog('Please use at least six characters!')
                self.updateMode('firstPwd')
            elif ' ' in self.pwd:
                self.errorDialog('Your password should not contain spaces!')
                self.updateMode('firstPwd')
            else:
                self.updateMode('secPwd')

        elif self.input == 'secPwd':

            pwd = self.inputEdit.text()

            if pwd != self.pwd:
                self.errorDialog("The passwords doesn't match!\nPlease try again!")
                self.updateMode('firstPwd')
                return
            
            currentUser.pwd = sha256(pwd.encode()).hexdigest()

            if self.mainWidget.currentUser.balance is None:
                if self.balanceDialog():
                    return
                self.mainWidget.currentUser.balance = 0

            if self.mainWidget.currentUser.cardId is None:
                self.mainWidget.changeUI('newUserCard')

            else:
                self.mainWidget.changeUI('newUserFinal')
    
    def errorDialog(self, errorText):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText(errorText)
       
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return

    def balanceDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(220,180)
        msg.setText('Did you previously have a non-zero balance?')
        msg.setStandardButtons(QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('newUserOldUsers')
            return True
        return False


class newUserOldUsers(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(newUserOldUsers, self).__init__(mainWidget, parent, backButton = False)
        self.id = 'newUserOldUsers'

        self.titleString = 'Please find try to find yourself on the list:'

        self.pageNo = 0
        self.noItems = 8
        self.lastPageNo = 0
        self.refUserList = []
        self.pageList = []

        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))

        headerString = ['Name:',
                         'Mail:',
                         'Balance:']

        headerLabel = [QtWidgets.QLabel(self), QtWidgets.QLabel(self), QtWidgets.QLabel(self)]

        for i in range(3):
            headerLabel[i].setText(headerString[i])
            headerLabel[i] = changeFont(headerLabel[i], 10, True)
            #headerLabel[i].setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))

        nextBtn = expandButton(self)
        nextBtn.setText('Next page!')
        nextBtn = changeFont(nextBtn, 12, True, 'c')
        nextBtn.clicked.connect(lambda: self.changePage(1))
        self.nextBtn = nextBtn
        
        prevBtn = expandButton(self)
        prevBtn.setText('Previous page!')
        prevBtn = changeFont(prevBtn, 12, True, 'c')
        prevBtn.clicked.connect(lambda: self.changePage(-1))
        self.prevBtn = prevBtn
        
        grid = QtWidgets.QGridLayout(self)
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
            
            nameLabels.append(QtWidgets.QLabel(self))
            nameLabels[i].setText('{name}')
            nameLabels[i] = changeFont(nameLabels[i], 10)
            
            mailLabels.append(QtWidgets.QLabel(self))
            mailLabels[i].setText('{mail}')
            mailLabels[i] = changeFont(mailLabels[i], 10)
            
            balanceLabels.append(QtWidgets.QLabel(self))
            balanceLabels[i].setText('{balance}')
            balanceLabels[i] = changeFont(balanceLabels[i], 10)

            meBtns.append(expandButton(self))
            meBtns[i].setText('Me!')
            meBtns[i] = changeFont(meBtns[i], 10)
            meBtns[i].clicked.connect(lambda: self.foundActionDialog(None))

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

    def update(self):
        self.refUserList = refFuncs.loadRefUsers()

        pageList = []
        shortList = []
        for refUser in self.refUserList:

            if len(shortList) == self.noItems:
                pageList.append(shortList)
                shortList = []

            shortList.append(refUser)

        while True:
            if len(shortList) != self.noItems:
                shortList.append(None)
            else:
                break

        self.lastPageNo = len(pageList) - 1
        self.pageList = pageList
        self.pageNo = 0

        self.changePage(-1)

    def changePage(self, direction):
        
        self.pageNo += direction
        self.nextBtn.clicked.disconnect()

        if self.pageNo <= 0:
            self.prevBtn.hide()
            self.nextBtn.clicked.connect(lambda: self.changePage(1))
            if self.pageNo < 0:
                self.pageNo -= direction

        elif self.pageNo >= self.lastPageNo:
            self.nextBtn.setText("I'm not here!?")
            self.nextBtn.clicked.connect(self.notThereDialog)
            self.pageNo -= direction

        else:
            self.nextBtn.setText('Next page!')
            self.nextBtn.clicked.connect(lambda: self.changePage(1))
            self.prevBtn.show()

        shortList = self.pageList[self.pageNo]

        nameLabels = self.nameLabels
        mailLabels = self.mailLabels
        balanceLabels = self.balanceLabels
        meBtns = self.meBtns

        for i in range(self.noItems):
            refUser = shortList[i]
            if refUser is not None:
                nameLabels[i].setText(f'{refUser.name}')
                mailLabels[i].setText(f'{refUser.mail}')
                balanceLabels[i].setText(f'{refUser.balance}')
                meBtns[i].clicked.disconnect()
                meBtns[i].clicked.connect(self.foundActionDialog)

                nameLabels[i].show()
                mailLabels[i].show()
                balanceLabels[i].show()
                meBtns[i].show()
            else:
                nameLabels[i].hide()
                mailLabels[i].hide()
                balanceLabels[i].hide()
                meBtns[i].hide()

    def foundActionDialog(self):
        for i, btn in enumerate(self.meBtns):
            if btn is self.sender():
                refUser = self.pageList[self.pageNo][i]
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(220,180)
        msg.setText(f'Oh, so you are {refUser.name.split()[0]},\nwith a balance of {refUser.balance}?')
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.currentUser.balance = refUser.balance
            self.mainWidget.currentRefUserList = self.refUserList.remove(refUser)

            if self.mainWidget.currentUser.cardId is None:
                self.mainWidget.changeUI('newUserCard')

            else:
                self.mainWidget.changeUI('newUserFinal')

    def notThereDialog(self):
        
        # A message box is set up with a text and two buttons
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(220,180)
        msg.setText("Sorry, you will have to enter it manually then.\nAre you sure you're not there?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # msg.exec_() will return the value of the pressed button
        pressedButton = msg.exec_()

        # A check to see if the 'Yes' button was pressed, and the UI is then changed
        if pressedButton == QtWidgets.QMessageBox.Yes:
            self.mainWidget.changeUI('newUserBalance')
            



class newUserBalance(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(newUserBalance, self).__init__(mainWidget, parent, backButton = False)
        self.id = 'newUserBalance'

        numPad = inputWidgets.inputFrame('numpad', self)
        numPad.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = 'Please enter your current balance:\n(Sign will be added later)'
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = swipeLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        inputEdit.setMaxLength(5)
        self.inputEdit = inputEdit
        
        vbox = QtWidgets.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def update(self):
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)

    def enterAction(self):

        balance = int(self.inputEdit.text())

        if balance >= 900:
            self.errorDialog(f'Sorry, but that seems very unlikely!\nPlease try again or contact {contact}!')
            self.update()
            return

        elif self.enterActionDialog():
            balance = - balance

        self.mainWidget.currentUser.balance = balance

        self.mainWidget.transfer = 'ManBalance'

        if self.mainWidget.currentUser.cardId is None:
            self.mainWidget.changeUI('newUserCard')

        else:
            self.mainWidget.changeUI('newUserFinal')

    def enterActionDialog(self):
        # A message box is set up with a text and two buttons
            msg = QtWidgets.QMessageBox(self.mainWidget)
            msg = changeFont(msg, 12, True)
            msg.move(220,180)
            msg.setText('Was the sign of your balance "+" (Yes) or "-" (No)')
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            # msg.exec_() will return the value of the pressed button
            pressedButton = msg.exec_()

            # A check to see if the 'Yes' button was pressed, and the UI is then changed
            if pressedButton == QtWidgets.QMessageBox.Yes:
                return False

            else:
                return True

    def errorDialog(self, errorText):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText(errorText)
       
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return


class newUserCard(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(newUserCard, self).__init__(mainWidget, parent, backButton = False)
        self.id = 'newUserCard'
        self.swipeActive = True

        self.input = 0
        self.swipeOne = ' '

        self.titleString = ['Hi {name}!\nPlease swipe your card!',
                            'Please swipe it again!']
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(titleLabel)
        vbox.addStretch(1)
        
        self.setLayout(vbox)

    def update(self):
        super().update()
        name = self.mainWidget.currentUser.name
        self.titleLabel.setText(f'Hi {name}!\nPlease swipe your card!')
        self.input = 0

    def swipeAction(self):
        if self.input == 0:
            self.titleLabel.setText(self.titleString[1])
            self.swipeOne = self.cardSequence
            self.input = 1

        elif self.input == 1:
            if self.swipeOne == self.cardSequence:
                self.mainWidget.currentUser.cardId = self.cardSequence
                self.mainWidget.changeUI('newUserFinal')
            else:
                self.errorDialog("Sorry, but the two swipes didn't match!\nPlease try again!")
                self.update()

    def errorDialog(self, errorText):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText(errorText)
       
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return


class newUserFinal(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(newUserFinal, self).__init__(mainWidget, parent, backButton = False, menuButton = False)
        self.id = 'newUserFinal'

        titleString = 'Is the following information correct?'
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel = changeFont(titleLabel, 14, True, 'c')
        titleLabel.setText(titleString)
        
        yesBtn = expandButton(self)
        yesBtn.setText('Yes!')
        yesBtn.clicked.connect(self.yesPressed)

        noBtn = expandButton(self)
        noBtn.setText('No!')
        noBtn.clicked.connect(self.noPressedDialog)

        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(titleLabel, 0, 0, 1, 4)
        grid.addWidget(noBtn, 6, 0, 1, 3)
        grid.addWidget(yesBtn, 6, 3)

        contentString = [('Name:', '{name}'), ('SDU-ID:', '{sduId}'), ('Mail:', '{mail}'), ('Balance:', '{balance}')]

        contentLabel = []
        self.contentLabel = contentLabel
                       
        for i in range(4):
            tagLabel = QtWidgets.QLabel(self)
            tagLabel = changeFont(tagLabel, 12, True)
            tagLabel.setText(contentString[i][0])

            contentLabel.append(QtWidgets.QLabel(self))
            contentLabel[i] = changeFont(contentLabel[i], 12)
            contentLabel[i].setText(contentString[i][1])

            grid.addWidget(tagLabel, i + 1, 1)
            grid.addWidget(contentLabel[i], i + 1, 2)
            grid.setRowStretch(i, 1)
            
        grid.setRowStretch(0, 1)
        grid.setRowStretch(5, 1)
        grid.setRowStretch(6, 1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,1)
        grid.setColumnStretch(3,3)

        self.setLayout(grid)

    def update(self):
        user = self.mainWidget.currentUser
        contentString = [f'{user.name}', f'{user.sduId}', f'{user.mail}', f'{user.balance}']

        for i in range(4):
            self.contentLabel[i].setText(contentString[i])

    def yesPressed(self):
        refUserList = self.mainWidget.currentRefUserList
        refUser = self.mainWidget.currentUser
        user = userFuncs.refToMainUser(refUser)
        user.saveUser()
        if self.mainWidget.transfer == 'ManBalance':
            self.mainWidget.transfer = []
            mailFuncs.sendMail(user, 'ManBalance')
        if refUserList != []:
            refFuncs.saveRefUsers(refUserList)
        self.errorDialog('Great, your user has now been created!\nPlease note that this does not include a first swipe!')
        self.mainWidget.changeUI('mainMenu')

    def noPressedDialog(self):
        # A message box is set up with a text and two buttons
            msg = QtWidgets.QMessageBox(self.mainWidget)
            msg = changeFont(msg, 12, True)
            msg.move(220,180)
            msg.setText('Are you sure?\nYou will have to start over!')
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            # msg.exec_() will return the value of the pressed button
            pressedButton = msg.exec_()

            # A check to see if the 'Yes' button was pressed, and the UI is then changed
            if pressedButton == QtWidgets.QMessageBox.Yes:
                self.mainWidget.changeUI('newUserInitial')

    def errorDialog(self, errorText):
        
        # A message box is set up with a text and a button
        msg = QtWidgets.QMessageBox(self.mainWidget)
        msg = changeFont(msg, 12, True)
        msg.move(280,100)
        msg.setText(errorText)
       
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        msg.exec_()
        return

        
def main():
    pass
    
if __name__ == '__main__':
    main()
