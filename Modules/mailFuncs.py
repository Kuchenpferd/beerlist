#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import smtplib
from userFuncs import saveUser
from hashlib import sha256
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import ascii_letters, digits
from random import randrange

# Path to determine the data folder (Should be changed to './Data/', when imported)
workFolder = './'

# Additional destinations
resourceFolder = workFolder + 'Resources/'
dataFolder = workFolder + 'Data/'

# A minimal function to convert the plain string message to an HTML string
def plainToHtml(plainString):
    htmlString = """\<html><head></head><body><p>""" + plainString.replace('\n','<br>') + """</p></body></html>"""
    return htmlString

# A small function that generates a new random password
def genNewPwd(pwdLen = 8):

    # The character is made up from all ASCII letters and the digits (imported from 'string')
    # The length of the list is also found
    charList = ascii_letters + digits
    charLen = len(charList)

    # The new password is set to an empty string
    newPwd = ''

    # Each iteration a new random char from the char list is added to the password
    for i in range(pwdLen):
        newPwd += charList[randrange(charLen)]

    # At last the new password is returned
    return newPwd

# A function that generates a QR code for MobilePay, and returns the path to the code
def generateQR(user, extraAmount, returnLink = False):

    # The amount is determined from the user balance and some extra amount
    # (the extra amount can be negative). If the amount is below zero,
    # it is automatically set to 0.
    amount = user.balance + extraAmount
    if amount < 0:
        amount = 0
        
    # The QR content and the command string is created and then the command is run in the shell
    qrContent = '"mobilepay://send?amount={}&phone=98050&comment={}"'.format(amount, user.sduId)
    command = 'qrencode -s 10 -l M -o ' + resourceFolder + 'qrcode.png ' + qrContent
    os.system(command)

    # Afterwards the path to the picture is returned, along with the content of the QR
    # code (only if explicitly requested)
    if returnLink:
        return resourceFolder + 'qrcode.png', qrContent
    else:
        return resourceFolder + 'qrcode.png'

