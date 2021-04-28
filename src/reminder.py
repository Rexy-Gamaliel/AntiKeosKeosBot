import re
'''
Identifiers:
\d any number
\D anything but a number
\s space
\S anything but a space
\w any character
\W anything but a character
. = any character except for a newline
\b the whitespace around words
.\a period

Modifiers:
{1,3} we're expecting 1-3
+ match 1 or more
? match 0 or 1
* match 0 or more
$ match the end of a string
^ matching the beginning of a string
| either or
[] range or "variance"  [A-Za-z]
{x}  expecting "x" amount

White space characters:
\n newline
\s space
\t tab
\e escape
\f form feed
\r return

DON'T FORGET!
. + * ? [ ] $ ^ ( ) { } | \
'''

pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
pattern = "[\D]+[\d]+"
user_input = input('enter your email: ')
if (re.search(pattern, user_input)):
    print("valid email")
else:
    print("invalid email")

exampleString = '''
# Jessica is 15 years old, and Daniel is 27 years old.
# Edward is 97, and his grandfather, Oscar C is 102.
# '''
#
ages = re.findall(r'\d{1,3}', exampleString)
names = re.findall(r'[A-Z][a-z]+',exampleString)
print(ages)
print (names)

string1= 'ABh'
string2 ='abH'

comparison = string1.lower() == string2.lower()
print(comparison)