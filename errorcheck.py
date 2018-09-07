#! /usr/bin/python3


# import modules
from subprocess import check_call,Popen,PIPE
from copy import deepcopy
from colorama import Fore,Style
import sys,os,stat,time


# Set up global vars and make log directory if needed
testChoice = ""
if not os.path.isdir("/tmp/errorcheck"):
    os.mkdir("/tmp/errorcheck")
checkList=[]


# Work on autobuilding the list of checks from a supplied data file
def buildCheckList():
    """Build list checkList from external data file. List contains check name, command, and help text.

    Arguments:
      None
    """
    global checkList
    fileObj=open("errorcheck.dat")
    fileObjList=fileObj.readlines()
    i=0
    # Build list
    while i<len(fileObjList):
        checkList.append(fileObjList[i].split("^"))
        checkList[i][3]=checkList[i][3].split("&")
        i+=1
    fileObj.close()
    # print list to verify
#    i=0
#    while i<len(checkList):
#        print("Record " + str(i) + " Field 0: " + checkList[i][0])
#        print("Record " + str(i) + " Field 1: " + checkList[i][1])
#        print("Record " + str(i) + " Field 2: " + checkList[i][2])
#        k=0
#        while k<len(checkList[i][3]):
#           print(checkList[i][3][k])
#           k+=1
#        i+=1
    return()


def print_Separator(separator,fgColor="WHITE"):
    """Print a blank line followed by a separator line, for easier reading.

    Arguments:
      separator: character to use to build separator line
      fgColor  : color of separator line. Default is WHITE
    """
    print("\n")
    if fgColor=="RED":
        print(f"{Fore.RED}%-60s{Style.RESET_ALL}" % (separator*60))
    elif fgColor=="BLUE":
        print(f"{Fore.BLUE}%-60s{Style.RESET_ALL}" % (separator*60))
    elif fgColor=="GREEN":
        print(f"{Fore.GREEN}%-60s{Style.RESET_ALL}" % (separator*60))
    elif fgColor=="YELLOW":
        print(f"{Fore.YELLOW}%-60s{Style.RESET_ALL}" % (separator*60))
    else:
        print(separator*60)
    return()


def print_Menu():
    """Print options menu

    Arguments:
      None
    """
    global checkList
    print_Separator("=","YELLOW")
    i=0
    optionChar="A"
    print("The tests you can run are:")
    while i < len(checkList):
        print(f"%2s: %s" % (optionChar, checkList[i][0]))
        i+=1
        optionChar=chr(ord(optionChar)+1)
    # Continue with menu options and info not in data file/check list
    print("""
 V: View logs
 Z: Run all tests
 Q: Quit

You can choose one or more tests to run together as background tasks. Enter your options on one line,
no spaces or separators between test choices. Select background tests with capital letters (A-K).

You can run tests live one at a time. Choose live tests with lower-case letters (a-k).

    """)
    return()


def valid_Choice(testChoice):
    """Make sure that a valid menu option was chosen

    Arguments:
      testChoice: selected menu option(s)
    """
    validChoice = True
    i = 0
    while i < len(testChoice):
        if testChoice[i].isdigit():
            validChoice = False
        if len(testChoice) > 1 and "Q" in testChoice.upper():
            validChoice = False
        if testChoice[i-1].upper() not in "ABCDEFGHIJKQVZ":
            validChoice = False
        i+=1
    return(validChoice)


