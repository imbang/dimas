# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 20:01:13 2013

@author: litbang
"""

import sys
import imaplib, email

#log in and select the inbox
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('imbang80', '1mb4ng12')
#print "email ",mail.list()
#sys.exit(1)

mail.select('INBOX')

#get uids of all messages
result, data = mail.uid('search', None, 'ALL') 
uids = data[0].split()

#read the lastest message
result, data = mail.uid('fetch', uids[-1], '(RFC822)')
#result, data = mail.uid('fetch', uids[-1], '(BODYSTRUCTURE)')
m = email.message_from_string(data[0][1])

print "email ",m
sys.exit(1)

if m.get_content_maintype() == 'multipart': #multipart messages only
    for part in m.walk():
        #find the attachment part
        if part.get_content_maintype() == 'multipart': continue
        if part.get('Content-Disposition') is None: continue

        #save the attachment in the program directory
        filename = part.get_filename()
        fp = open(filename, 'wb')
        fp.write(part.get_payload(decode=True))
        fp.close()
        print '%s saved!' % filename