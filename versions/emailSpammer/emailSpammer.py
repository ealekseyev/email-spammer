import smtplib, socket, json, sys, os
from random import randrange
import threading as mp
from time import sleep

# use base spammer/spoofer unless there is a 5th argv present
sent_from = 'sceet421@gmail.com'
sent_from_pass = list('NULLLL') #os.popen("cat pass.txt").read()
try:
    x = sys.argv[5]
    sent_from = 'arandomperson4206969@gmail.com'
    sent_from_pass = list('NULLLL') #os.popen("cat pass.txt").read()
except: pass

# header info
to_emails = [str(sys.argv[1])]
subject = str(sys.argv[3])
from_name = sys.argv[2]

# amount of threads to launch at a time
threads = 50

# generate empty list (for thread array)
def returnNone(lenlist):
	obj = []
	for i in range(lenlist):
		obj.append(None)
	return obj

# format header
def set_email_text(body):
	e = "From: {}\n".format(from_name)
	e += "To: {}\n".format(", ".join(to_emails))
	e += "Subject: {}\n\n".format(subject)
	e = e + body
	return e

# generate random amount of text of iter length
def random_text(iter):
	bdy = ''
	for i in range(iter):
		char = str(chr(randrange(33, 126)))
		if char != '.':
			bdy += char
		else: 
			bdy += 'k'
	return bdy

# sends email and executes all dependencies
# num is the amount of times it has had to execute
def main(num=1):
	email_text = set_email_text(random_text(randrange(500, 1000)))

	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(sent_from, sent_from_pass)
		server.sendmail(sent_from, to_emails, email_text)
		server.close()
		print('Email ' + str(repsLeft) + ' Sent on try ' + str(num))
	except Exception as e:
		# try sending again after short sleep
		if num < 20:
			sleep(0.05)
			main(num+1)
		# if it has been trying for some time, print error
		else:
			print(e)

reps = int(sys.argv[4])
repsLeft = reps
p = returnNone(threads)

for i in range(len(sent_from_pass)):
	sent_from_pass[i] = chr(ord(sent_from_pass[i])-1)
sent_from_pass = "".join(sent_from_pass)

print(sent_from + " > " + ", ".join(to_emails))

#replace threads for num
if reps <= threads:
	for i in range(reps):
		p[i] = mp.Thread(target=main)
		p[i].start()
	for i in range(reps):
		p[i].join()

else:
	#replace threads for num
	for i in range(threads):
		p[i] = mp.Thread(target=main)
		p[i].start()
		repsLeft -= 1
	while True:
		#replace threads for num
		for i in range(threads):
			if p[i].is_alive() == False and repsLeft > 0:
				p[i] = mp.Thread(target=main)
				p[i].start()
				repsLeft -= 1
			elif repsLeft == 0:
				break
		if repsLeft <= 0:
			#replace threads for num
			print("Waiting for all threads to finish", end="")
			for i in range(threads):
				p[i].join()
				print(".", end="")
			break

print("\ndone")
