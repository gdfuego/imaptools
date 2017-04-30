#!/usr/bin/env python

import email
import getpass, imaplib
import re
import os
import sys
from tqdm import tqdm

list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

detach_dir = '.'
if 'downloads' not in os.listdir(detach_dir):
    os.mkdir('downloads')

userName = raw_input('Enter your AOL username:')
passwd = getpass.getpass('Enter your password: ')

imapSession = imaplib.IMAP4_SSL('imap.aol.com')
typ, accountDetails = imapSession.login(userName, passwd)
if typ != 'OK':
    print 'Not able to sign in!'
    raise

typ, folders = imapSession.list()
if typ != 'OK':
    print 'Not able to get a list of folders'
    raise

for folder in folders:
    folder = parse_list_response(folder)[2]
    print 'Processing %s' % folder
    imapSession.select(folder, 'readonly')
    typ, data = imapSession.search(None, 'ALL')
    if typ != 'OK':
        print 'Error searching Inbox.'
        raise

    # Iterating over all emails
    for msgId in tqdm(data[0].split()):
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print 'Error fetching mail.'
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_string(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(detach_dir, 'downloads', fileName)
                if not os.path.isfile(filePath) :
                    print fileName
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
imapSession.close()
imapSession.logout()

