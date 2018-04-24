#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
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
    def __init__(self, name, mail, sduId, pwd, balance = 0, cardId = '', number = 0,
                 lastPay = 1, lastActive = 1, createDate = 1):

        # As the default input for unspecified last payment date is 1,
        # we now that if lastPay = 1, then we need to set both dates:
        if lastPay == 1:
            lastPay = date(2000, 1, 1)
            lastActive = date.today()

        if createDate == 1:
            createDate = date.today()

        # All parameters are transferred to be properties of the user
        self.name = name
        self.mail = mail
        self.sduId = sduId
        self.pwd = pwd
        self.balance = balance
        self.cardId = cardId
        self.lastPay = lastPay
        self.lastActive = lastActive
        self.createDate = createDate
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
    def paySome(self, amount, payDate=None):

        # The balance is subtracted the paid amount
        self.balance -= amount

        # The last pay property is updated
        if payDate is not None:
            self.lastPay = payDate
        else:
            self.lastPay = date.today()

    # Internal function that writes a file for the current object
    def saveUser(self):
        # If a user is newly created, the user number will be '0', which is corrected
        # to the appropriate number
        if self.number == 0:
            self.number = findNewUserNumber()

        # The path is then defined from the user number
        path = f'{dataFolder}Users/user_{self.number:04d}'

        if os.name != 'posix':
            cardId = self.cardId.replace('_', '?').replace(';', '<').replace(':', '>').replace('æ', ';')
        else:
            cardId = self.cardId

        # The user file is opened and all the information of the user is written to the file
        with open(path, 'w', encoding = 'utf-8') as userFile:
            userFile.write(self.name + '\n')
            userFile.write(self.mail + '\n')
            userFile.write(self.sduId + '\n')    
            userFile.write(self.pwd + '\n')
            userFile.write(str(self.balance) + '\n')
            userFile.write(cardId + '\n')
            userFile.write(str(self.lastPay) + '\n')
            userFile.write(str(self.lastActive) + '\n')
            userFile.write(str(self.createDate) + '\n')

# A function that loads a single user from 'path'
def loadUser(path):
    # The user file at 'path' is opened and the content is split in lines,
    # which are then sorted into their respective variables.
    with open(path, 'r', encoding = 'utf-8') as userFile:
        userContent = userFile.read().splitlines()
        name = userContent[0]
        mail = userContent[1]
        sduId = userContent[2]
        pwd = userContent[3]
        balance = int(userContent[4])
        cardId = userContent[5]
        number = int(path.split('_')[1])

        if os.name != 'posix':
            cardId = cardId.replace(';', 'æ').replace('<', ';').replace('>', ':').replace('?', '_')

        # As both lines containing dates need to be specifically formatted, they are
        # treated specially.
        lastPayLine = userContent[6].split('-')
        lastPay = date(*[int(x) for x in lastPayLine])
        
        lastActiveLine = userContent[7].split('-')
        lastActive = date(*[int(x) for x in lastActiveLine])

        try:
            createLine = userContent[7].split('-')
            createDate = date(*[int(x) for x in createLine])
        except IndexError:
            createDate = 1

        # At last everything is put into a user object and returned
        tmpUser = userInstance(name, mail, sduId, pwd, balance, cardId, number,
                               lastPay, lastActive, createDate)
    return tmpUser

# A function that loads all users and return a list
def loadUsers(users = None):

    # If users is not defined make it empty
    if users is None:
        users = []

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
    userFileList = os.listdir(f'{dataFolder}Users/')
    
    # Each time the loop runs it sets a True flag, which is turned False if any user file
    # already has the current user number.
    # If the flag is still True after the check, the current user number is not taken,
    # and otherwise, 1 is added, and the loop is restarted.
    while True:
        flag = True
        for userFile in userFileList:
            if 'user_' in userFile:
                userNumber = int(userFile.split('user_')[1])
                if userNumber == newUserNumber:
                    flag = False
                    break
        if flag:
            break
        newUserNumber += 1
    return newUserNumber

# A function that writes files for all the users contained in users
# (Will probably not be used)
def saveUsers(users):
    for user in users:
        user.saveUser()

# A function that takes a string and looks through all users in 'users'
# to see if any of their cardIds match the string.
# It then returns that user; returns None if no match is found.
def findUserCard(cardString, users = None):
    if users is None:
        users = loadUsers()
    for user in users:
        if cardString == user.cardId:
            return user
    return None

# A function very similar to the previous one, only it checks if the input string
# matches any sduId or mail of the users.
def findUserNoCard(inputString, users = None):
    if users is None:
        users = loadUsers()
    for user in users:
        if inputString == user.sduId:
            return user
        elif inputString == user.mail:
            return user
    return None

# A function to determine if a sduId is valid using regex'es
def validSduId(sduId):
    valid = re.match('[a-z]{5}[0-9]{2}',sduId)
    if valid is not None:
        if valid.group() == sduId:
            return True
    valid = re.match('[a-z]{4}[0-9]{3}',sduId)
    if valid is not None:
        if valid.group() == sduId:
            return True
    ## Approximately 150 student Ids in about 42000
    ## do not follow the above two conventions, but instead
    ## the one below.
    ## To prevent people from typing wrong, it will be left
    ## commented out for now.
    # valid = re.match('[a-z]{4}[0-9]{2}',sduId)
    # if valid is not None:
    #     if valid.group() == sduId:
    #         return True
    return False

def searchUsers(inString, users = None):
    inString = inString.lower()
    if users == None:
        users = loadUsers()
    matchUsers = []
    for user in users:
        if inString in user.name.lower() or inString in user.sduId.lower() or inString in user.mail.lower():
            matchUsers.append(user)
    return matchUsers

def totalDebt(debt=None, netDebt=None, users=None):

    if users == None:
        users = loadUsers()
    if debt is None:
        debt = {'400:2000':0, '350:400':0, '300:350':0, '250:300':0, '200:250':0, '150:200':0, '100:150':0, '50:100':0, '0:50':0,
                '-50:0':0, '-100:-50':0, '-150:-100':0, '-200:-150':0, '-250:-200':0, '-300:-250':0, '-350:-300':0, '-400:-350':0, '-2000:-400':0}
    
    for user in users:
        for interval in debt:
            itvl = [int(i) for i in interval]
            if itvl[0] < user.balance and user.balance <= itvl[1]:
                debt[interval] += user.balance

    if netDebt is None:
        netDebt = 0
    for interval in debt:
        netDebt += debt[interval]

    return debt, netDebt



def refToMainUser(refUser):
    mainUser = userInstance(refUser.name, refUser.mail, refUser.sduId, refUser.pwd, refUser.balance, refUser.cardId)
    return mainUser

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
