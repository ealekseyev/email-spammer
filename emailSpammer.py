from urllib.request import urlopen
import smtplib, socket, json, sys, os
from random import randrange
import threading as mp
from time import sleep

sent_from = 'sceet421@gmail.com'
sent_from_pass = list('fwbodppm') #os.popen("cat pass.txt").read()
try:
    x = sys.argv[5]
    sent_from = 'arandomperson4206969@gmail.com'
    sent_from_pass = list('jepoufwfolopx21') #os.popen("cat pass.txt").read()
except: pass
to_emails = [str(sys.argv[1])]
subject = str(sys.argv[3])
from_name = sys.argv[2]

def set_email_text(body):
	e = "From: {}\n".format(from_name)
	e += "To: {}\n".format(", ".join(to_emails))
	e += "Subject: {}\n\n".format(subject)
	e = e + body
	return e

def random_text(min, max):
	bdy = ''
	for i in range(randrange(min, max)):
		char = str(chr(randrange(33, 126)))
		if char != '.':
			bdy += char
		else: 
			bdy += 'k'
	return bdy

def main():
	email_text = set_email_text(random_text(500, 1000))

	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(sent_from, sent_from_pass)
		server.sendmail(sent_from, to_emails, email_text)
		server.close()
		print('Email Sent')
	except Exception as e:
		print(e)
		sleep(0.2)
		main()

reps = int(sys.argv[4])
repsLeft = reps
p = [None, None, None, None, None, None, None, None, None, None]

for i in range(len(sent_from_pass)):
	sent_from_pass[i] = chr(ord(sent_from_pass[i])-1)

sent_from_pass = "".join(sent_from_pass)

print("Starting with " + sent_from)

if reps <= 10:
	for i in range(reps):
		p[i] = mp.Thread(target=main)
		p[i].start()
	for i in range(reps):
		p[i].join()
else:
	for i in range(10):
		p[i] = mp.Thread(target=main)
		p[i].start()
		repsLeft -= 1
	while True:
		for i in range(10):
			if p[i].is_alive() == False and repsLeft > 0:
				p[i] = mp.Thread(target=main)
				p[i].start()
				repsLeft -= 1
			elif repsLeft == 0:
				break
		if repsLeft <= 0:
			break

for i in range(10):
	p[i].join()

print("done")