# A function to send mails to user. There are two mail types, 'Debt' and 'Pwd'.
# The function returns True if the mail was succesfully sent (or skipped, see below),
# and returns false if it tried sending the mail thrice (once) for debt (pwd) and still failed
def sendMail(user, mailType = 'Debt', debtLimit = 0):

    # If the type is debt, and the current users balance is below the debtLimit, they will not receive a mail
    if mailType == 'Debt' and user.balance <= debtLimit:
        return True

    # First all the required mail credentials are loaded from its file and stored in the relevant variables
    path = dataFolder + 'mailCredentials.t'
    with open(path, 'r') as credFile:
        content = credFile.read().splitlines()
        senderMail = content[0]
        pwdMail = content[1]
        smtpServer = content[2]
        loginUsername = content[3]

    # As we want to be able to use both pictures and links, the root message must be a multipart object with subtype related
    msgRoot = MIMEMultipart('related')

    # From, To and preamble (?) is set for the message
    msgRoot['From'] = senderMail
    msgRoot['To'] = user.mail
    msgRoot.preamble = 'Where will this go?'

    # Sets up the mail to be a password reset mail
    if mailType == 'Pwd':

        # First of we get the mail content from a file
        path = dataFolder + 'newPwdMail.t'
        with open(path, 'r') as mailFile:
            plainText = mailFile.read()

        # Next we generate a random password and finds the SHA256 hash
        newPwd = genNewPwd()
        newPwdHash = sha256(newPwd.encode()).hexdigest()

        # The subject line for the mail is set as well
        msgRoot['Subject'] = 'Nyt password til Æters Ølliste'

        # Next the user custom information and the password is substituted in the mail
        # Valid substitutes are (so far): {name}, {sduId} and {pwd}
        plainTxt = plainTxt.format(name = user.name, sduId = user.sduId, pwd = newPwd)
        
        # The text is then converted to HTML format
        htmlText = plainToHtml(plainText)

    # Sets up the mail to be a debt mail
    elif mailType == 'Debt':

        # As debt mails are sent repeatedly a delay of 40 s is introduced to
        # compensate the restriction from the mail server
        sleep(40)

        # As before the conent of the mail is loaded from a file
        path = dataFolder + 'debtMail.t'
        with open(path, 'r') as mailFile:
            plainText = mailFile.read()

        # The parameters for the QR code generation are set up separately for ease of reading
        extraAmount = 0
        returnLink = True

        # A QR code and a MobilePay link is generated
        (path, mobilePayLink) = generateQR(user, extraAmount, returnLink)

        # The subject line of the mail is set
        msgRoot['Subject'] = 'Opgørelse af Æters Ølliste'

        # An HTML of the plain text is generated before substitutions
        htmlText = plainToHtml(plainText)

        # The plain text substitution is done. Some elements are merely comments in plain txt.
        # Valid substitutions are (so far): {name}, {sduId}, {qrcode}, {balance} and {link}
        plainTxt = plainTxt.format(name = user.name, sduId = user.sduId,
                                   qrcode = '(QR kode kan ikke vises)', balance = user.balance,
                                   link = '(Link virker ikke)')

        # The HTML substitution is done.
        # Valid substitutions are (so far): {name}, {sduId}, {qrcode}, {balance} and {link}
        htmlText = htmlText .format(name = user.name, sduId = user.sduId, balance = user.balance,
                                    qrcode = '<img src="cid:qrcode">',
                                    link = '<a href="' + mobilePayLink + '">link</a>')

        # The generated QR code is loaded into a MIMEImage intance
        with open(path, 'rb') as qrFile:
            msgImage = MIMEImage(qrFile.read())

        # A header used for identification in the HTML code is added to the picture,
        # and the picture is attached to the root message
        msgImage.add_header('Content-ID', '<qrcode>')
        msgRoot.attach(msgImage)

    # Everything is now common for the two mails again.
    # The plain/html text lines are converted to MIME text objects using utf8 encoding
    msgPlain = MIMEText(plainTxt.encode('utf-8'), 'plain', _charset = 'utf-8')
    msgHtml = MIMEText(htmlTxt.encode('utf-8'), 'html', _charset = 'utf-8')
    
    # As both a plain version and an HTML version will be attached we need
    # a multipart object of subtype 'alternative' to use both.
    # That object is then attached to the root message.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # The two MIME text objects are then attached to the alternative message.
    # Note that the preferred format must always be attached last!
    msgAlternative.attach(msgPlain)
    msgAlternative.attach(msgHtml)

    # A connection to the mail server is established, and authenticated
    # using the credentials loaded earlier.
    mailServer = smtplib.SMTP_SSL(smtpServer, 465)
    mailServer.esmtp_features['auth'] = 'LOGIN'
    mailServer.login(loginUserName, pwdMail)

    # If the mail is a password reset mail, only one try will be made at sending the mail
    if mailType == 'Pwd':
        try:
            mailServer.sendmail(sender, [user.mail], msgRoot.as_string())

            # If the mail is suceesfully sent, the password of the user is updated and saved and True is returned
            user.pwd = newPwdHash
            saveUser(user)
            mailServer.quit()
            return True
        except:
            
            # If the mail is not send False is returned
            mailServer.quit()
            return False

    # If the mailType is 'Debt', 3 tries will be made before returning False
    elif mailType == 'Debt':
        tryCounter = 0
        while True:
            try:
                if tryCounter == 3:

                    # If the send function fails thrice False is returned
                    mailServer.quit()
                    return False
                
                mailServer.sendmail(sender, [user.mail], msgRoot.as_string())
                mailServer.quit()

                # If the mail was succesfully sent True is returned
                return True
            except:
                tryCounter += 1
                sleep(10)    

# The usual header, which in this case just passes, as this script is not ment to be run at all.
def main():
    pass
if __name__ == '__main__':
    main()
