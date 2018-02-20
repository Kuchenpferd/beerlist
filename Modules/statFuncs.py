#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date, datetime

# Path to determine the data folder (Should be changed to './Data/', when imported)
workFolder = './../'

# Additional destinations
dataFolder = workFolder + 'Data/'

# The class that contains an hour-specific statistic
class statInstance(object):

    # The properties of the stat instance is initialized, with the capability of creating
    # a totally empty stat with no input arguments
    def __init__(self, units = 0, newUsers = 0, yearAndMonth = 1, dayOfMonth = 1, hour = 1):

        # Once again, we know that we need to determine the "standard" properties if
        # yearAndMonth = 1
        if yearAndMonth == 1:
            yearAndMonth = date.today().strftime('%y-%m')
            dayOfMonth = date.today().day
            hour = datetime.now().hour

        # All arguments are then turned into properties of the statistic
        self.units = int(units)
        self.newUsers = int(newUsers)
        self.yearAndMonth = yearAndMonth
        self.dayOfMonth = int(dayOfMonth)
        self.hour = int(hour)

    # Internal function, that adds 'units' to the relevant 'statType' property
    def addSome(self, statType, units = 1):
        if statType == 'Mark':
            self.units += units
        elif statType == 'User':
            self.newUsers += units

# A function that load the statistics file specific to the 'yearAndMonth' specified
# (stat files are named by yearAndMonth) and returns a list of stats
def loadStats(yearAndMonth, stats = []):

    # First the path is set to the specific file
    path = dataFolder + 'Statistics/' + yearAndMonth

    # As the specific stat file might not exist, a try/catch is set up with a FileNotFound catch
    try:
        # Assuming the file exists, it is opened and it's content split into lines
        with open(path, 'r', encoding = 'utf-8') as statFile:
            content = statFile.read().splitlines()

            # As each line contains one instance of a stat, the content of each is
            # put into the relvant variables
            for line in content:
                lineContent = line.split(' ')
                units = lineContent[1]
                newUsers = lineContent[2]
                dayOfMonth = lineContent[0]
                hour = lineContent[3]

                # An instance of stat is then created and appended to the stats list
                tmpStat = statInstance(units, newUsers, yearAndMonth, dayOfMonth, hour)
                stats.append(tmpStat)

    except FileNotFoundError:
        # In case the file does not already exist, an empty instance of stat is created
        # and added as the single element of of 'sts'
        tmpStat = statInstance()
        stats.append(tmpStat)
        
    # At last the list is returned
    return stats

# A function that writes the elements of the list 'stats'
def saveStats(stats):

    # As all stats in a list can only have the same yearAndMonth
    # (per definition; see loadStats) it is fetched from the fist element
    # and the file path is set.
    yearAndMonth = stats[0].yearAndMonth
    path = dataFolder + 'Statistics/' + yearAndMonth

    # The stat file is opened and each stat is written  on its own line
    with open(path, 'w', encoding = 'utf-8') as statFile:
        for stat in stats:
            line = '{} {} {} {}\n'.format(stat.dayOfMonth, stat.units, stat.newUsers, stat.hour)
            statFile.write(line)

# A function that updates the overall stats given the statType and units
def updateStats(statType, units = 1):

    # First of the current yearAndMonth, dayOfMonth and hour is determined
    yearAndMonth = date.today().strftime('%y-%m')
    dayOfMonth = date.today().day
    hour = datetime.now().hour
    
    # Then the relevant stats list is created by loading the stats
    stats = loadStats(yearAndMonth)

    # A True flag is set up to determine if any stat matches both the current dayOfMonth and hour;
    # If there is a match, addSome is called for the specific stat, and the flag is set to False
    # and the llop is broken (as ony one stat can match)
    flag = True
    for stat in stats:
        if stat.dayOfMonth == dayOfMonth and stat.hour == hour:
            stat.addSome(statType, units)
            flag = False
            break

    # If the flag is still True after the loop is done, no stat matched
    # the current dayOfMonth and hour and thus a new instance should be created,
    # and have addSome run before being appended to the 'stats' list
    if flag:
        tmpStat = statInstance()
        tmpStat.addSome(statType, units)
        stats.append(tmpStat)

    # The new 'stats' list is then saved
    saveStats(stats)

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
