import time, os, email, subprocess
import smtplib
import imaplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from time import sleep

class EmailBEE():

    def checkMail(self):
        m = imaplib.IMAP4_SSL('imap.gmail.com')
        m.login("kindlemusicplayer@gmail.com", "ENTER PASSWORD")
        m.select('INBOX')
        rep, emailNums = m.search(None, "(FROM bhuvan.belur@gmail.com)")
        emailNums = emailNums[0].split()
        emailTexts = []
        for EId in emailNums:
            textList = []
            rep, emailData = m.fetch(EId, '(RFC822)')
            m.store(EId, '+FLAGS', '\\Deleted')
            m.expunge()
            realData = emailData[0][1]
            decodedData = realData.decode('utf-8')
            emailMessage = email.message_from_string(decodedData)

            for part in emailMessage.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    for char in body.decode('utf-8'):
                        textList.append(char)
                    del textList[-2:]
                    finalMessage = ''.join(textList)
                    emailTexts.append(finalMessage)
                    return(finalMessage, emailMessage)
        return ("", "")

    def save_attachment(self, msg, download_folder=None):
        if download_folder == None:
            download_folder = os.getcwd()
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path