#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import subprocess as sp
import csv
from backup import backup
from datetime import datetime, date
import sys
sys.path.append('../Modules/')

import userFuncs, refFuncs

mainFolder = '../'
payFolder = mainFolder + 'Data/Payment/'
indexDicts = {'MobPay':{'msg':9, 'amount':3, 'date':6}, 'NetBank':{'msg':2, 'amount':4, 'date':0}}
typeDict = {'Ord':['-Orig.csv', '-Tmp.csv'], 'Ref':['-Tmp.csv', '-AutoFinal.csv']}
logPath = payFolder + 'payment.log.n'
makeLog = True
today = datetime.now()

def plog(string, printIt=True):
    string += '\n'
    if makeLog:
        try:
            with open(logPath, 'a', encoding='utf-8') as logFile:
                print(string, file=logFile)
        except:
            with open(logPath, 'w', encoding='utf-8') as logFile:
                print(string, file=logFile)
    if printIt:
        print(string[:-1])

def intF(str):
    num = float(str.replace('.','').replace(',','.'))
    num = int(round(num))
    return num

def list2str(fileList):
    return '{' + ','.join(fileList) + '}'

def runProc(args, shell=False):
    if shell:
        out, err = sp.Popen(' '.join(args), stdout=sp.PIPE, stderr=sp.PIPE, shell=True).communicate()
    else:
        out, err = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE).communicate()
    return out.decode('utf-8'), err.decode('utf-8')

def main():
    plog('\nAuto payment log ' + today.strftime('%y.%m.%d %H:%M') + '\n')
    totalChanges = 0
    totalPaidAmount = 0
    netDebt, debt = refFuncs.totalRefDebt(userFuncs.totalDebt())
    plog(f'The current net debt is {netDebt} kr. with the following dispersion:')
    for interval in debt:
        plog(f'  {interval} : {debt[interval]} kr.')

    plog('\nArchiving previous payment files.')
    archiveFolder = payFolder + 'Archive/' + today.strftime('%y.%m.%d')
    count = 0
    while True:
        out, err = runProc(['mkdir', archiveFolder])
        if err != '':
            archiveFolder += f'-{count}'
            count += 1
        else:
            break

    fileList = glob(payFolder + '*.*')
    fileList.remove(logPath)
    runProc(['mv', payFolder + '*.*', archiveFolder], shell=True)
    runProc(['mv', archiveFolder + 'payment.log.n', logPath])

    plog('Trying to retrieve the *-Orig.csv from ~/beerlist/')
    fileList = glob(mainFolder + '*-Orig.csv')
    if len(fileList) != 2:
        plog('Failed, please fill NetBank-Templ.csv and MobPay-Templ.csv\n(located in ~/beerlist/) with their respective data, rename them\nto "*-Orig.csv" and run again.')
        runProc(['cp', payFolder + 'Archive/*-Templ.csv', mainFolder], shell=True)
        return
    else:
        plog('Succeeded.')
        runProc(['mv', mainFolder + '*-Orig.csv', payFolder], shell=True)

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
            idx = indexDicts[payType]
            plog(f'Loading {payType} data now.'.replace('Mob', 'Mobile'))
            with open(payFolder + payType + ending[0], 'r', encoding = 'utf8') as file0:
                with open(payFolder + payType + ending[1], 'w', encoding = 'utf8') as file1:
                    plog('\nFound the following matches (no-/anything to confirm/reject):')
                    reader = csv.reader(file0, dialect = 'excel')
                    writer = csv.writer(file1, dialect = 'excel')
                    for rRow in reader:
                        wFlag = 'not'
                        if rRow[idx['amount']] != 'Beløb':
                            msg = rRow[idx['msg']].lower()
                            amount = intF(rRow[idx['amount']])
                            payDate = list(reversed(rRow[idx['date']].replace('/', '.').split('.')))
                            payDate = date(*[int(x) for x in payDate])
                            for user in users:
                                if user.sduId in msg:
                                    outStr = f'    {user.sduId} matched the message:\n      "{msg}"\n    With a user balance of {user.balance} and a payment of:\n      {amount}\n'
                                    plog(outStr, False)
                                    wFlag = input(outStr)
                                    if  wFlag == '':
                                        user.paySome(amount, payDate)
                                        if userType == 'Ord':
                                            user.saveUser()
                                        else:
                                            if user.balance == 0:
                                                refUsers.remove(user)
                                            refFuncs.saveRefUsers(users)
                                        plog('\n    Okay, changes saved.\n')
                                        totalChanges += 1
                                        totalPaidAmount += amount
                                    else:
                                        plog('\n    Okay, changes has not been saved.\n')
                        if wFlag != '':
                            writer.writerow(rRow)
    runProc(['cp', payFolder + 'NetBank-AutoFinal.csv', mainFolder + 'NetBank-Final.csv'])
    runProc(['cp', payFolder + 'MobPay-AutoFinal.csv', mainFolder + 'MobPay-Final.csv'])
    plog("That's it for this time, please check the *-Final.csv files in ~/beerlist/,\nthese should be manually checked for missed entries, a good tool should be\nmanPayment.\nPlease remove the lines as you find them and move the files\nto ~/beerlist/Data/Payment/ when done.")
    plog(f'A total of {totalChanges} changes have been made adding up to a total paid amount\nof {totalPaidAmount} kr.!')

    netDebt, debt = refFuncs.totalRefDebt(userFuncs.totalDebt())
    plog(f'The new net debt is {netDebt} kr. with the following dispersion:')
    for interval in debt:
        plog(f'  {interval} : {debt[interval]} kr.')

    plog(f'\nPlease refer to the log of this run at ~/beerlist/Data/Payment/payment.log\n')
    runProc(['mv', logPath, logPath[:-2]])

if __name__ == '__main__':
    main()