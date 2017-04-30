#!/usr/bin/env python

"""Simplified IMAP function for my needs"""

import re
import imaplib

LISTPARSE = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def parse_list_response(line):
    """Process the output of an IMAP list command"""
    flags, delimiter, mailbox_name = LISTPARSE.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

class Ayemappy(object):
    """Simplified wrapper on imap"""

    def __init__(self):
        """Setup connection"""
        self.session = None
        self.server = None
        self.user = None
        self.folders = []

    def connect(self, server, user, password):
        """Connect to the specified server with the supplied username and password"""
        self.server = server
        self.user = user
        self.session = imaplib.IMAP4_SSL(self.server)
        typ, accountdetails = self.session.login(self.user, password)
        if typ != 'OK':
            print 'Not able to sign in!'

    def listfolders(self):
        """Obtain a list of folders"""
        self.folders = []
        typ, folders = self.session.list()
        if typ != 'OK':
            print 'Not able to get a list of folders'
        for folder in folders:
            self.folders.append(parse_list_response(folder)[2])
        return self.folders

    def listmessages(self, folder):
        """Get a list of message IDs for a given folder"""
        self.session.select(folder, 'readonly')
        typ, data = self.session.search(None, 'ALL')
        if typ != 'OK':
            print 'Error searching Inbox.'
        return data[0].split()

    def disconnect(self):
        """Disconnect from the IMAP server"""
        self.session.close()
        self.session.logout()
