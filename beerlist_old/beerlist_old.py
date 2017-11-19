# coding=utf8

import hashlib
import os
import csv
import time
import datetime
import getpass

ppc = 5 # Price Per Can (kroner)
users = [] # List over all users

v = False

err_contact = 'Please try again or contact Dennis (dsb@sdu.dk) or Mikkel Schier (mikkc13)'

####################################################################################
## Definition of the class and relevant functions for reference (old paper) users ##
####################################################################################
class ref_user(object):

    def __init__(self, name, mail, balance=0):
        self.name = name
        self.mail = mail
        self.balance = balance

def addRefUsers():
    ref_users = []
    with open('paper_users.csv','r',encoding='utf8') as csvfile:
        dreader = csv.reader(csvfile,dialect='excel')
        for row in dreader:
            if int(row[2]) != 0:
                tmp_user=ref_user(row[0],row[1],int(row[2]))
                ref_users.append(tmp_user)
    return ref_users

def writeRefUsers(ref_users):
    with open('paper_users.csv','w',newline='',encoding='utf8') as csvfile:
        rwriter = csv.writer(csvfile,dialect='excel')
        for r_user in ref_users:
            rwriter.writerow([r_user.name, r_user. mail, str(r_user.balance)])

###########################################
## Definition of class statistics (stat) ##
###########################################
class stat(object):

    def __init__(self, units=0, new_users=0, yam_id=1, dom_id=1, h = 1):
        if yam_id == 1:
            yam_id=datetime.date.today().strftime("%y-%m")
        if dom_id == 1:
            dom_id=int(datetime.date.today().day)
        if h == 1:
            h = int(datetime.datetime.now().hour)
        self.yam_id = yam_id
        self.dom_id = dom_id
        self.h = h
        self.units = units
        self.new_users = new_users

    def addSome(self, cat='un', numUnits=1):
        if cat == 'un':
            self.units += numUnits
        elif cat == 'us':
            self.new_users += 1


# Define function to read the stat file
def openStats(yam):
    stats = []
    path = 'statistics/' + yam
    try:
        stat_file = open(path, "r")
        content = stat_file.read().splitlines()
        for line in content:
            data = line.split(' ')
            dom = int(data[0])
            no_units = int(data[1])
            new_users = int(data[2])
            hour = int(data[3])
            tmp_stat = stat(no_units,new_users,yam,dom,hour)
            stats.append(tmp_stat)
        stat_file.close()
    except FileNotFoundError:
        tmp_stat = stat()
        stats.append(tmp_stat)
    return stats

# Define function to write the stat file
def writeStats(yam,stats):
    path = 'statistics/' + yam
    stat_file = open(path, "w")
    for stat_in in stats:
        if stat_in.yam_id == yam:
            stat_file.write(str(stat_in.dom_id) + ' ' + str(stat_in.units) + ' ' + str(stat_in.new_users) + ' ' + str(stat_in.h) + '\n')
    stat_file.close()

# Define a function that can easily be called from within the main script (This handles ALL interaction of users and statistics)
def alterStats(cat='un',units=1):
    yam = datetime.date.today().strftime("%y-%m")
    dom = int(datetime.date.today().day)
    hour = int(datetime.datetime.now().hour)
    count = 0
    stats = openStats(yam)
    for stat_in in stats:
        if stat_in.dom_id == dom:
            if stat_in.h == hour:
                stat_in.addSome(cat,units)
                count += 1
    if count == 0:
        if cat == 'un':
            tmp_stat = stat(units)
        elif cat == 'us':
            tmp_stat = stat(0,units)
        stats.append(tmp_stat)
    writeStats(yam,stats)



