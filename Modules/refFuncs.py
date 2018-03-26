#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv

# Path to determine the data folder (Should be changed to './Data/', when imported)
workFolder = './../'

# Additional destinations
dataFolder = workFolder + 'Data/'

# The class of the reference user instance, now a subclass of the user instance.
# Reference users are the old users, that has not yet been created in the system
class refUserInstance(object):

    # The reference user does not have nearly as many properties as the ordinary user,
    # so the rest of the necessaries are set to None.
    def __init__(self, name = None, mail = None, balance = None, pwd = None, cardId = None):
        self.name = name
        self.mail = mail
        if mail is not None:
            self.sduId = mail.split('@')[0]
        else:
            self.sduIds = None
        self.balance = balance
        self.pwd = pwd
        self.cardId = cardId

    # Internal function to handle payments
    def paySome(self, amount):

        # The balance is subtracted the paid amount
        self.balance -= amount

# A function that loads all reference users and returns them in a list 'refUsers'
def loadRefUsers(refUsers = None):
    
    # If the input list is None, set it to be empty
    if refUsers is None:
        refUsers = []

    # First the path is determined
    path = dataFolder + 'Users/refUsers.csv'

    # The '.csv' file is opened using a csv reader
    with open(path, 'r', encoding = 'utf-8') as refUserFile:
        rowReader = csv.reader(refUserFile, dialect = 'excel')

        # As there is one reference user per row, each row is
        # separated into the relevant variables
        for row in rowReader:
            name = row[0]
            mail = row[1]
            balance = int(row[2])

            # As the only reference users that are relevant to check for
            # are the ones with a non-zero balance, we do the following check
            # before we create a refuserInstance and append that user to the list
            if balance != 0:
                tmpRefUser = refUserInstance(name, mail, balance)
                refUsers.append(tmpRefUser)

    # At last the list of refUsers is returned
    return refUsers

# A function that takes a list of reference users and writes it to the relevant file
def saveRefUsers(refUsers):
    path = dataFolder + 'User/refUsers.csv'
    with open(path, 'w', newline = '', encoding = 'utf-8') as refUserFile:
        rowWriter = csv.writer(refUserFile, dialect = 'excel')

        # Each user get their own row, and the relevant properties are written
        for refUser in refUsers:
            rowWriter.writerow([refUser.name, refUser.mail, str(refUser.balance)])

def findRefUser(inputString, refUsers = None):
    if refUsers == None:
        refUsers = loadRefUsers()
    for refUser in refUsers:
        if inputString == refUser.sduId:
            refUsers = refUsers.remove(refUser)
            return refUser, refUsers
    return None, refUsers

def searchRefUsers(inString, refUsers = None):
    inString = inString.lower()
    if refUsers == None:
        refUsers = loadRefUsers()
    matchIdxs = []
    for i, refUser in enumerate(refUsers):
        if inString in refUser.name.lower() or inString in refUser.mail.lower():
            matchIdxs.append(i)
    return matchIdxs, refUsers


# A function to look through the file containing the names and mails of all students
# and return the name if the input string matches the mail of sduId of the student
def findName(idString):

    # First the path to the file is set and then opened and split into rows with a csv reader
    path = dataFolder + 'Permanent/allStudents.csv'
    with open(path, 'r', encoding = 'utf-8') as studentFile:
        rowReader = csv.reader(studentFile, dialect = 'excel')

        # Each row is split into relevant variables
        # and then the sduId and mail are then checked
        # against the input string. The name is returned if
        # a match is found, and None is returned if no match is found
        for row in rowReader:
            name = row[0]
            mail = row[1]
            sduId = mail.split('@')[0]
            if idString == sduId:
                return name
            elif idString == mail:
                return name
    return None

# A function to look through the file containing the names and mails of all employees
# and return the name if the input string matches the mail of sduId of the employee
def findEmpolyee(idString):

    # First the path to the file is set and then opened and split into rows with a csv reader
    path = dataFolder + 'Permanent/allStaff.csv'
    with open(path, 'r', encoding = 'utf-8') as employFile:
        rowReader = csv.reader(employFile, dialect = 'excel')

        # Each row is split into relevant variables
        # and then the sduId and mail are then checked
        # against the input string. The name is returned if
        # a match is found, and None is returned if no match is found
        for row in rowReader:
            name = row[0]
            mail = row[1]
            sduId = mail.split('@')[0]
            if idString == sduId:
                return name, mail
            elif idString == mail:
                return name, mail
    return None, None

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
