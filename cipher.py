pas = ''
try: pas = input("pass to cipher: ")
except: pas = raw_input("pass to cipher: ")

passs = ''

for i in range(len(pas)):
	passs += chr(ord(pas[i])+1)
print(passs)