################################
## Definition of class 'user' ##
################################
class user(object):

    def __init__(self, name, mail, sdu_id, pwd, balance=0, card_id=0, number=0, last_pay=datetime.date(2000,1,1), last_card=1):
        if last_card == 1:
            last_card = datetime.date.today()
        self.name = name
        self.mail = mail
        self.sdu_id = sdu_id
        self.balance = balance
        self.card_id = card_id
        self.pwd = pwd
        self.last_pay = last_pay
        self.last_card = last_card
        self.number = number

    def __str__(self):
        return '\nUser: ' + self.name + '\nUser number: {}'.format(self.number)      

    def printStuff(self):
        print('\nName: ' + self.name)
        print('SDU ID: {}'.format(self.sdu_id))
        print('Mail: {}'.format(self.mail))
        print('Balance: {} kr.'.format(self.balance))
        if self.card_id:
            print('Card ID: {}'.format(self.card_id))
        else:
            print('Card ID has not yet been defined.')
        print('Password: {}'.format(self.pwd))
        print('Last active with payments: {}'.format(self.last_pay))
        print('Last active with a card swipe: {}'.format(self.last_card))
        print('User number: {}'.format(self.number))

    def printBalance(self):
        os.system('clear')
        print('Hi {}, your current balance is: {}'.format(self.name,self.balance))

    # Now takes the input numCans, and adds that number of ppc to the balance.    
    def addSome(self, numCans):
        self.balance += ppc*numCans
        self.last_card = datetime.date.today()
        alterStats('un',numCans)

# Define function to find the next user number
def nextUserNumber():
    next_user = 1
    for user in users:
        if user.number >= next_user:
            next_user = user.number+1
    return next_user

# Define function to read a file and create a user with the info in the file
def addUserFromFile(path):
    if v:
        print('------------------------------------')
        print('addUserFromFile() has been called...')
        print('------------------------------------')

    if v: print('Opening user file: ' + path)
    user_file = open(path, "r")
    content = user_file.read().splitlines()
    if v:
        print('This file contains:')
        for line in content:
            print(line)
    # Adds the capability of reading the two dates, that are now stored in the user file as well.
    lp = content[6].split('-')
    lp = datetime.date(int(lp[0]),int(lp[1]),int(lp[2]))
    lc = content[7].split('-')
    lc = datetime.date(int(lc[0]),int(lc[1]),int(lc[2]))
    tmp_number = int(path.split('_')[1])
    if v: print('\nAdding user:')
    tmp_user = user(content[0], content[1], content[2], content[3], int(content[4]), content[5], tmp_number, lp, lc)
    if v: tmp_user.printStuff()
    users.append(tmp_user)
    user_file.close()

# Define function to write a user_file saving the relevant information
def writeUserFile(user):
    if v: print('----------------------------------')
    if v: print('writeUserFile() has been called...')
    if v: print('----------------------------------')
    if user.number == 0: user.number = nextUserNumber()
    name = 'users/user_' + '{num:04d}'.format(num=user.number)
    if v: print('Writing to file ' + name)
    user_file = open(name, 'w')
    user_file.write(user.name + '\n')
    user_file.write(user.mail + '\n')
    user_file.write(user.sdu_id + '\n')    
    user_file.write(user.pwd + '\n')
    user_file.write(str(user.balance) + '\n')
    user_file.write(user.card_id + '\n')
    user_file.write(str(user.last_pay) + '\n')
    user_file.write(str(user.last_card) + '\n')
    user_file.close()

# Define function which returns an integer from input
def inputInt(string):
    while True:
        while True:
            try: 
                integer1 = int(input(string))
            except (ValueError, KeyboardInterrupt, EOFError):
                print('Error - input is not an integer, try again.')
            else:
                break
        while True:
            try:
                integer2 = int(input('Confirm (write it again)\n'))
            except (ValueError, KeyboardInterrupt, EOFError):
                print('Error - input is not an integer, try again.')
            else:
                break
        if integer1 == integer2:
            return integer1
        else:
            print('The two numbers do not match - try again')
            continue

# Define function which returns a string upon requesting it twice and checking it
def inputCard(string, check=True):
    while True:
        try:
            string1 = input(string)
            if string1 == 'æ_':
                print('Sorry, but there was an error reading your card, please try again:')
                continue
            elif check:
                string2 = input('Confirm (do it again)\n')
                if string2 == 'æ_':
                    print('Sorry, but there was an error reading your card, please try again from the beginning:')
                    continue
                elif string1 == string2:
                    return string1
                else:
                    print('Confirmation failed, try again from the beginning:')
                    continue
            else:
                return string1
        except (KeyboardInterrupt, EOFError):
            pass
            
