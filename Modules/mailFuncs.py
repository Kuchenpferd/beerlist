#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pyqrcode
from hashlib import sha256
from string import ascii_letters, digits
from random import randrange
from exchangelib import DELEGATE, Account, Credentials, Configuration, Message, Mailbox, FileAttachment, HTMLBody

# Path to determine the data folder (Should be changed to './Data/', when imported)
workFolder = '../'

# Additional destinations
resourceFolder = workFolder + 'Resources/'
dataFolder = workFolder + 'Data/Permanent/'

# A minimal function to convert the plain string message to an HTML string
def plainToHtml(plainString):
    htmlString = """<html><body>""" + plainString.replace('\n','<br>') + """</body></html>"""
    return htmlString

# Another small function that encodes an URL with ASCII
def asciiEncodeUrl(url):
    keys = [('!','%21'), ('*','%2A'), ("'",'%27'), ('(','%28'), (')','%29'), (';','%3B'), (':','%3A'), ('@','%40'), ('&','%26'),
            ('=','%3D'), ('+','%2B'), ('$','%24'), (',','%2C'), ('/','%2F'), ('?','%3F'), ('#','%23'), ('[','%5B'), (']','%5D')]

    for key, code in keys:
        url = url.replace(key, code)
    return url

# A small function to set up a small "dict" for every text mention of '{url}SOMETHING{/url}'
# in the mail text. It also handles the setup of the AppRedirect URL, then return the mentioned dict
def htmlUrls(urlTexts, altUrl, mobilePayUrl):

    # ASCII encoding the two URL that go into the AppRedirect URL
    altUrl = asciiEncodeUrl(altUrl)
    mobilePayUrl = asciiEncodeUrl(mobilePayUrl)

    # Then setting up the AppRedirect URL
    rdctUrl = f'http://rdct.it?site={altUrl}&app={mobilePayUrl}'

    # And finally creating the dict to be used for substitutions later
    urlSubs = []
    for urlText in urlTexts:
        urlSubs.append((f'{{url}}{urlText}{{/url}}', f'<a href={rdctUrl}>{urlText}</a>'))

    return urlSubs

# A small function that generates a new random password
def genNewPwd(pwdLen = 8):

    # The character is made up from all ASCII letters and the digits (imported from 'string')
    # The length of the list is also found
    charList = ascii_letters + 6*digits
    charLen = len(charList)

    # The new password is set to an empty string
    newPwd = ''

    # Each iteration a new random char from the char list is added to the password
    for i in range(pwdLen):
        newPwd += charList[randrange(charLen)]

    # At last the new password is returned
    return newPwd

# A function that generates a QR code for MobilePay, and returns the path to the code
def generateQR(user, extraAmount, returnUrl = False):

    # The amount is determined from the user balance and some extra amount
    # (the extra amount can be negative). If the amount is below zero,
    # it is automatically set to 0.
    amount = user.balance + extraAmount
    if amount < 0:
        amount = 0
        
    # The QR content and the command string is created and then the command is run in the shell
    qrContent = f'mobilepay://send?amount={amount}&phone=98050&comment={user.sduId}'
    qrCode = pyqrcode.create(qrContent, error = 'M', version = 6, mode = 'binary')
    qrCode.png(resourceFolder + 'qrcode.png', scale = 6, module_color = [0, 0, 0, 255], background = [0xff, 0xff, 0xff])

    # Afterwards the path to the picture is returned, along with the content of the QR
    # code (only if explicitly requested)
    if returnUrl:
        return resourceFolder + 'qrcode.png', qrContent
    else:
        return resourceFolder + 'qrcode.png'

# A function that handles the login and authentication process with the Exchange server,
# then returns the 'account' (similar to a 'session') object
def loginExchange(returnSender=False):

    # First all the required mail credentials are loaded from its file and stored in the relevant variables
    path = dataFolder + 'mailCredentials.t'
    with open(path, 'r') as credFile:
        content = credFile.read().splitlines()
        senderMail = content[0]
        pwdMail = content[1]
        serverAdress = content[2]
        loginUsername = content[3]

    # The credentials, configuration and account/session is then setup and then returned.
    credentials = Credentials(username=loginUsername, password=pwdMail)
    config = Configuration(server=serverAdress, credentials=credentials)
    account = Account(primary_smtp_address=senderMail, config=config, autodiscover=False, access_type=DELEGATE)
    if returnSender:
        return account, senderMail
    else:
        return account

