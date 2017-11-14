import sys
from PyQt4 import QtGui, QtCore
          
class myWin(QtGui.QMainWindow):
     def __init__(self):
          super(myWin, self).__init__()
          self.setGeometry(50,50,500,300)
          self.mainUI()
          

     def mainUI(self):

          self.line_ed = QtGui.QLineEdit(self)
          self.line_ed.move(0,80)
          self.line_ed.resize(100,15)
          self.line_ed.setFocusPolicy(QtCore.Qt.StrongFocus)

          
          a_btn = QtGui.QPushButton('a', self)
          a_btn.move(0,100)
          a_btn.setFocusPolicy(QtCore.Qt.NoFocus)
          #a_btn.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_A, QtCore.Qt.NoModifier))
          a_btn.clicked.connect(self.do)
          #a_btn.clicked.connect(lambda: self.simKeyPress(1QtCore.Qt.Key_A))
          
     #def simKeyPress(self, key = 0):
          #self.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier))

     def do(self):
          self.line_ed.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_A, QtCore.Qt.NoModifier))




if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     mainW = myWin()
     mainW.show()
     sys.exit(app.exec_())