# Define function which returns a string upon checking that it is correct
# and non-empty
def inputString(string, check=True, check2=False):
    while True:
        try:
            string1 = input(string)
            if check:
                if check2:
                    try:
                        if string1 != 'exit':
                            string1.split(' ')[1]
                    except IndexError:
                        print('Your full name should contain at least two names!\nPlease try again.')
                        continue
                    key=input('Is this correct? (y/n)\n' + string1.title() + '\n')
                else:
                    key=input('Is this correct? (y/n)\n' + string1 + '\n')
                if key == 'y':
                    return string1
                else:
                    print('Please try again from the beginning:')
                    continue
            else:
                return string1
        except (KeyboardInterrupt, EOFError):
            pass

#Define a function that returns a masked (hashed) password after asuring that it is correct
def inputPass(string, check=True):
    while True:
        try:
            string1 = getpass.getpass(string)
            if check:
                string2 = getpass.getpass('Confirm (write it again)\n')
                if string1 == string2:
                    return string1
                else:
                    print('Confirmation failed, try again from the beginning:')
                    continue
            else:
                return string1
        except (KeyboardInterrupt, EOFError):
            pass
        
# Define function which adds a user by asking user for input
def addUserByInput(new_card_id=''):
    while True:
        ok = False
        did_refs = False
        while True:
            tmp_sdu_id = inputString('Please enter your SDU ID (Part before @ in your student mail)\n(If you are an employee, please input "employee"):\n')
            tmp_sdu_id = tmp_sdu_id.lower()
            with open('all_users.csv','r',encoding='utf8') as ref_file:
                for line in ref_file:
                    ref = line.strip('\n').split(',')
                    if tmp_sdu_id == ref[1].split('@')[0]:
                        found = input('Is your name ' + ref[0] + '? (y/n):\n')
                        if found in 'exitExit':
                            print('Returning to the main screen.')
                            time.sleep(3)
                            return
                        elif found == 'n':
                            tmp_name = ''
                            tmp_mail = ''
                            print('Please continue manually then.')
                            break
                        elif found == 'y':
                            tmp_name = ref[0]
                            tmp_mail = ref[1]
                            ref_users = addRefUsers()
                            did_refs = True
                            for r_user in ref_users:
                                if tmp_sdu_id == r_user.mail.split('@')[0] or tmp_name == r_user.name:
                                    print('You were already a user with a balance of: ' + str(r_user.balance) + ' kr.')
                                    tmp_balance = r_user.balance
                                    tmp_marks = 0
                                    ref_users.remove(r_user)
                                    break
                            tmp_balance = 0
                            tmp_marks = 0
                            break
                    else:
                        tmp_name = ''
                        tmp_mail = ''
            if tmp_sdu_id in 'exitExit':
                print('Returning to the main screen.')
                time.sleep(3)
                return
            elif tmp_sdu_id == 'employee':
                print('You have chosen employee mode.\n')
                while True:
                    tmp_sdu_id = inputString('Please enter your prefered SDU ID (Choose for yourself):\n')
                    if tmp_sdu_id == 'exit' or tmp_sdu_id == 'Exit':
                        print('Returning to the main screen.')
                        time.sleep(3)
                        return
                    for user1 in users:
                        if user1.sdu_id == tmp_sdu_id:
                            print('The SDU ID you have entered is already in use! ' + err_contact)
                            break
                    else: break
                while True:
                    tmp_mail = inputString('SDU-mail (Use dash "-" instead of period "."):\n')
                    tmp_mail = tmp_mail.replace('-','.')
                    if tmp_mail == 'exit' or tmp_mail == 'Exit':
                        print('Returning to the main screen.')
                        time.sleep(3)
                        return
                    elif '@' not in tmp_mail:
                        print('That is not a valid mail-address (no @), try again')
                    elif 'sdu.dk' not in tmp_mail.split('@')[1]:
                        print('That is not a valid SDU mail, try again.')
                    else:
                        for user1 in users:
                            if user1.mail == tmp_mail:
                                print('The mail you have entered is already in use! ' + err_contact)
                                break
                        else:
                            ref_users = addRefUsers()
                            for r_user in ref_users:
                                if tmp_mail == r_user.mail:
                                    fprint('You were already a user with a balance of: ' + str(r_user.balance))
                                    tmp_balance = r_user.balance
                                    tmp_marks = 0
                                    ref_users.remove(r_user)
                                    did_refs = True
                                    break
                            break
                tmp_name = ''
                break
            elif len(tmp_sdu_id) != 7:
                print('There is an incorrect number of characters! ' + err_contact)
                continue
            else:
                for user1 in users:
                    if user1.sdu_id == tmp_sdu_id:
                        print('The SDU ID you have entered is already in use! ' + err_contact)
                        break
                if not tmp_mail:
                    tmp_mail = tmp_sdu_id + '@student.sdu.dk'
                break
        if not tmp_name:
            tmp_name = inputString('Full name:\n',True,True)
            tmp_name = tmp_name.title()
            if tmp_name in 'exitExit':
                print('Returning to the main screen.')
                time.sleep(3)
                return
        print('Please enter a password below. The only time you need the password is if you have \nforgotten your card, but you still want to have a soda/beer/noodle,\nor if you have to change to a new card\n')
        print('This system is encrypted with SHA256!')
        tmp_pwd_input = inputPass('Please enter a password (Note that no characters will show):\n')
        tmp_pwd = hashlib.sha256(tmp_pwd_input.encode()).hexdigest()
        while True:
            if did_refs:
                break
            new = input('Are you already a member of the paper list: (y)es or (n)o?\n')
            if new in 'exitExit':
                print('Returning to the main screen.')
                time.sleep(3)
                return
            elif new == 'n':
                tmp_marks = 0
                tmp_balance = 0
                break
            elif new == 'y':
                tmp_marks = 0 #inputInt('Current number of marks:\n') No use for this, as noone has any marks right now!
                input('Please take note of your debt in the following list: (Press Enter to continue)')
                ref_users = addRefUsers()
                c = 0
                tab_form = '{0:%d}{1:%d}{2}' % (33, 30)
                os.system('clear')
                print(tab_form.format('Name:', 'Mail:', 'Balance:'))
                for ref_user in ref_users:
                    print(tab_form.format(ref_user.name, ref_user.mail, str(ref_user.balance)))
                    c += 1
                    if c == 16:
                        c = 0
                        input('Press Enter to get the next list.')
                        os.system('clear')
                        print(tab_form.format('Name:', 'Mail:', 'Balance:'))
                tmp_balance = inputInt('\nCurrent balance. If your balance is negative\n(remember, that\'s a good thing!) use the minus sign to the left of "@":\n')
                break
            else:
                print('Not a valid answer, try again.')
        tmp_balance += ppc*tmp_marks
        # The check that asks if newuser was started by a card swipe
        if new_card_id != '':
            while True:
                if new_card_id[0] != 'æ':
                    new_card_id = new_card_id[1:]
                else:
                    break
            tmp_card_id = new_card_id
        else:
            tmp_card_id = inputCard('Swipe your SDU-card\n')
            if tmp_card_id == 'exit' or tmp_card_id == 'Exit':
                print('Returning to the main screen.')
                time.sleep(3)
                return
        os.system('clear')
        print('\n--- You have entered the following: ---\n')
        print('Name: ' + tmp_name)
        print('SDU ID: ' + tmp_sdu_id)
        print('Mail: ' + tmp_mail)
        #print('Entered number of marks: {}'.format(tmp_marks))
        print('Current balance: {} kr.'.format(tmp_balance))
        while True:
            answer = input('Are the above correct? (y)es, (n)o or (e)xit\n')
            if answer in 'yne':
                break
            else:
                print('Not an option')
        if answer == 'y':
            print('Great the user has now been created!\nPlease note that no additional marks has been added during the registration!\n Returning to the main screen.')
            time.sleep(3)
            break
        elif answer == 'e':
            print('Exiting - no user was added')
            return
        else:
            print('Then lets do it again')
            continue

    tmp_user = user(tmp_name, tmp_mail, tmp_sdu_id, tmp_pwd, tmp_balance, tmp_card_id)
    if v: tmp_user.printStuff()
    users.append(tmp_user)
    alterStats('us')
    writeUserFile(tmp_user)
    if did_refs:
        writeRefUsers(ref_users)
        
