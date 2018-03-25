#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../Modules/')

import argparse
import sh, os

GoogleDrivePath = '/home/pi/GoogleDrive/'
DataPath = '/home/pi/beerlist/Data/'

parser = argparse.ArgumentParser(description='A script to make and upload backups of our data.')
parser.add_argument('mode', type=str, choices=['users', 'stats', 'party', 'payment', 'all'], help='Choose one of these modes to backup up the according files. Note that "party" and "payment", are simply to have a separate folder for rapid backups during parties and a specific folder for payment-related back ups.')
parser.add_argument('-clean', action='store_true', default=False, help='Add this flag to clean the Google Drive folder of the specified update mode. The files for the last month are kept for all but "all-mode", which retains the last 2 months worth of data, and "party-mode", which cleans all data. (In the subfolder)')

def backup(mode=None, clean=False):

    if mode is None:
        args = parser.parse_args()
        mode = args.mode
        clean = args.clean

    GoogleDriveSub = f'{mode}_backup'
    FileMask = f'{mode}_backup_'
    DataSub = mode.title()
    SecDataSub = ''
    CleanTime = 1

    if mode == 'party':
        DataSub = 'Users'
        CleanTime = 0
    elif mode == 'all':
        DataSub = '../..'
        CleanTime = 2
    elif mode == 'payment':
        DataSub = 'Users'
        SecDataSub = 'Payment/Archive'
        CleanTime = 3

    if not clean:

        DateStamp = sh.date('+%y.%m.%d_%H-%M')
        BackupFile = f'{FileMask}{DateStamp}.tar.gz'
        FullFilePath = f'{GoogleDrivePath}{GoogleDriveSub}/{BackupFile}'

        sh.cd(DataPath)
        sh.tar('czf', FullFilePath, DataSub, SecDataSub)

        sh.cd(GoogleDrivePath)
        output = os.popen(f'grive -u -s {GoogleDriveSub}')
        print(output)

        sh.sleep('1s')

        with open('.griveignore', 'a') as file:
            file.write(f'{GoogleDriveSub}/{BackupFile}\n')

    else:

        LastDate = sh.date('+%d', date=f'{CleanTime} month ago')
        LastMonth = sh.date('+%m', date=f'{CleanTime} month ago')
        LLastMonth = sh.date('+%m', date=f'{CleanTime + 1} month ago')

        Mask1 = f'{FileMask}*.{LastMonth}.[0-{LastDate[0]}][0-{LastDate[1]}]_*-*.tar.gz'
        Mask2 = f'{FileMask}*.{LLastMonth}.[0-9][0-9]_*-*.tar.gz'

        sh.cd(GoogleDrivePath)
        output = os.popen(f'grive -f -s {GoogleDriveSub}')
        print(output)

        sh.sleep('1s')

        sh.rm('-f', f'{GoogleDrivePath}{GoogleDriveSub}/{Mask1}')
        sh.rm('-f', f'{GoogleDrivePath}{GoogleDriveSub}/{Mask2}')

        output = os.popen(f'grive -s {GoogleDriveSub}')
        print(output)

        sh.sleep('1s')

        sh.grep('-v', f'{GoogleDriveSub}/{Mask1}', '.griveignore', _out='tmp')
        sh.grep('-v', f'{GoogleDriveSub}/{Mask2}', 'tmp', _out='.griveignore')
        sh.rm('-f', 'tmp')

    sh.rm('-f', f'{GoogleDrivePath}{GoogleDriveSub}/*.tar.gz')

if __name__ == '__main__':
    backup()