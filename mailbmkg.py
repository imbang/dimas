# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 18:42:09 2013

@author: litbang
"""

import sys

from twisted.internet import protocol, defer, endpoints, task
from twisted.mail import imap4
from twisted.python import failure

@defer.inlineCallbacks
def main(reactor, username="bayu.imbang@bmkg.go.id", password="1mb4ng12",
         strport="ssl:host=mail.bmkg.go.id:port=993"):
    endpoint = endpoints.clientFromString(reactor, strport)
    factory = protocol.Factory()
    factory.protocol = imap4.IMAP4Client
    try:
        client = yield endpoint.connect(factory)
        yield client.login(username, password)
        yield client.select('INBOX')
        info = yield client.fetchEnvelope(imap4.MessageSet(2))
        print 'First message subject:', info[2]['ENVELOPE'][1]
        #print info
    except:
        print "IMAP4 client interaction failed"
        failure.Failure().printTraceback()

# This API requires Twisted 12.3 or later, or a trunk checkout:
task.react(main, sys.argv[1:])