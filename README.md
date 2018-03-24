# beerlist_gui
A GUI for the previous beerlist system using Python 3.6

UIs to do:
 - New User (sduId, name, mail, pwd) - Needs testing!
 - New User (Old Users) - Needs testing!
 - New User (balance) - Needs testing!
 - New User (new card) - Needs testing!
 - New User (Final) - Needs testing!
 
Other things to do:
 - Started testing of the newUser UIs:
 	- Having an issue, where an old user doesn't show up again if the user
 	  creation is cancelled.
 	- Implemented a check of allStaff.csv, along the lines of allStudents.csv,
 	  but it needs to be tested thoroughly
 	- Still missing a few possibilities.
 - Consider a redo of the 'Back' system, it doesn't seem to be working as intended
 	- Did a first pass of this, needs to be checked

Dependencies (Everything can now be installed using PIP3): 
 - PyQt5, pyautogui, pyperclip, pyqrcode, pypng, exchangelib
 - All further dependencies should already be in a standard Python build
 - Note that the special dependencies and requirements of the standalone script updateStudentList.py is listed within this specific file.
