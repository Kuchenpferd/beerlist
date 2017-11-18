#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from loremipsum import get_paragraph, get_sentence
from PyQt4 import QtGui, QtCore

        
class Example(QtGui.QWidget):
    
    def __init__(self, parent = None):
        super(Example, self).__init__(parent)
        self.setGeometry(0,0,800,480)
        
        self.mainUI()

    def mainUI(self):
        btn = QtGui.QPushButton('Next', self)
        btn.clicked.connect

        
        l1 = QtGui.QLabel()
        l2 = QtGui.QLabel()
        
        l1.setText(get_sentence(True))
        l2.setText(get_sentence(True) + get_sentence(True) + get_sentence(True) + get_sentence(True) + '\n\n' + get_sentence(True))
        
        l2.setWordWrap(True)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addStretch()
        vbox.addWidget(l2)
        vbox.addStretch()
        

        self.setLayout(vbox)

class mainWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        self.setGeometry(50,50,800,480)
        self.setWindowTitle('Labels?')

        self.widgetStack = QtGui.QStackedWidget(self)
        self.widgetStack.setGeometry(0,0,800,480)
        
        UI = QtGui.QWidget(self.widgetStack)
        UI.setGeometry(0,0,800,480)
        
        self.widgetStack.addWidget(UI)
        self.widgetStack.setCurrentWidget(UI)
        
        self.mainUI(UI)

    def changeScreen(self, oldUI, newFuncUI):
        
        self.widgetStack.removeWidget(oldUI)
        oldUI.destroy()

        UI = QtGui.QWidget(self.widgetStack)
        UI.setGeometry(0,0,800,480)

        self.widgetStack.addWidget(UI)
        self.widgetStack.setCurrentWidget(UI)

        newFuncUI(UI)
        
        

    def mainUI(self, UI):
        
        btn = QtGui.QPushButton('Next', self)
        btn.clicked.connect(lambda: self.changeScreen(UI,self.secUI))

        
        l1 = QtGui.QLabel()
        l2 = QtGui.QLabel()
        
        l1.setText(get_sentence(True))
        l2.setText(get_sentence(True) + get_sentence(True) + get_sentence(True) + get_sentence(True) + '\n\n' + get_sentence(True))
        
        l2.setWordWrap(True)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addStretch(2)
        vbox.addWidget(l2)
        vbox.addStretch()
        vbox.addWidget(btn)
        

        UI.setLayout(vbox)
        self.show()

    def secUI(self, UI):
                
        btn = QtGui.QPushButton('Next', self)
        btn.clicked.connect(lambda: self.changeScreen(UI,self.mainUI))

        
        l1 = QtGui.QLabel()
        l2 = QtGui.QLabel()
        
        l1.setText('I did nawt!')
        l2.setText('What is going on!??!')
        
        l2.setWordWrap(True)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(l1)
        vbox.addWidget(l2)
        vbox.addStretch(2)
        vbox.addWidget(btn)
        

        UI.setLayout(vbox)
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
