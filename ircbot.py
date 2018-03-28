import sys
import socket
import string

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "irc.root-me.org"
#channel = "#root-me_challenge"
channel = "##root-me_challenge"
botnick = "exaybachayBot"
adminname = "exaybachay"
exitcode = "bye " + botnick

ircsock.connect((server, 6667))
ircsock.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " " + botnick + "\n"))
ircsock.send(bytes("NICK " + botnick + "\n"))

def joinchan(chan):
	ircsock.send(bytes("JOIN "+ chan + "\n"))
	ircmsg = ""
	while ircmsg.find("End of /NAMES list.") == -1:
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		ircmsg = ircmsg.strip('\n\r')
		print(ircmsg.encode("UTF-8"))

def ping():
	ircsock.send(bytes("PONG :pingis\n"))

def sendmsg(msg, target=channel):
	ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n"))

def main():
	joinchan(channel)
	while 1:
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		ircmsg = ircmsg.strip('\n\r')
		print(ircmsg)

		if ircmsg.find("PRIVMSG") != -1:
			name = ircmsg.split('!',1)[0][1:]
			message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

			if len(name) < 17:
				if message.find('Hi ' + botnick) != -1:
					sendmsg("Hello " + name + "!")
				if message[:5].find('.tell') != -1:
					target = message.split(' ', 1)[1]
					if target.find(' ') != -1:
						message = target.split(' ', 1)[1]
						target = target.split(' ')[0]
					else:
						target = name
						message = "Could not parse.  The message should be in the format of .tell target message to work properly."
					sendmsg(message, target)
			if name.lower() == adminname.lower() and message.rstrip() == exitcode:
				sendmsg("quitting time. :'(")
				ircsock.send(bytes("QUIT \n"))
				return
		else:
			if ircmsg.find("PING :") != -1:
				ping()

main()
