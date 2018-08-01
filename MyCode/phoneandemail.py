#! python3

# Read in text containing phone numbers and email addresses from clipboard, pull out only the phone numbers
# and emails, and paste them back to the clipboard

import pyperclip
import re

phoneRegex = re.compile(r'''
(
((\d\d\d)|(\(\d\d\d\)))?      # area code (optional)
(\s|-)                         # separator (space or dash)
\d\d\d                         # exchange
-                              # separator
\d\d\d\d                       # last four digitd
(((ext(\.)?\s)|x) (\d{2,5}))?   # optional extension
)
''', re.VERBOSE)

emailRegex = re.compile(r'''
[a-zA-Z0-9_.+]+            # name
@                          # @
[a-zA-Z0-9_.+]+            # domain name
''', re.VERBOSE)

def copyIn():
    #Get data from clipboard
    incomingText=pyperclip.paste()
    return incomingText

def pasteOut(textToCopyToClipboard):
    # Copy data to the clipboard
    outGoingText=pyperclip.copy(textToCopyToClipboard)
    return outGoingText

getText=copyIn()
getPhone=phoneRegex.findall(getText)
getEmail=emailRegex.findall(getText)

# since the findall method returns a list of tuples, we want only the first item in the tuple. Go through the
# list of returned phone numbers and only take the first item in the tuple
phoneList=[]
for phoneNumber in getPhone:
    phoneList.append(phoneNumber[0])

#print(phoneList)
#print(getEmail)

# put each phone number and email on own line and combine to make one large output
textToCopyToClipboard = '\n'.join(phoneList) + '\n' + '\n'.join(getEmail)
copyToClipboard = pasteOut(textToCopyToClipboard)


