#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sh, os

GoogleDrivePath = '/home/pi/GoogleDrive/'
DataPath = '/home/pi/beerlist/Data/'

parser = argparse.ArgumentParser(description='A script to make and upload backups of our data.')
parser.add_argument('mode', type=str, choices=['users', 'stats', 'party', 'all'])
parser.add_argument('-clean', action='store_true', default=False)

def main():
    args = parser.parse_args()
    mode = args.mode
    clean = args.clean

    GoogleDriveSub = f'{mode}_backup'
    FileMask = f'{mode}_backup_'
    DataSub = mode.title()
    CleanTime = 1

    if mode == 'party':
        DataSub = 'Users'
    elif mode = 'all':
        DataSub = '../..'
        CleanTime = 2

    if not clean:

        DateStamp = sh.date('+%y.%m.%d_%H-%M')
        BackupFile = f'{FileMask}{DateStamp}.tar.gz'
        FullFilePath = f'{GoogleDrivePath}{GoogleDriveSub}/{BackupFile}'

        sh.cd(DataPath)
        sh.tar('-czf', FullFilePath, DataSub)

        sh.cd(GoogleDrivePath)
        output = os.popen(f'grive -u -s {GoogleDriveSub}')

        ## Check ouput for errors before proceeding!!!

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

        ## Check ouput for errors before proceeding!!!

        sh.sleep('1s')

        sh.rm('-f', f'{GoogleDrivePath}{GoogleDriveSub}/{Mask1}')
        sh.rm('-f', f'{GoogleDrivePath}{GoogleDriveSub}/{Mask2}')

        output = os.popen(f'grive -s {GoogleDriveSub}')

        ## Check ouput for errors before proceeding!!!

        sh.sleep('1s')

        sh.grep('-v', f'{GoogleDriveSub}/{Mask1}', '.griveignore', _out='tmp')
        sh.grep('-v', f'{GoogleDriveSub}/{Mask2}', 'tmp', _out='.griveignore')
        sh.rm('-f', 'tmp')

    sh.rm('-f', f'{GoogleDrivePath}{GoogleDriveSub}/*.tar.gz')

if __name__ == '__main__':
    main()