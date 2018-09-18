#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
sys.path.append('../Modules/')

import userFuncs, refFuncs

payFolder = '../Data/Payment/'
# logPath = payFolder + 'manPayment.log'
makeLog = False

def main():

    if len(sys.argv) > 1:
        thresh = int(sys.argv[1])
    else:
        thresh = 999
    
    print('Welcome to Aeter RKI!')

    debt, netDebt = userFuncs.totalDebt()
    debt, netDebt = refFuncs.totalRefDebt(debt, netDebt)
    print(f'The current net debt is {netDebt} kr. with the following dispersion:')
    for interval in debt:
        print(f'  {interval} : {debt[interval]} kr.')
    print('')

    badUsers = []
    users = userFuncs.loadUsers()
    for user in users:
        if user.balance > thresh:
            badUsers.append(user)

    print(f'The following users have a balance above {thresh} kr.:')
    for user in badUsers:
         print(f'  {user.name}, {user.sduId} with a balnce of {user.balance} kr.')
    print('')
            

if __name__ == '__main__':
    main()
