str = input("String to enlarge: ")
iter = int(input("amount of whitespace between characters: "))
final = ''

for i in str:
    final += i
    for j in range(iter):
        final += chr(0x200E)

print(final)
print(len(final))