#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import inputWidgets
from genUIs import expandButton, standardUI
from PyQt5 import QtWidgets, QtCore

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

        self.input = 'sduId'

        keyBoard = inputWidgets.inputFrame('full', self)
        keyBoard.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = ['Please enter your SDU-ID:',
                            'Please enter your full name:',
                            'Please enter your preferred SDU-ID:',
                            'Please enter your sdu email:',
                            'Please enter a password (min. 6 chars):',
                            'Please enter the password again']

        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString[0])
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        titleLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))
        self.titleLabel = titleLabel

        empBtn = expandButton(self)
        empBtn.setText('Employee')
        empBtn.clicked.connect(self.employeeMode)
        self.empBtn = empBtn

        inputEdit = QtWidgets.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        self.inputEdit = inputEdit
        
        grid = QtWidgets.QGridLayout(contentFrame)
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
        self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.inputEdit.setFocus(True)

    def enterAction(self):
        if self.input == 'sduId':
            self.input = 'name'

            self.titleLabel.setText(self.titleString[1])

            self.empBtn.hide()

            self.grid.removeWidget(self.titleLabel)
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.grid.addWidget(self.titleLabel, 0, 0, 1, 4)
            self.inputEdit.setFocus(True)  
            
        elif self.input == 'sduIdAlt':
            self.input = 'name'

            self.titleLabel.setText(self.titleString[1])
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.inputEdit.setFocus(True)  
        
        elif self.input == 'name':
            self.input = 'mail'

            self.titleLabel.setText(self.titleString[3])
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.inputEdit.setFocus(True)  

        elif self.input == 'mail':
            self.input = 'firstPwd'

            self.titleLabel.setText(self.titleString[4])
            self.inputEdit.setEchoMode(QtWidgets.QLineEdit.Password)
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
        nextBtn.clicked.connect(lambda: self.changePage('next'))
        self.nextBtn = nextBtn
        
        prevBtn = expandButton(self)
        prevBtn.setText('Previous page!')
        prevBtn = changeFont(prevBtn, 12, True, 'c')
        prevBtn.clicked.connect(lambda: self.changePage('prev'))
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

    def changePage(self, direction):
        self.mainWidget.changeUI('newUserBalance')

class newUserBalance(standardUI):

    def __init__(self, mainWidget, parent = None):
        super(newUserBalance, self).__init__(mainWidget, parent)
        self.id = 'newUserBalance'

        numPad = inputWidgets.inputFrame('numpad', self)
        numPad.enterBtn.clicked.connect(self.enterAction)

        contentFrame = QtWidgets.QFrame(self)
        contentFrame.setFrameShape(0)
        contentFrame.setGeometry(100, 0, 600, 100)

        self.titleString = 'Please enter your current balance:'
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.titleString)
        titleLabel = changeFont(titleLabel, 12, True, 'c')
        self.titleLabel = titleLabel

        inputEdit = QtWidgets.QLineEdit(self)
        inputEdit = changeFont(inputEdit, 12, False, 'c')
        inputEdit.setMaxLength(5)
        self.inputEdit = inputEdit
        
        vbox = QtWidgets.QVBoxLayout(contentFrame)
        vbox.addWidget(titleLabel)
        vbox.addWidget(inputEdit)
        
        contentFrame.setLayout(vbox)

    def enterAction(self):
        self.mainWidget.changeUI('newUserFinal')

    def update(self):
        self.inputEdit.setText('')
        self.inputEdit.setFocus(True)
        # A dialog box to determine the sign should go here

class newUserFinal(standardUI):
    def __init__(self, mainWidget, parent = None):
        super(newUserFinal, self).__init__(mainWidget, parent, False, False)
        self.id = 'newUserFinal'

        titleString = 'Is the following information correct?'
        
        titleLabel = QtWidgets.QLabel(self)
        titleLabel = changeFont(titleLabel, 14, True, 'c')
        titleLabel.setText(titleString)
        
        yesBtn = expandButton(self)
        yesBtn.setText('Yes!')
        yesBtn.clicked.connect(lambda: self.mainWidget.changeUI('mainMenu'))

        noBtn = expandButton(self)
        noBtn.setText('No!')
        noBtn.clicked.connect(lambda: self.mainWidget.changeUI('newUserInitial'))

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
        
def main():
    pass
    
if __name__ == '__main__':
    main()
