#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('../Modules/')

import userFuncs, refFuncs, mailFuncs

debtLimit = 0

parser = argparse.ArgumentParser(description='A script to send mail to all users with a balance above the supplied debtLimit.')
parser.add_argument('debtLimit', type=int, default=0, help='A debtLimit to determine which users recieve a mail. Defaults to 0.')

def sendMails(debtLimit=None):

    if debtLimit is None:
        debtLimit = parser.parse_args().debtLimit

    userType = ['ordinary', 'reference']
    userLists = []
    userLists.append(userFuncs.loadUsers())
    userLists.append(refFuncs.loadRefUsers())
    for i, users in enumerate(userLists):
        users = [user for user in users if user.balance > debtLimit]
        usersTup = mailFuncs.sendMail(users, 'Debt', debtLimit)

        mailSent = 0
        for user, sent in usersTup:
            if not sent:
                print(f'Failed to sent mail to {user.sduId}')
            else:
                mailSent += 1
        print(f'Sent {mailSent} of {len(usersTup)} mails to {userType[i]} users.')

if __name__ == '__main__':
    sendMails()