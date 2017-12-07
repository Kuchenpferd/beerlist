#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
import genUIs
import newUserUIs
import refFuncs
        
# The class for the main window, which is the main container of everything
class mainWindow(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)

        # The geometry is set up
        self.setGeometry(50,50,800,480)

        self.currentUser = refFuncs.refUserInstance()
        self.currentUserList = []
        self.currentRefUserList = []
        self.transfer = {}

        # An instance of stacked widget is set up
        self.widgetStack = QtWidgets.QStackedWidget(self)
        self.widgetStack.setGeometry(0,0,800,480)

        # Each UI is set up
        mainMenuUI = genUIs.mainMenu(self, self.widgetStack)
        multiModeUI = genUIs.multiMode(self, self.widgetStack)
        markDoneUI = genUIs.markDone(self, self.widgetStack)
        resetPwdUI = genUIs.resetPwd(self, self.widgetStack)
        loginUI = genUIs.login(self, self.widgetStack)
        loggedInUI = genUIs.loggedIn(self, self.widgetStack)
        changePwdUI = genUIs.changePwd(self, self.widgetStack)
        changeCardUI = genUIs.changeCard(self, self.widgetStack)
        payModeUI = genUIs.payMode(self, self.widgetStack)
        newUserInitialUI = newUserUIs.newUserInitial(self, self.widgetStack)
        newUserCardUI = newUserUIs.newUserCard(self, self.widgetStack)
        newUserOldUsersUI = newUserUIs.newUserOldUsers(self, self.widgetStack)
        newUserBalanceUI = newUserUIs.newUserBalance(self, self.widgetStack)
        newUserFinalUI = newUserUIs.newUserFinal(self, self.widgetStack)

        # .. and then added to the widget stack
        self.widgetStack.addWidget(mainMenuUI)
        self.widgetStack.addWidget(multiModeUI)
        self.widgetStack.addWidget(markDoneUI)
        self.widgetStack.addWidget(resetPwdUI)
        self.widgetStack.addWidget(loginUI)
        self.widgetStack.addWidget(loggedInUI)
        self.widgetStack.addWidget(changePwdUI)
        self.widgetStack.addWidget(changeCardUI)
        self.widgetStack.addWidget(payModeUI)
        self.widgetStack.addWidget(newUserInitialUI)
        self.widgetStack.addWidget(newUserCardUI)
        self.widgetStack.addWidget(newUserOldUsersUI)
        self.widgetStack.addWidget(newUserBalanceUI)
        self.widgetStack.addWidget(newUserFinalUI)

        # The main UI is set as the current widget and everything is shown
        self.widgetStack.setCurrentWidget(mainMenuUI)
        self.lastWidgetId = mainMenuUI.id
        self.show()

    # A function that changes the active UI to whichever UI matches idUI
    def changeUI(self, idUI):

        if idUI == 'back':
            idUI = self.lastWidgetId
        self.lastWidgetId = self.widgetStack.currentWidget().id

        # Finding the UI matching idUI
        for indexUI in range(0,self.widgetStack.count()):
            testUI = self.widgetStack.widget(indexUI)
            if testUI.id == idUI:
                UI = testUI
                break

        # .. and then set to be the active UI
        self.widgetStack.setCurrentWidget(UI)
        
        # The UI is updated
        UI.update()        


    
        

# The usual main function, followed by the check that this file only can be run
# if it is not loaded as a module
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
