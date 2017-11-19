#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from loremipsum import get_paragraph, get_sentence
from PyQt4 import QtGui, QtCore

# A sub class for the standard UI, for now quite empty
class standardUI(QtGui.QWidget):
    def __init__(self, parent = None):
        super(standardUI, self).__init__(parent)
        self.setGeometry(0,0,800,480)

# A function to set up a specific UI.
# These have been written separate from the main class (see further down)
# so that UI can be put in separate files.
# It takes to inputs:
# - UI is the empty widget which should be filled with content
# - mainWidget is the current instance of the main window
def mainUI(UI, mainWidget):

    # A button to move to the next screen is set up. The clicked signal is connected
    # to a function within the main window to change UI's
    btn = QtGui.QPushButton('Next', UI)
    btn.clicked.connect(lambda: mainWidget.changeUI(UI,secUI))

    # A few labels is set up
    l1 = QtGui.QLabel(UI)
    l2 = QtGui.QLabel(UI)

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

    # At last the layout is added to the widget and a show() function is called
    # to show the widget
    UI.setLayout(vbox)
    mainWidget.show()

# Similar to the function above, but sets up a different UI
def secUI(UI, mainWidget):

    # This UI also has a button to move back to the previous UI,
    # but it is connected to a dialog option (see below)
    btn = QtGui.QPushButton('Next', UI)
    btn.clicked.connect(lambda: secToMainDialog(UI, mainWidget))

    # Once again a few labels is set up and everything is added to a VBox layout
    l1 = QtGui.QLabel(UI)
    l2 = QtGui.QLabel(UI)
        
    l1.setText('Who and where?!')
    l2.setText('What is going on!??!')
        
    l2.setWordWrap(True)

    vbox = QtGui.QVBoxLayout()
    vbox.addStretch()
    vbox.addWidget(l1)
    vbox.addWidget(l2)
    vbox.addStretch(2)
    vbox.addWidget(btn)
        
    # At last the layout is added to the widget and everything is shown
    UI.setLayout(vbox)
    mainWidget.show()

# A UI specific dialog function
def secToMainDialog(UI, mainWidget):

    # A message box is set up with a text and two buttons
    msg = QtGui.QMessageBox(mainWidget)
    msg.setGeometry(50,100,60,30)
    msg.setText('Do you want to go move on?')
    msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

    # msg.exec_() will return the value of the pressed button
    pressedButton = msg.exec_()

    # A check to see if the 'Yes' button was pressed, and the UI is then changed
    if pressedButton == QtGui.QMessageBox.Yes:
        mainWidget.changeUI(UI, mainUI)

    # Another check to so if the 'No' button was pressed
    elif pressedButton == QtGui.QMessageBox.No:
        pass
        
# The class for the main window, which is the main container of everything
class mainWindow(QtGui.QWidget):

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)

        # The geometry is set up
        self.setGeometry(50,50,800,480)

        # An instance of stacked widget is set up.
        # For this intance it seems like overkill, but later it might be useful
        self.widgetStack = QtGui.QStackedWidget(self)
        self.widgetStack.setGeometry(0,0,800,480)

        # An initial standard UI is started
        UI = standardUI(self.widgetStack)

        # The empty widget is put in the stack and set to be active
        self.widgetStack.addWidget(UI)
        self.widgetStack.setCurrentWidget(UI)

        # At last the function that sets up the content of the first UI is called
        mainUI(UI, self)

    # A function that changes the active UI from oldUI to whatever content newFuncUI sets up
    def changeUI(self, oldUI, newFuncUI):

        # First oldUI is removed from the stack and destroyed
        self.widgetStack.removeWidget(oldUI)
        oldUI.destroy()

        # Next a new empty UI is started, added to the stack, and set to be active
        UI = standardUI(self.widgetStack)
        self.widgetStack.addWidget(UI)
        self.widgetStack.setCurrentWidget(UI)

        # At last the function to set up new content for the UI is called
        newFuncUI(UI, self)

# The usual main function, followed by the check that this file only can be run
# if it is not loaded as a module
def main():
    app = QtGui.QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