def run_Check(choice, check, command, wait=2):
    try:
      if choice in "ABCDEFGHIJKZ":
          # Run checks in background and log STDOUT and STDERR to files
          outfile = "/tmp/errorcheck/" + check + "_out.txt"
          errfile = "/tmp/errorcheck/" + check + "_err.txt"
          fout = open(outfile,'w')
          ferr = open(errfile,'w')
          fout.write("Command: " + command + "\n")
          print("Checking " + check + ". Please wait about " + str(wait) + " seconds.")
          process=Popen(command, shell=True, stdout=fout, stderr=ferr)
          fout.close
          ferr.close
      elif choice in "abcdefghijkz":
          # Run checks in foreground. No need to log output
          print_Separator("=","BLUE")
          print(f"{Fore.BLUE+Style.BRIGHT}Running check \"%s\"{Style.RESET_ALL}" % (command))
          process=Popen(command, shell=True)
          process.wait()
    except IOError as e:
      sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
    except OSError as e:
      sys.exit("failed to run shell: %s" % (str(e)))
    except Exception as e:
      sys.exit("An error occured: %s" % (str(e)))
    return()


def view_Logs():
    logList=[]
    os.chdir("/tmp/errorcheck/")
    logList=os.listdir("/tmp/errorcheck/")
    fileData=[]
    i=0
    while i < len(logList):
        logFile=os.path.join("/tmp/errorcheck",logList[i])
        logData=(logList[i],time.ctime(os.path.getmtime(logFile)))
        logList[i]=logData
        i+=1
    printLog=""
    print_Separator("+","BLUE")
    while printLog.upper() != "Q":
        i=1
        for logFile in logList:
            print("%3d: %-18s created on %-30s" % (i,logFile[0],logFile[1]))
            i+=1
        print("  Q: Quit and return to main menu")
        print("")
        printLog = input("Which log would you like see? ")
        if printLog.isdigit():
            print_Separator("+","BLUE")
            logFile=logList[int(printLog)-1][0]
            print(f"{Fore.GREEN+Style.BRIGHT}Printing logfile %-30s{Style.RESET_ALL}" % (logFile))
            fileObj=open(logFile,'r')
            x=fileObj.readlines()
            j=0
            while j in range(0,len(x)-1):
                printLine=x[j].strip()
                print(printLine)
                j+=1
            print_Separator("+","BLUE")
    return()


buildCheckList()
while testChoice.upper() != "Q":
    print_Menu()
    testChoice = input("What test(s) would you like to run: ")
    if valid_Choice(testChoice):
        i = 0
        while i < len(testChoice):
            if testChoice[i].upper() in "AZ":
                run_Check(testChoice[i],"free_mem", "free -m")
            if testChoice[i].upper() in "BZ":
                run_Check(testChoice[i],"dmesg", "dmesg | tail")
            if testChoice[i].upper() in "CZ":
                run_Check(testChoice[i],"iostat", "iostat -txz 5 5", 25)
            if testChoice[i].upper() in "DZ":
                run_Check(testChoice[i],"vmstat", "vmstat -t 2 5", 10)
            if testChoice[i].upper() in "EZ":
                run_Check(testChoice[i],"mpstat", "mpstat -P ALL 2 5", 10)
            if testChoice[i].upper() in "FZ":
                run_Check(testChoice[i],"top_CPU", "top -n 1 -o %CPU -b")
            if testChoice[i].upper() in "GZ":
                run_Check(testChoice[i],"top_MEM", "top -n 1 -o %MEM -b")
            if testChoice[i].upper() in "HZ":
                run_Check(testChoice[i],"sar_dev", "sar -n DEV 1 5")
            if testChoice[i].upper() in "IZ":
                run_Check(testChoice[i],"sar_tcp", "sar -n TCP,ETCP 1 5")
            if testChoice[i].upper() in "JZ":
                run_Check(testChoice[i],"pidstat", "pidstat 1 5")
            if testChoice[i].upper() in "KZ":
                run_Check(testChoice[i],"uptime", "uptime")
            if testChoice[i].upper() in "V":
                view_Logs()
            if testChoice[i].upper() in "Q":
                break
            i+=1
    else:
        print("Please choose from the options provided in the menu.")
print("Done.")

#
# Info about these checks can be found at https://medium.com/netflix-techblog/linux-performance-analysis-in-60-000-milliseconds-accc10403c55
# See more checks at https://medium.com/netflix-techblog/netflix-at-velocity-2015-linux-performance-tools-51964ddb81cf
#
