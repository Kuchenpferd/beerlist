#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
from statFuncs import updateStats
from datetime import date

# Path to determine the data folder (Should be changed to './Data/', when imported)
workFolder = './../'

# Additional destinations
dataFolder = workFolder + 'Data/'

# The price of setting a mark
price = 5

# The class of the main user instance
class userInstance(object):

    # The user is set up with all of the properties
    def __init__(self, name, mail, sduId, pwd, balance = 0, cardId = 0, number = 0,
                 lastPay = 1, lastActive = 1):

        # As the default input for unspecified last payment date is 1,
        # we now that if lastPay = 1, then we need to set both dates:
        if lastPay == 1:
            lastPay = date(2000, 1, 1)
            lastActive = date.today()

        # All parameters are transferred to be properties of the user
        self.name = name
        self.mail = mail
        self.sduId = sduId
        self.pwd = pwd
        self.balance = balance
        self.cardId = cardId
        self.lastPay = lastPay
        self.lastActive = lastActive
        self.number = number

    # Internal function to add 'units' marks to the the user balance
    def addSome(self, units = 1):
        self.balance += price*units

        # The last active property is also updated
        self.lastActive = date.today()

        # The stats are updated with the type 'Mark' (see class and functions further down)
        statType = 'Mark'
        updateStats(statType, units)

    # Internal function to handle payments
    def paySome(self, amount):

        # The balance is subtracted the paid amount
        self.balance -= amount

        # The last pay property is updated
        self.lastPay = date.today()

# A function that loads a single user from 'path'
def loadUser(path):
    # The user file at 'path' is opened and the content is split in lines,
    # which are then sorted into their respective variables.
    with open(path, 'r', encoding = 'utf-8') as userFile:
        userContent = userFile.read().splitline()
        name = userContent[0]
        mail = userContent[1]
        sduId = userContent[2]
        pwd = userContent[3]
        balance = int(userContent[4])
        cardId = userContent[5]
        number = int(path.split('_')[1])

        # As both lines containing dates need to be specifically formatted, they are
        # treated specially.
        lastPayLine = userContent[6].split('-')
        lastPay = date(int(lastPayLine[0]),
                       int(lastPayLine[1]),
                       int(lastPayLine[2]))
        
        lastActiveLine = userContent[7].split('-')
        lastActive = date(int(lastActiveLine[0]),
                          int(lastActiveLine[1]),
                          int(lastActiveLine[2]))

        # At last everything is put into a user object and returned
        tmpUser = userInstance(name, mail, sdu_id, pwd, balance, cardId, number,
                               lastPay, lastActive)
    return tmpUser

# A function that loads all users and return a list
def loadUsers(users = []):

    # First a list of files in the user folder is generated
    userFileList = os.listdir(dataFolder + 'Users/')

    # Then all files in the list are put into paths,
    # loaded and added to a list, that is then returned.
    # A check is set in place to make sure that only user files are loaded
    for userFile in userFileList:
        if 'user_' in userFile:
            path = dataFolder + 'Users/' + userFile
            tmpUser = loadUser(path)
            users.append(tmpUser)
    return users

# A small function to determine the next number of user
# (Has been rewritten, so that it can fill out an eventual "hole" of a deleted user)
# (Has been further rewritten to check the directory instead of a list)
def findNewUserNumber():

    # An initial value is set (1 is the only reasonable value for this)
    newUserNumber = 1

    # A list of filenames in the user directory is loaded
    userFileList = os.listdir(dataFolder + 'Users/')
    
    # Each time the loop runs it sets a True flag, which is turned False if any user file
    # already has the current user number.
    # If the flag is still True after the check, the current user number is not taken,
    # and otherwise, 1 is added, and the loop is restarted.
    while True:
        flag = True
        for userFile in userFileList:
            userNumber = int(userFile.split('user_')[1])
            if userNumber == newUserNumber:
                flag = False
                break
        if flag:
            break
        newUserNumber += 1
    return newUserNumber

# A function that writes a file for the specified 'user'
def saveUser(user):

    # If a user is newly created, the user number will be '0', which is corrected
    # to the appropriate number
    if user.number == 0:
        user.number = findNewUserNumber()

    # The path is then defined from the user number
    path = dataFolder + 'Users/user_{number:04d}'.format(number = user.number)

    # The user file is opened and all the information of the user is written to the file
    with open(path, 'w', encoding = 'utf-8') as userFile:
        userFile.write(user.name + '\n')
        userFile.write(user.mail + '\n')
        userFile.write(user.sduId + '\n')    
        userFile.write(user.pwd + '\n')
        userFile.write(str(user.balance) + '\n')
        userFile.write(user.cardId + '\n')
        userFile.write(str(user.lastPay) + '\n')
        userFile.write(str(user.lastActive) + '\n')

# A function that writes files for all the users contained in users
# (Will probably not be used)
def saveUsers(users):
    for user in users:
        saveUser(user)

# A function that takes a string and looks through all users in 'users'
# to see if any of their cardIds match the string.
# It then returns that user; returns None if no match is found.
def findUserCard(cardString, users):
    for user in users:
        if cardString == user.cardId:
            return user
    return None

# A function very similar to the previous one, only it cheks if the input string
# matches any sduId or mail of the users.
def findUserNoCard(inputString, users):
    for user in users:
        if inputString == user.sduId:
            return user
        elif inputString == user.mail:
            return user
    return None

def refToMainUser(refUser):
    mainUser = userInstance(refUser.name, refUser.mail, refUser.sduId, refUser.pwd, refUser.balance)
    return mainUser

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