# A function to send mails to user. There are three mail types, 'Debt', 'Pwd' and 'ManBalance'.
# If the mail type is 'Pwd', a new pwd is created for user and then sent to their mail.
# A succesfully sent mail returns True and an unsuccesfull returns False.
#
# If the mail type is 'Debt', the input param user should actually be a list of users,
# who will each recieve a 'debt' mail if their balance is above the debtLimit.
# A set of tuples is returned, containg a boolean flag for each user, which is True if their balance
# is above the debtLimit and succesfully recieved a mail and False in any other case (mail not sent or low balance)
# 
# If the mail type is 'ManBalance', the user was created with a manually entered balance. 
# Any such creation is potentially suspicious and a mail is thus send to the cashier so that he/she
# can check up on the creation if neccesary.
def sendMail(user, mailType = 'Debt', debtLimit = 0):

    # 'Pwd' mail
    if mailType == 'Pwd':

        # We generate a random password and find the SHA256 hash
        newPwd = genNewPwd()
        newPwdHash = sha256(newPwd.encode()).hexdigest()

        # The mail text for a 'Pwd' mail is loaded and converted to HTML
        path = dataFolder + 'newPwdMail.t'
        with open(path, 'r', encoding='utf-8') as mailFile:
            messageText = plainToHtml(mailFile.read())

        # Next the user specific information is substituted in the mail
        # Valid substitutes are (so far): {name}, {sduId} and {pwd}
        subList = [('{name}', user.name), ('{sduId}', user.sduId), ('{pwd}', newPwd)]
        for key, subst in subList:
            messageText = messageText.replace(key, subst)
        
        # A connection is made to the Exchange server
        account = loginExchange()

        # And a message is created
        message = Message(account = account,
                          folder = account.sent,
                          subject = 'Nyt password til Æters Ølliste',
                          body = HTMLBody(messageText),
                          to_recipients = [Mailbox(email_address = user.mail)])

        try:

            # We then try sending the message, and if it succeds the users pwd is overwritten
            # and the user is saved.
            message.send_and_save()
            user.pwd = newPwdHash
            user.saveUser()
            sent = True

        except:

            # If sending it fails a flag is set to False
            sent = False

        # The connection is closed and the flag is returned
        account.protocol.close()
        return sent

    # 'Debt' mails
    elif mailType == 'Debt':

        # As 'Debt' means that 'user' is actually a list and for ease of reading it is renamed to reflect that
        users = user

        # The list of tuples to be returned
        usersStatus = []

        # Next the template text of the 'Debt' mail is loaded and (roughly) converted to HTML
        path = dataFolder + 'debtMail.t'
        with open(path, 'r', encoding='utf-8') as mailFile:
            templateText = plainToHtml(mailFile.read())

        # The URL any (non-mobile) webbrowser will show when the embedded hyperlink is pressed
        altUrl = 'https://www.facebook.com/aeter.sdu/'

        # Any embedded URL should be referenced in the template as '{url}Text here{/url}' where
        # the middle text will be the text of the hyperlink.
        # Please note that though this script (as of now) supports multiple URL in the same text,
        # the destination will always be the same.
        # 
        # Any embedded URLs in the template are identified and listed
        urlTexts = []
        startIndex = 0
        while True:
            tmpIndex = templateText[startIndex:].find('{url}') + startIndex + 5
            if tmpIndex - startIndex != 4:
                startIndex = tmpIndex
                endIndex = templateText[startIndex:].find('{/url}') + startIndex
                urlTexts.append(templateText[startIndex:endIndex])
            else:
                break

        # A connection to the Exchange server is created
        account = loginExchange()

        # Next the user independent part of the message is set up
        message = Message(account = account,
                          folder = account.sent,
                          subject = 'Opgørelse af Æters Ølliste')

        # Looping over all users
        for user in users:

            # Checking if the user balance is indeed above the debtLimit
            if user.balance > debtLimit:

                # A custom QR code and MobilePay URL are generated
                qrCodePath, mobilePayUrl = generateQR(user, extraAmount = 0, returnUrl = True)

                # A "dict" over the proper (AppRedirect) URLs is created from the custom MP URLs
                urlSubs = htmlUrls(urlTexts, altUrl, mobilePayUrl)

                # Next the user specific information is substituted in the template
                # Valid substitutes are (so far): {name}, {sduId}, {qrcode} and {url}TEXT HERE{/url}
                subList = [('{name}', user.name), ('{sduId}', user.sduId), ('{qrcode}', f'<img src="cid:{qrCodePath[-10:-4]}">')] + urlSubs
                messageText = templateText
                for key, subst in subList:
                    messageText = messageText.replace(key, subst)

                # Next the newly created QR code is loaded into a file attachment
                with open(qrCodePath, 'rb') as qrFile:
                    qrImage = FileAttachment(name = qrCodePath[-10:-4], content = qrFile.read())

                # The remaining message parameters are set (including attaching the QR code)
                message.attach(qrImage)
                message.body = HTMLBody(messageText)
                message.to_recipients = [Mailbox(email_address = user.mail)]

                try:

                    # The message is then sent and the user/True tuple is added to the out list if succesfull
                    message.send_and_save()
                    usersStatus.append((user, True))
                except:

                    # If the message is not sent, the user/False tuple is added instead
                    usersStatus.append((user, False))

            else:

                # If the user has a balance below the debtLimit, the user/False tuple is added to the out list.
                # (They can be differentiated from failed attempts at sending later on.)
                usersStatus.append((user, False))

        # In the end, the connection is closed and the tuples list is returned
        account.protocol.close()
        return usersStatus

    # 'ManBalance' mails
    elif mailType == 'ManBalance':

        # The content of the manual balance mail is created on spot
        plainText = f"""
            Hi Cashier,

            A user named {user.name.split()[0]} has just been created with a manual
            balance input of {user.balance}.

            Further user properties are:
                Name:       {user.name}
                Sdu-Id:     {user.sduId}
                Mail:       {user.mail}
                User no.:   {user.number}
                Balance:    {user.balance}

            Best regards,
            The Beerlist
            """[1:].replace('            ','')

        # And it is then converted to HTML
        messageText = plainToHtml(plainText)
        
        # A connection is made to the Exchange server
        account, mail = loginExchange()

        # And a message is created
        message = Message(account = account,
                          folder = account.sent,
                          subject = 'Nyt password til Æters Ølliste',
                          body = HTMLBody(messageText),
                          to_recipients = [Mailbox(email_address = mail)])

        try:

            # We then try sending the message
            message.send_and_save()
            sent = True

        except:

            # If sending it fails a flag is set to False
            sent = False

        # The connection is closed and the flag is returned
        account.protocol.close()
        return sent

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
