#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
sys.path.append('../Modules/')

import userFuncs, refFuncs

payFolder = '../Data/Payment/'
logPath = payFolder + 'manPayment.log'
makeLog = True

def plog(string, printIt=True):
    if makeLog:
        try:
            with open(logPath, 'a', encoding='utf-8') as logFile:
                print(string, file=logFile)
        except:
            with open(logPath, 'w', encoding='utf-8') as logFile:
                print(string, file=logFile)
    if printIt:
        print(string)

def inplog(string):
    plog(string)
    inString = input(string + '\n')
    if inString == '':
        outString = '(input): *accept*'
    else:
        outString = f'(input): {inString}'
    plog(outString, False)
    return inString

def main():
    plog(f'\nLog for manual payment entries: {datetime.now()}\n', False)
    plog('Welcome to manual payment entries!')
    totalChanges = 0
    totalPaidAmount = 0
    while True:
        exitFlag = False
        inString = inplog('Enter part/all of a name or sduId:')
        while True:
            matchedUsers = userFuncs.searchUsers(inString)
            matchedRefIdxs, refUsers = refFuncs.searchRefUsers(inString)

            if inString.lower() == 'exit':
                exitFlag = True
                break

            if len(matchedUsers) == 1 and matchedRefIdxs == []:
                user = matchedUsers[0]
                plog(f'  Found (ord): {user.sduId}, {user.name} with a {user.balance} balance.')
                inString = inplog('Press enter to accept or type in a new query:')
                if inString == '':
                    matchType = '(ord)'
                    match = user
                    break

            elif len(matchedRefIdxs) == 1 and matchedUsers == []:
                user = reUsers[matchedRefIdxs[0]]
                plog(f'  Found (ref): {user.sduId}, {user.name} with a {user.balance} balance.')
                inString = inplog('Press enter to accept or type in a new query:')
                if inString == '':
                    matchType = '(ref)'
                    match = matchedRefIdxs[0]
                    break

            elif matchedUsers and matchedRefIdxs == []:
                plog('  No matches found at all.')
                inString = inplog('Please type in another query:')

            else:
                if matchedUsers != []:
                    plog('  Found the following ordinary users:')
                    for i, user in enumerate(matchedUsers):
                        plog(f'    {i}: {user.sduId}, {user.balance}, {user.name}')
                    if len(matchedUsers) == 0:
                        i = -1
                    refStart = i + 1
                else:
                    plog('  No matches found in the ordinary users.')
                    refStart = 0

                if matchedRefIdxs != []:
                    plog('  Found the following reference users:')
                    for i, refIdx in matchedRefIdxs:
                        refUser = refUsers[refIdx]
                        plog(f'    {i+refStart}: {refUser.sduId}, {refUser.balance}, {refUser.name}')
                    if len(matchedRefIdxs) == 0:
                        i = -1
                    refEnd = i + refStart + 1
                else:
                    plog('  No matches found in the reference users.')

                inString = inplog('Enter a number to choose that user or type in a new query:')
                try:
                    inInt = int(inString)
                    if inInt in range(refEnd):
                        if inInt in range(refStart):
                            matchType = '(ord)'
                            match = matchedUsers[inInt]
                        else:
                            matchType = '(ref)'
                            match = matchedRefIdxs[inInt - refStart]
                        break
                except:
                    pass

            if exitFlag:
                break

            if matchType == '(ref)':
                user = refUsers[match]
            else:
                user = match

            plog(f'Chosen user: {user.sduId}, {user.balance}, {user.name}')
            inString = inplog('Please enter paid amount:')
            while True:
                if inString.lower() == 'exit':
                    exitFlag = True
                    break
                elif inString.lower() == 'back':
                    amount = ''
                    break
                try:
                    if inString == '':
                        inString = '0'
                    amount = int(inString)
                    break

                except ValueError:
                    inString = inplog('Not a number, please try again ("back" return to queries, nothing equals "0"):')

            if exitFlag:
                break

            if type(amount) is int:
                user.paySome(amount)
                plog(f'Corrected {matchType} user to: {user.sduId}, {user.balance}, {user.name}')
                inString = inplog('Save these changes (no-/anything to accept/decline)?')
                if inString == '':
                    if matchType = '(ord)':
                        user.saveUser()
                        plog('User saved.\n')
                    else:
                        if user.balance == 0:
                            refUsers.remove(user)
                        refFuncs.saveRefUsers(refUsers)
                        plog('Reference users saved.\n')
                    totalChanges += 1
                    totalPaidAmount += amount

                elif inString.lower() == 'exit':
                    plog('Nothing was changed.\n')
                    break
                else:
                    plog('Nothing was changed.\n')

    plog('\nExiting!')
    plog(f'Made a total of {totalChanges} adding up to a total paid amount of {totalPaidAmount} kr.!')
    plog(f'Please refer to the log of this run at {logPath}\n')

if __name__ == '__main__':
    main()