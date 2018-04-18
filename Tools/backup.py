#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess as sp
from datetime import datetime
from dateutil.relativedelta import relativedelta

bucketPath = 'gs://aeterbackup/'
DataPath = '../Data/'

parser = argparse.ArgumentParser(description='A script to make and upload backups of our data.')
parser.add_argument('mode', type=str, choices=['users', 'stats', 'party', 'payment'], help='Choose one of these modes to backup up the according files. Note that "party" and "payment", are simply to have a separate folder for rapid backups during parties and a specific folder for payment-related back ups.')
parser.add_argument('-clean', action='store_true', default=False, help='Add this flag to clean the Google Drive folder of the specified update mode. The files for the last month are kept for all but "party-mode", which cleans all data. (In the subfolder)')

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def rg2gr(expr):
    expr = expr.replace('.', '\.').replace('*', '.*')
    return expr

def date(monthsBack=0):
    dT = relativedelta(months=-monthsBack)
    date = datetime.now() + dT
    return date

def runProc(args, shell=False):
    if shell:
        out, err = sp.Popen(' '.join(args), shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()
    else:
        out, err = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE).communicate()
    out, err = out.decode('utf-8'), err.decode('utf-8')
    print(out, err)
    return out, err

def backup(mode=None, clean=False):

    if mode is None:
        args = parser.parse_args()
        mode = args.mode
        clean = args.clean

    bucketSub = f'{mode.title()}/'
    FileMask = f'{mode}_backup_'
    DataSub = mode.title()
    SecDataSub = ''
    CleanTime = 1

    if mode == 'party':
        DataSub = 'Users'
        CleanTime = 0
    elif mode == 'payment':
        DataSub = 'Users'
        SecDataSub = 'Payment/Archive'
        CleanTime = 3

    if not clean:

        DateStamp = date().strftime('%y.%m.%d_%H-%M')
        BackupFile = f'{FileMask}{DateStamp}.tar.gz'

        with cd(DataPath):
            runProc(['tar', 'czf', BackupFile, DataSub, SecDataSub], True)
            runProc(['gsutil', 'mv', BackupFile, bucketPath + bucketSub], True)

    else:

        LastDate = date(CleanTime).strftime('%d')
        LastMonth =  date(CleanTime).strftime('%m')
        LLastMonth =  date(CleanTime + 1).strftime('%m')    

        Mask1 = f'{FileMask}*.{LastMonth}.[0-{LastDate[0]}][0-{LastDate[1]}]_*-*.tar.gz'
        Mask2 = f'{FileMask}*.{LLastMonth}.[0-9][0-9]_*-*.tar.gz'

        runProc(['gsutil', 'rm', '-f', bucketPath + bucketSub + Mask1], True)
        runProc(['gsutil', 'rm', '-f', bucketPath + bucketSub + Mask2], True)

if __name__ == '__main__':
    backup()