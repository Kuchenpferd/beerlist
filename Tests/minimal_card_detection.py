import sys
from PyQt4 import QtGui
          
class myWin(QtGui.QMainWindow):
     def __init__(self):
          super(myWin, self).__init__()
          self.setGeometry(50,50,500,300)
          
          # The Widget must have an empty string to keep track of pressed keys
          self.card_seq = ''

     # Modifies the keyPressedEvent to specifically listen for SDU cards
     def keyPressEvent(self, event):
         if type(event) == QtGui.QKeyEvent:
              # Check if the pressed keycode matches the card initializer 'æ'
              if event.key() == 198:
                   # Clears the stored sequence, i.e. initialization
                   self.card_seq = ''
              # Check if the pressed keycode matches the card terminator (Either 'Enter' key, should be cleaned later)
              elif event.key() == 16777221 or event.key() == 16777220:
                   # Placeholder for the event, where we can pass the card sequence, i.e. termination
                   print(str(self.card_seq))
              # Always add the latest keypress at the end of the card sequence
              self.card_seq += event.text()
              
              event.accept()
         else:
              event.ignore()


if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     mainW = myWin()
     mainW.show()
     sys.exit(app.exec_())
