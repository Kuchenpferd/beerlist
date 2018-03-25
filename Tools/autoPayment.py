#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh
import csv
import backup
from datetime import date
import sys
sys.path.append('../Modules/')

import userFuncs, refFuncs

payFolder = '../Data/Payment/'
indexDicts = {'MobPay':{'msg':9, 'amount':3}, 'NetBank':{'msg':2, 'amount':4}}
typeDict = {'Ord':['-Orig.csv', '-Tmp.csv'], 'Ref':['-Tmp.csv', '-AutoFinal.csv']}
logPath = payFolder + 'payment.log'
makeLog = True

def plog(string, printIt=True):
    if makeLog:
        try:
            with open(logPath, 'a', encoding='utf-8') as logFile:
                print(string, file=logFile)
        except:
            with open(logPath, 'a', encoding='utf-8') as logFile:
                print(string, file=logFile)
    if printIt:
        print(string)

def intF(str):
    return int(str.replace('.','').replace(',','.'))

def main():
    plog('Payment log ' + sh.date('+%y.%m.%d %H:%M'))
    try:
        plog('Trying to archive the previous payment files.')
        archiveFolder = payFolder + 'Archive/' + sh.date('+%y.%m.%d')
        count = 0
        while True:
            try:
                sh.mkdir(archiveFolder)
                break
            except:
                archiveFolder += str(count)
                count += 1

        sh.mv(payFolder + '*.csv', archiveFolder)
        sh.mv(payFolder + 'payment.log', archiveFolder)
        plog('Succeded.')
    except:
        plog('Failed, they might be backed up already.')
        pass

    try:
        plog('Trying to retrieve the *-Orig.csv from ~/beerlist/')
        sh.mv('../*-Orig.csv', payFolder)
    except:
        sh.cp(payFolder + 'Archive/*-Templ.csv', '..')
        plog('Failed, please fill NetBank-Templ.csv and MobPay-Templ.csv\n(located in ~/beerlist/) with their respective data, rename them\nto "*-Orig.csv" and run again.')
        return

    plog('Backing up all users and payment archives.')
    backup(mode='payment')

    for userType in typeDict:
        ending = typeDict[userType]
        users = []
        if userType == 'Ord':
            plog('Loading ordinary users.')
            users = userFuncs.loadUsers()
        else:
            plog('\nLoading reference users.')
            users = refFuncs.loadRefUsers()

        for payType in indexDicts:
            idx = indexDicts[paytype]
            plog(f'Loading {payType} data now.'.replace('Mob', 'Mobile'))
            with open(payFolder + payType + ending[0], 'r', encoding = 'utf8') as file0:
                with open(payFolder + payType + ending[1], 'w', encoding = 'utf8') as file1:
                    plog('\n\nFound the following matches (no-/anything to confirm/reject):')
                    reader = csv.reader(file0, dialect = 'excel')
                    writer = csv.writer(file1, dialect = 'excel')
                    for rRow in reader:
                        wFlag = 'not'
                        msg = rRow[idx['msg']]
                        amount = intF(rRow[idx['amount']])
                        for user in users:
                            if user.sduId in rRow[idx['msg']]:
                                outStr = f'    {user.sduId} matched the message:\n      "{msg}"\n    With a user balance of {user.balance} and a payment of:\n      {amount}\n'
                                plog(outStr, False)
                                wFlag = input(outStr)
                                if  wFlag == '':
                                    user.balance -= amount
                                    user.lastPay = date.today()
                                    if userType == 'Ord':
                                        user.saveUser()
                                    else:
                                        refFuncs.saveRefUsers(users)
                                    plog('\n    Okay, changes saved.\n')
                                else:
                                    plog('\n    Okay, changes has not been saved.\n')
                        if wFlag != '':
                            writer.writerow(rRow)
    sh.cp(payFolder + 'NetBank-AutoFinal.csv', '../NetBank-Final.csv')
    sh.cp(payFolder + 'MobPay-AutoFinal.csv', '../MobPay-Final.csv')
    plog("That's it for this time, please check the *-Final.csv files in ~/beerlist/,\nthese should be manually checked for missed entries,\na good tool should be manPayment.\nPlease remove the lines as you find them\nand move the files to ~/beerlist/Data/Payment/ when done.")

if __name__ == '__main__':
    main()