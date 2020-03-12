import smtplib, socket, sys, os, time
from random import randrange
import threading as t
import os

# these are the email addresses and their passwords 
# that the spam mail will be sent from.
# for Gmail accounts you must allow 3rd party app access
# in account settings.
emails = {"youremailhere@provider.domain":"youremailpassword",
          "emailherenumber2@provider.domain":"the password"}

print("Note that if you send too many emails from a single IP, the SMTP server may block your IP address.\n")

# input the arguments for main()
# also check that they are actually valid
# and won't throw an exception.

target = input("Target > ")

try:
    target.index("@")
except:
    print("E: Invalid target, Quitting...")
    exit()

name = input("Name of sender, default none > ")
subject = input("Subject, default none > ")

reps = input("Email count, default 50 > ")

if reps == "":
    reps = 50
try:
    reps = int(reps)
except:
    print("E: Invalid email count. Quitting...")
    exit()

emailCount = reps

threads = input("Thread count, default half of email count > ")
if threads == "":
    threads = reps / 2
try:
    threads = int(threads)
except:
    print("E: Invalid thread count. Quitting...")
    exit()

if threads > reps:
    print("E: Thread count cannot be larger than email count. Quitting...")
    exit()


print("{} emails will be sent to {} using {} threads at a time. Starting...".format(str(reps), str(target), str(threads)))


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
# count is the amount of times it has run main
count = 0
def main(from_name, sent_from, sent_from_pass, to_email, bdy_text, subject="", num=1, silent=0):
    global count
    global emails
    # set headers and body
    email_text = "From: {}\n".format(from_name)
    email_text += "To: {}\n".format(to_email)
    email_text += "Subject: {}\n\n".format(subject)
    email_text = email_text + bdy_text

    #print(email_text)

    try:
	# using the basic gmail smtp server, change this if you want
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sent_from, sent_from_pass)
        server.sendmail(sent_from, [to_email], email_text)
        server.close()
        if not silent:
            print('Email ' + str(count) + 'sent on try ' + str(num) + ' from ' + sent_from)
        count += 1
    except Exception as e:
        # try sending again after short sleep
        if num < 10:
            time.sleep(0.05)
            try:
                main(from_name, sent_from, sent_from_pass, to_email, bdy_text, subject, num+1)
            except:
                num+=1
        #if it has been trying for some time, print error
        else:
            if not silent:
                print("Failed to send from " + sent_from)
            main(name,
                 list(emails.keys())[emails.keys().index(sent_from)-1],
                 list(emails.values())[emails.keys().index(sent_from)-1],
                 target,
                 random_text(randrange(500, 1000)),
                 subject)

# Start main
# Parallelism - executes multiple instances of main()
# all at once.

if __name__ == "__main__":
    startTime = time.time()
    p = [None for i in range(threads)]
    if reps <= threads:
        for i in range(reps):
            p[i] = t.Thread(target=main,
                            args=[name,
                                  list(emails.keys())[reps % len(list(emails.keys()))],
                                  list(emails.values())[reps % len(list(emails.values()))],
                                  target,
                                  random_text(randrange(500, 1000)),
                                  subject])
            p[i].start()
            reps -= 1
        for i in range(reps):
            p[i].join()

    else:
        # replace threads for num
        for i in range(threads):
            p[i] = t.Thread(target=main,
                            args=[name,
                                  list(emails.keys())[reps % len(list(emails.keys()))],
                                  list(emails.values())[reps % len(list(emails.values()))],
                                  target,
                                  random_text(randrange(500, 1000)),
                                  subject])
            p[i].start()
            reps -= 1
        while True:
            # replace threads for num
            for i in range(threads):
                if p[i].is_alive() == False and reps > 0:
                    p[i] = t.Thread(target=main,
                                    args=[name,
                                          list(emails.keys())[reps % len(list(emails.keys()))],
                                          list(emails.values())[reps % len(list(emails.values()))],
                                          target,
                                          random_text(randrange(500, 1000)),
                                          subject])
                    p[i].start()
                    reps -= 1
                elif reps == 0:
                    break
            if reps <= 0:
                # replace threads for num
                for i in range(threads):
                    p[i].join()
                break

    totalTime = time.time() - startTime

    # print elapsed time and average speed.
    print("\nFinished in " + str(totalTime) + " seconds.")
    print("Average speed: " + str(emailCount / float(totalTime)) + " emails per second.")
