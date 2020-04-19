import smtplib, socket, sys, os, time
from random import randrange
import threading as t
import os

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

from randomsent import rand_sentence, rand_name

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

# these are the email addresses and their encrypted passwords
# that the spam mail will be sent from.
# for Gmail accounts you must allow 3rd party app access
# in account settings.
#value to test encryption. Once decrypted correctly, the value should be equal to "test_enc"
test_enc = "dCvQ79ib8td3qXTkXbQjM/95GFIazp/ShXbw4cuL1O0="
emails_enc = {"anotherspamemail513@gmail.com":"CB3YDiia4b3kGRFqCRaR9Ex/DrTfhYdAFUhnE3qTrJU=",
          "anotherspamemail514@gmail.com":"5mNWK1kMcxtBY0QGGCwZS6YHuFzMW0udU12ud7tTEcc=",
          "no426191@gmail.com":"rg2PoaT4djf+9s9sO9jqJPjbgtKOKadkQkJ9CmXoYTo=",
          "uu3810816@gmail.com":"SuA2LS0ZZrzIlj92BYfAnXACPFfzIlgUX3OWqxIlQeA=",
          "ms7001912@gmail.com":"txMGGI1O62FtNtF1D/KYtbLLuiZ+hVNmkHtnZ60CP0E=",
          "jd2390529@gmail.com":"pZSnPDMKyGJsWgon5kbmMaLtrR0S1rLhfpmqV6NpGgY=",
          "sd3239465@gmail.com":"puER54Ar9vObmkM1WR/xhlKo2aj8Iuc7aajbbWkNRKs=",
          "jb1286815@gmail.com":"keaw3sgjKecSgE9FRSsWLuZEPPy+3PI+pCjJ7LGKw2g="}

emails = {}

print("Note that if you send too many emails from a single IP, the SMTP server may block your IP address.\n")

# input the arguments for main()
# also check that they are actually valid
# and won't throw an exception.

decryption_key = input("Password decryption key > ")

if decrypt(test_enc, decryption_key).decode("utf-8") == "test_enc":
    print("Verified decryption key, decrypting passwords...")
else:
    print("E: Incorrect decryption key")
    quit()

for key, value in emails_enc.items():
    try:
        dec = decrypt(value, decryption_key).decode("utf-8")
    except:
        print("E: Incorrect decryption key")
        quit()
    emails.update( {key: dec} )

# target address
target = input("Target > ")

try:
    target.index("@")
except:
    print("E: Invalid target, Quitting...")
    exit()

# sender name
name = input("Name of sender, default random > ")
if name.replace(" ", "") == "":
	name = "__RAND__"

# subject of emails
subject = input("Subject, default none > ")

# email count
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
    """
    bdy = ''
    for i in range(iter):
        char = str(chr(randrange(33, 126)))
        if char != '.':
            bdy += char
        else:
            bdy += 'k'
    return bdy
    """
    return rand_sentence()

# sends email and executes all dependencies
# count is the amount of times it has run main
count = 0

def main(from_name, sent_from, sent_from_pass, to_email, bdy_text, subject="", num=1, silent=0):
    global count
    global emails
    # set headers and body
    if from_name == "__RAND__":
        email_text = "From: {}\n".format(rand_name())
    else:
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
            print('Email ' + str(count) + ' sent on try ' + str(num) + ' from ' + sent_from)
        count += 1
    except Exception as e:
        # try sending again after short sleep
        if num < 15:
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
