#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, pymongo, sys, os

def importPermCsv(mode='Students'):
    userList = []
    filePath = f'../Data/Permanent/all{mode}.csv'
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, dialect='excel')
        for row in reader:
            user = {'name':row[0], 'sduId':row[1].split('@')[0], 'mail':row[1]}
            userList.append(user)

    client = pymongo.MongoClient()
    db = client['beerlistData']
    collection = db[f'all{mode}']
    collection.insert_many(userList)


def importUsers():
    client = pymongo.MongoClient()
    db = client['beerlistData']
    collection = db[f'users']
    userList = loadUsers()
    collection.insert_many(userList)
    collection = db[f'refUsers']
    userList = loadRefUsers()
    collection.insert_many(userList)
    




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
        userDict = {'name':name, 'sduId':sduId, 'mail':mail, 'pwd':pwd, 'balance':balance, 'cardId':cardId, 'dates':{'lastActive':lastActive, 'lastPay':lastPay}}

    return userDict

def loadRefUsers(refUsers = None):
    
    # If the input list is None, set it to be empty
    if refUsers is None:
        refUsers = []

    # First the path is determined
    path = '../Data/Users/refUsers.csv'

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
                tmpRefUserDict = {'name':name, 'sduId':mail.split('@')[0], 'balance':balance}
                refUsers.append(tmpRefUser)

    # At last the list of refUsers is returned
    return refUsers

def loadUsers(users = None):

    # If users is not defined make it empty
    if users is None:
        users = []

    # First a list of files in the user folder is generated
    userFileList = os.listdir('../Data/Users/')

    # Then all files in the list are put into paths,
    # loaded and added to a list, that is then returned.
    # A check is set in place to make sure that only user files are loaded
    for userFile in userFileList:
        if 'user_' in userFile:
            path = '../Data/Users/' + userFile
            tmpUser = loadUser(path)
            users.append(tmpUser)
    return users

def main():
    pass

if __name__ == '__main__':
    main()