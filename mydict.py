#! /usr/bin/python3


# import modules
import json
import spellchecker
from colorama import Fore,Style


# create spell checker object
spell=spellchecker.SpellChecker()


# use json library and methods to load data from text file
dictData = json.load(open("dictdata.json"))


def getDef(yourWord):
    """Search word definition(s) in data file.

    Arguments:
      yourWord: word to search for
    """
    if yourWord in dictData.keys():
        myDef=dictData.get(yourWord)
    elif yourWord.lower() in dictData.keys():
        yourWord=yourWord.lower()
        myDef=dictData.get(yourWord)
    else:
        myDef=[]
    return(myDef)


def printDef():
    """Display result of definition search.

    Arguments:
      myDef: list containing definition result
    """
    print(f"Searching for word \"%s\"..." % (yourWord))
    myDef=getDef(yourWord)
    if len(myDef)==0:
        print("Sorry, I could not find your word.")
    else:
        i=0
        for i in range(0,len(myDef)):
            print("%2d: %s" % (i+1,myDef[i]))
            i+=1
    return()


yourWord = input("What word are you looking for? ")
if yourWord.isalpha():
    # word is all alpha and not empty string
    if yourWord in spell:
        # word is spelled correctly, get the definition
        printDef()
    else:
        # word showed up as misspelled. Get a suggested spelling and verify
        tryWord = spell.correction(yourWord)
        tryAgain=input("Your word might be misspelled. Did you mean to type \"%s\"? (Y or N) " % (tryWord))
        if tryAgain in "Yy":
            # Use the suggested spelling
            print("Ok, I'll try that.")
            yourWord=tryWord
            printDef()
        else:
            # does user wants to stick with their spelling?
            youSure=input("So search for \"%s\"? (Y or N) " % (yourWord))
            if youSure in "Yy":
                printDef()
            else:
                print("Please try again with a different word.")
else:
    print("Please enter a word.")

