#!/usr/bin/python
# -*- coding: utf-8 -*-

## NOTE:
## This script will only work on a Windows system (presumably?) that has an Outlook client installed,
## with a single (presumably?) SDU account setup, and after the GAL has been downloaded for offline use.

# Requires the package pywin32 to be installed (Note that you might have to run more than PIP!)
import win32com.client
import csv

# Function to update the overall mail lists
def updateLists():
    # First we create two lists containing the name of the GAL lists and the destination filenames
    listNames = ['All Staff', 'All Students']
    fileNames = ['../Data/allStaff.csv', '../Data/allStudents.csv']

    # We then repeat the process for each of the two GAL lists
    for i in range(2):
        # We then connect to the Outlook files and find the required contacts
        outlookMAPI = win32com.client.gencache.EnsureDispatch('Outlook.Application').GetNamespace('MAPI')
        contacts = outlookMAPI.AddressLists.Item(listNames[i]).AddressEntries

        # The counters are only for visualization of the progress of the process
        totalContacts = contacts.Count
        count = 1

        # We then open the file to write
        path = fileNames[i]
        with open(path, 'w', newline = '', encoding = 'utf-8') as file:
            rowWriter = csv.writer(file)

            # Each contact get their own row and the relevant properties are written
            for container in contacts:
                contact = container.GetExchangeUser()
                rowWriter.writerow([contact.Name, contact.PrimarySmtpAddress])

            # Again, for visualization
            count += 1
            if count%50 == 0:
                print(f'{count} out of {totalContacts}')

        # And again for visualization
        if i == 0:
            print('Partly finished!')
        else:
            print('Finished!')

# The usual header
def main():
    updateLists()
if __name__ == '__main__':
    main()