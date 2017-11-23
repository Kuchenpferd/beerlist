#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from datetime import date, datetime

# Path to determine the data folder (Should be changed to './Data/', when imported)
workFolder = './'

# Additional destinations
resourceFolder = workFolder + 'Resources/'
dataFolder = workFolder + 'Data/'

# The price of setting a mark
price = 5

# The class of the main user instance
class userInstance(object):

    # The user is set up with all of the properties
    def __init__(self, name, mail, sdu_id, pwd, balance = 0, cardId = 0, number = 0,
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
    with open(path, 'r') as userFile:
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
        lastPay = date(int(lastPayLine[0]), int(lastPayLine[1]), int(lastPayLine[2]))
        lastActiveLine = userContent[7].split('-')
        lastActive = date(int(lastActiveLine[0]),
                          int(lastActiveLine[1]), int(lastActiveLine[2]))

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
        for fileName in userFileList:
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
    with open(path, 'w') as userFile:
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

# A function to look through the file containing the names and mails of all students
# and return the name if the input string matches the mail of sduId of the student
def findName(idString):

    # First the path to the file is set and then opened and split into rows with a csv reader
    path = dataFolder + 'allStudents.csv'
    with open(path, 'r') as studentFile:
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

# The class of the reference user instance, now a subclass of the user instance.
# Reference users are the old users, that has not yet been created in the system
class refUserInstance(userInstance):

    # The reference user does not have nearly as many properties as the ordinary user,
    # so the rest of the necessaries are set to None.
    def __init__(self, name, mail, balance):
        super(refUserInstance, self).__init__(name, mail, None, None, balance)
        self.sduId = mail.split('@')[0]

# A function that loads all reference users and returns them in a list 'refUsers'
def loadRefUsers(refUsers = []):
    
    # First the path is determined
    path = dataFolder + 'refUsers.csv'

    # The '.csv' file is opened using a csv reader
    with open(path, 'r') as refUserFile:
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
    path = dataFolder + 'refUsers.csv'
    with open(path, 'w', newline = '') as refUserFile:
        rowWriter = csv.writer(refUserFile, dialect = 'excel')

        # Each user get their own row, and the relevant properties are written
        for refUser in refUsers:
            rowWriter.writerow([refUser.name, refUser.mail, str(refUser.balance)])

# The class that contains an hour-specific statistic
class statInstance(object):

    # The properties of the stat instance is initialized, with the capability of creating
    # a totally empty stat with no input arguments
    def __init__(self, units = 0, newUsers = 0, yearAndMonth = 1, dayOfMonth = 1, hour = 1):

        # Once again, we know that we need to determine the "standard" properties if
        # yearAndMonth = 1
        if yearAndMonth == 1:
            yearAndMonth = date.today().strftime('%y-%m')
            dayOfMonth = date.today().day
            hour = datetime.now().hour

        # All arguments are then turned into properties of the statistic
        self.units = int(units)
        self.newUsers = int(newUsers)
        self.yearAndMonth = yearAndMonth
        self.dayOfMonth = int(dayOfMonth)
        self.hour = int(hour)

    # Internal function, that adds 'units' to the relevant 'statType' property
    def addSome(self, statType, units = 1):
        if statType == 'Mark':
            self.units += units
        elif statType == 'User':
            self.newUsers += units

# A function that load the statistics file specific to the 'yearAndMonth' specified
# (stst files are named by yearAndMonth) and returns a list of stats
def loadStats(yearAndMonth, stats = []):

    # First the path is set to the specific file
    path = dataFolder + 'Statistics/' + yearAndMonth

    # As the specific stat file might not exist, a try/catch is set up with a FileNotFound catch
    try:
        # Assuming the file exists, it is opened and it's content split into lines
        with open(path, 'r') as statFile:
            content = statFile.read().splitlines()

            # As each line contains one instance of a stat, the content of each is
            # put into the relvant variables
            for line in content:
                lineContent = line.split(' ')
                units = lineContent[1]
                newUsers = lineContent[2]
                dayOfMonth = lineContent[0]
                hour = lineContent[3]

                # An instance of stat is then created and appended to the stats list
                tmpStat = statInstance(units, newUsers, yearAndMonth, dayOfMonth, hour)
                stats.append(tmpStats)

    except FileNotFoundError:
        # In case the file does not already exist, an empty instance of stat is created
        # and added as the single element of of 'sts'
        tmpStat = statInstance()
        stats.append(tmpStats)
        
    # At last the list is returned
    return stats

# A function that writes the elements of the list 'stats'
def saveStats(stats):

    # As all stats in a list can only have the same yearAndMonth
    # (per definition; see loadStats) it is fetched from the fist element
    # and the file path is set.
    yearAndMonth = stats[0].yearAndMonth
    path = dataFolder + 'Statistics/' + yearAndMonth

    # The stat file is opened and each stat is written  on its own line
    with open(path, 'w') as statFile:
        for stat in stats:
            line = '{} {} {} {}\n'.format(stat.dayOfMonth, stat.units, stat.newUsers, stat.hour)
            statFile.write(line)

# A function that updates the overall stats given the statType and units
def updateStats(statType, units):

    # First of the current yearAndMonth, dayOfMonth and hour is determined
    yearAndMonth = date.today().strftime('%y-%d')
    dayOfMonth = date.today().day
    hour = datetime.now().hour
    
    # Then the relevant stats list is created by loading the stats
    stats = loadStats(yearAndMonth)

    # A True flag is set up to determine if any stat matches both the current dayOfMonth and hour;
    # If there is a match, addSome is called for the specific stat, and the flag is set to False
    # and the llop is broken (as ony one stat can match)
    flag = True
    for stat in stats:
        if stat.dayOfMonth == dayOfMonth and stat.hour == hour:
            stat.addSome(statType, units)
            flag = False
            break

    # If the flag is still True after the loop is done, no stat matched
    # the current dayOfMonth and hour and thus a new instance should be created,
    # and have addSome run before being appended to the 'stats' list
    if flag:
        tmpStat = statInstance()
        tmpStat.addSome(statType, units)
        stats.append(tmpStat)

    # The new 'stats' list is then saved
    saveStats(stats)

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
