#!/usr/bin/env python

import email
import re
import os
import sys
from tqdm import tqdm
import imaplib

list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

class ayemap:
    """Simplified wrapper on imap"""

    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.Session = None
        self.folders = []
	self.connect()

    def connect(self):
        self.Session = imaplib.IMAP4_SSL(self.server)
        typ, accountDetails = self.Session.login(self.user, self.password)
        if typ != 'OK':
            print 'Not able to sign in!'
            raise

    def listfolders(self):
        self.folders = []
	typ, folders = self.Session.list()
	if typ != 'OK':
	    print 'Not able to get a list of folders'
	    raise
	for folder in folders:
	    self.folders.append(parse_list_response(folder)[2])
	return self.folders

    def listmessages(self, folder):
        self.Session.select(folder, 'readonly')
        typ, data = imapSession.search(None, 'ALL')
        if typ != 'OK':
            print 'Error searching Inbox.'
            raise

    def disconnect(self):
        self.Session.close()
        self.Session.logout()



def main():
    import getpass

    detach_dir = '.'
    if 'downloads' not in os.listdir(detach_dir):
	os.mkdir('downloads')

    userName = raw_input('Enter your AOL username:')
    passwd = getpass.getpass('Enter your password: ')


    for folder in folders:
	print 'Processing %s' % folder

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

if __name__ == '__main__':
    main()
