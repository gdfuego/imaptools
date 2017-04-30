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

class ayemappy:
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
        typ, data = self.Session.search(None, 'ALL')
        if typ != 'OK':
            print 'Error searching Inbox.'
            raise
        return data[0].split()

    def disconnect(self):
        self.Session.close()
        self.Session.logout()

def main():
    pass

if __name__ == '__main__':
    main()
