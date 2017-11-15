import sys
import pyautogui
from PyQt4 import QtGui, QtCore
        
class myWin(QtGui.QMainWindow):
     def __init__(self,parent=None):
          super(myWin, self).__init__(parent)
          self.setGeometry(50,50,500,300)
          self.mainUI()

     def mainUI(self):
          # Setting up a simple LineEdit forto test functionality
          line_ed = QtGui.QLineEdit(self)
          line_ed.move(0,80)
          line_ed.resize(100,15)
          line_ed.setFocus(True)

          # Setting up a checkable modifier button, in this case shift.
          # Note that all buttons should have the focus set to none,
          # to keep the cursor in the LineEdit
          shift_btn = QtGui.QPushButton('Shift', self)
          shift_btn.move(0,140)
          shift_btn.setFocusPolicy(QtCore.Qt.NoFocus)
          shift_btn.setCheckable(True)

          # Setting up the generic letter button. on click, it sends its
          # label and the modifier key to the virtual key press function
          a_btn = QtGui.QPushButton('a', self)
          a_btn.move(0,100)
          a_btn.setFocusPolicy(QtCore.Qt.NoFocus)
          a_btn.clicked.connect(lambda: self.virtKeyPress('a', shift_btn))


     # Naïve virtual key press function.
     # It takes in whatever the button press label was, along with the
     # modfier key (shift in this case), modifies the key if necessary
     # and then calls typewrite(str) from PyAutoGui, which emulates the key press
     def virtKeyPress(self, key, shift_btn):
          if shift_btn.isChecked():
               key = key.upper()
          pyautogui.typewrite(key)

if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     mainW = myWin()
     mainW.show()
     sys.exit(app.exec_())
