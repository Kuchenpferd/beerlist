#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from loremipsum import get_paragraph, get_sentence
from PyQt4 import QtGui, QtCore
from random import randint

# A sub class for the standard UI
class standardUI(QtGui.QWidget):
    def __init__(self, parent = None):
        super(standardUI, self).__init__(parent)
        self.setGeometry(0,0,800,480)

        # Each UI will have it's own id, but the standard subclass wil have the label 'None'
        self.id = 'None'

    # A function that updates the UI, will be empty for static UIs, and content will be
    # specified as each UI is set up
    def update(self):
        pass

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
        
# The class for the main window, which is the main container of everything
class mainWindow(QtGui.QWidget):

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)

        # The geometry is set up
        self.setGeometry(50,50,800,480)

        # An instance of stacked widget is set up
        self.widgetStack = QtGui.QStackedWidget(self)
        self.widgetStack.setGeometry(0,0,800,480)

        # Each UI is set up
        mainUI = genMainUI(self)
        secUI = genSecUI(self)

        # .. and then added to the widget stack
        self.widgetStack.addWidget(mainUI)
        self.widgetStack.addWidget(secUI)

        # The main UI is set as the current widget and everything is shown
        self.widgetStack.setCurrentWidget(mainUI)
        self.show()

        

    # A function that changes the active UI to whichever UI matches idUI
    def changeUI(self, idUI):

        # Finding the UI matching idUI
        for indexUI in range(0,self.widgetStack.count()):
            testUI = self.widgetStack.widget(indexUI)
            if testUI.id == idUI:
                UI = testUI

        # The UI is updated
        UI.update()        

        # .. and then set to be the active UI
        self.widgetStack.setCurrentWidget(UI)
        

# The usual main function, followed by the check that this file only can be run
# if it is not loaded as a module
def main():
    app = QtGui.QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
