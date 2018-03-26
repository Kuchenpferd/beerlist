#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import os, csv
import sys
sys.path.append('../Modules/')

import statFuncs

statFolder = '../DataStats/'
statFile = '../stats.csv'

def main():
    allStats = statFuncs.loadAllStats()
    allStats.sort(key=lambda stat: stat.dateTime)
    with open(statFile, 'w') as csvFile:
        writer = csv.writer(csvFile, dialect='excel')
        writer.writerow(['Year', 'Month', 'Day', 'Week', 'Weekday', 'Hour', 'No. marks', 'No. new users'])
    for stat in allStats:
        y = stat.dateTime.year
        m = stat.dateTime.month
        d = stat.dateTime.day
        w = stat.week
        wd = stat.dayOfWeek
        h = stat.dateTime.hour
        nm = stat.units
        nnu = stat.newUsers
        with open(statFile, 'a') as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            writer.writerow([y, m, d, w, wd, h, nm, nnu])

if __name__ == '__main__':
    main()