# Define function which returns the user fitting the card_id
def findUser(string):
    for user in users:
        if string == user.card_id:
            if v: user.printStuff()
            return user
    return 0

# Define function which returns the user fitting the input sdu_id or mail
def findUserNoCard(string):
    for user in users:
        if string == user.sdu_id:
            if v: user.printStuff()
            return user
        elif string == user.mail:
            if v: user.printStuff()
            return user
    return 0

# Define function which adds ppc to the balance of a user and re-writes to the user file
# Now takes additional input of numCans, and passes it to addSome
def addAndReWrite(user, numCans=1):
    print('Adding kr. {} to the balance of {}'.format(ppc*numCans, user.name))
    user.addSome(numCans)
    writeUserFile(user)
    print('{} now has a balance of {} kr.'.format(user.name, user.balance))

# Define function which changes the card-id of a user and rewrites that user
def changeCard(user):
    if v: print('Current card-id of {} is {}'.format(user.name, user.card_id))
    tmp_card_id = inputCard('Swipe your new card\n')
    user.card_id = tmp_card_id
    print('Your card was succesfully changed!')
    if v: print('The card id is now {}'.format(user.card_id))
    writeUserFile(user)

# Define the function which should run at all times
# Should take inputs for the following:
# add a soda/beer to the balance
# add a new user, in two different ways;
# by direct input of a command or by input of an unknown card
# change a user's card
# check a users balance
# register multiplum input "xYY" where YY are integers
# have some form of SUDO
def runForEver():
    newKey = 'newuser'
    cardKey = 'newcard'
    balKey = 'bal'
    sudoKey = 'sudennis'
    os.system('clear')
    print('\n-----------------------------------')
    print('- Welcome to Øllistesystemet v1.9 -')
    print('-----------------------------------\n')
    print('For any questions contact Dennis (dsb@sdu.dk) or Mikkel Schier (mikkc13)\n')
    print('When you grab a soda/beer/noodles: run your SDU card through the reader.\nIf you want to register multiple marks at once, you can write "x" followed \nby a number and then swipe your card. For example: "x5" would register 5 marks.\nIf you wish to add yourself as a new user, simply swipe your card \nor write "' + newKey + '" and press Enter.\nIf you wish to change your card, write "' + cardKey + '" and press Enter.\nTo check your balance please write "' + balKey + '" and press Enter.\n')
    tmpKey = inputString('Swipe or write "' + newKey + '", "' + cardKey + '", "' + balKey + '" or "x.."\n\n', False)

    os.system('clear')

    # Check if a new user should be added
    if tmpKey == newKey:
        tmpAnswer = input('Do you wish to add a new user:\n(y)es or (n)o?\n')
        if tmpAnswer == 'y':
            print('You have requested to add a new user, fill in below:')
            addUserByInput()
        else:
            print('Okay - going back\n')
            time.sleep(1)
        return 1
    # Check if a card-id should be changed
    elif tmpKey == cardKey:
        tmpAnswer = input('Do you wish to change your card:\(y)es or (n)o?\n')
        if tmpAnswer == 'y':
            os.system('clear')
            print('You have requested to change your card')
            tmpId = inputString('Enter your SDU ID or email\n')
            if tmpId == 'exit' or tmpId == 'Exit':
                print('Returning to the main screen.')
                time.sleep(3)
                return 1
            tmpUser = findUserNoCard(tmpId)
            if tmpUser:
                print('You have entered the SDU ID or email belonging to {}'.format(tmpUser.name))
                tmpAnswerInput = inputPass('Please enter your password (Note that no characters will show):\n', False)
                tmpAnswer = hashlib.sha256(tmpAnswerInput.encode()).hexdigest()
                if tmpAnswer == tmpUser.pwd:
                    print('Correct!')
                    changeCard(tmpUser)
                    time.sleep(3)
                    return 1
                else:
                    print('Sorry, the password you entered was incorrect! ' + err_contact)
                    time.sleep(3)
                    return 1
            else:
                print('User not found! ' + err_contact)
                time.sleep(3)
                return 1
    # Check if sudo-mode activated
    elif tmpKey == sudoKey:
        print('You have entered GOD MODE, exiting...')
        time.sleep(1)
        return 0
    # Check if balance mode is selected, and performs the appropriate actions
    elif tmpKey == balKey:
        tmpAnswer = input('You have chosen balance mode, please swipe your card \nor enter you SDU/ID mail to check your balance:\n')
        if tmpAnswer == 'exit' or tmpAnswer == 'Exit':
                print('Returning to the main screen.')
                time.sleep(3)
                return 1
        tmpUser = findUser(tmpAnswer)
        if tmpUser:
            tmpUser.printBalance()
            time.sleep(5)
            return 1
        else:
            tmpUser = findUserNoCard(tmpAnswer)
            if tmpUser:
                tmpUser.printBalance()
                time.sleep(5)
                return 1
            else:
                print('User not found! ' + err_contact)
                time.sleep(3)
                return 1
    # A standard check to see if the key is one of the saved cards.
    else:
        tmpUser = findUser(tmpKey)
        if tmpUser:
            addAndReWrite(tmpUser)
            time.sleep(3)
        # Check if the entered key contains 'æ;:' (Maybe this should be 'Ã¦;:' instead), which would mean that an unknown card has been swiped. Appropriate action is taken
        elif 'æ;:' in tmpKey:
            tmpAnswer = input('You have swiped an unknown card.\nIf you are already a user, please write (n)o below.\nDo you wish to create a new user for that card: \n(y)es or (n)o\n')
            if tmpAnswer == 'y':
                print('You have requested to add a new user, fill in below:')
                addUserByInput(tmpKey)
            else:
                print('Okay - going back\n')
                time.sleep(3)
        # An extra check to see if the key is the sdu_id or mail of a user. If it is, it prompts for a password, checks that and adds to the balance of that user
        else:
            tmpUser = findUserNoCard(tmpKey)
            if tmpUser:
                print('You have entered the SDU ID or email belonging to {}'.format(tmpUser.name))
                tmpAnswerInput = inputPass('Please enter your password (Note that no characters will show):\n', False)
                tmpAnswer = hashlib.sha256(tmpAnswerInput.encode()).hexdigest()
                if tmpAnswer == tmpUser.pwd:
                    print('Correct!')
                    addAndReWrite(tmpUser)
                    time.sleep(3)
                else:
                    print('Sorry, the password you entered was incorrect! ' + err_contact)
                    time.sleep(3)
            else:
                # A whole series of checks, to see if the syntax match that of the multiple mode. If it does it sets numCans and checks for both card and login information.
                if len(tmpKey) == 2 or len(tmpKey) == 3:
                    if tmpKey[0] == 'x' and tmpKey[1:].isdigit():
                        numCans = int(tmpKey[1:])
                        if numCans <= 24:
                            tmpKey2 = inputString('You have chosen multiple mode, to register {} marks, please swipe your card \nor enter your SDU ID, to return to main press "Enter"\n'.format(numCans), False)
                            tmpUser = findUser(tmpKey2)
                            if tmpUser:
                                addAndReWrite(tmpUser, numCans)
                                time.sleep(3)
                                return 1
                            else:
                                tmpUser = findUserNoCard(tmpKey2)
                            if tmpUser:
                                print('You have entered the SDU ID or email belonging to {}'.format(tmpUser.name))
                                tmpAnswerInput = inputPass('Please enter your password (Note that no characters will show):\n', False)
                                tmpAnswer = hashlib.sha256(tmpAnswerInput.encode()).hexdigest()
                                if tmpAnswer == tmpUser.pwd:
                                    print('Correct!')
                                    addAndReWrite(tmpUser, numCans)
                                else:
                                    print('Sorry, the password you entered was incorrect! ' + err_contact)
                            else:
                                print('Your input was not 1recognized...\n' + err_contact)
                        else:
                            print('It seems you\'ve tried to use multiple mode. The maximum number \nof marks you can register at once is 24, but you tried {}.'.format(numCans))
                    else:
                        print('Your input was not recognized...\n' + err_contact)
                else:
                    print('Your input was not recognized...\n' + err_contact)
        time.sleep(3)
        return 1


def main():

    print('---------------------------------------')
    print('- Welcome to "Øllistesystemet" v. 1.8 -')
    print('---------------------------------------')

    print('Adding users from directory users/ to user-list')
    for user_file in os.listdir('users/'):
        path = 'users/' + user_file
        addUserFromFile(path)

    if v: 
        print('\n--- PRINT ALL USERS: ---')
        for x in users:
            print('{}'.format(x))
            x.printStuff()
   
    keepGoing = 1
    while keepGoing:
        keepGoing = runForEver()

# Only RUN this file if it is run as a script and not loaded as a module
if __name__ == '__main__':
    main()

