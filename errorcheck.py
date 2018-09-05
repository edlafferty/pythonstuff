#! /usr/bin/python3


# import modules
from subprocess import check_call,Popen,PIPE
from copy import deepcopy
import sys,os,stat,time


# Set up global vars and make log directory if needed
testChoice = ""
if not os.path.isdir("/tmp/errorcheck"):
    os.mkdir("/tmp/errorcheck")


def print_Menu():
    """Print options menu

    Arguments:
      None
    """
    print("""
===============================================================================================
The tests you can run are:
A: Free memory
B: dmesg
C: IOStat
D: VMStat
E: MPStat
F: Top (sorted by CPU)
G: Top (sorted by MEM)
H: Sar (devices)
I: Sar (TCP)
J: Uptime
K: PIDStat
V: View logs
Z: Run all tests
Q: Quit

You can choose one or more tests to run together as background tasks. Enter your options on one line,
no spaces or separators between test choices. Select background tests with capital letters (A-K).

You can run tests live one at a time. Choose live tests with lower-case letters (a-k).

    """)


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
        i=+1
    return(validChoice)


def run_Check(choice, check, command, wait=2):
  outfile = check + "/tmp/errorcheck/out.txt"
  errfile = check + "/tmp/errorcheck/err.txt"
  try:
    if choice in "ABCDEFGHIJK":
        fout = open(outfile,'w')
        ferr = open(errfile,'w')
        print("Checking " + check + ". Please wait about " + str(wait) + " seconds.")
        process=Popen(command, shell=True, stdout=fout, stderr=ferr)
        fout.close
        ferr.close
    elif choice in "abcdefghijk":
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
        logData=(logList[i],time.ctime(os.path.getctime(logFile)))
        logList[i]=logData
        i=i+1
    printLog=""
    while printLog.upper() != "Q":
        i=1
        for logFile in logList:
            print("%3d: %12s created on %30s" % (i,logFile[0],logFile[1]))
            i=i+1
        print("  Q: Quit and return to main menu")
        print("")
        printLog = input("Which log would you like see? ")
        if printLog.isdigit():
            logFile=logList[int(printLog)-1][0]
            fileObj=open(logFile,'r')
            x=fileObj.readlines()
            j=0
            while j in range(0,len(x)-1):
                print(x[j])
                j=j+1
    return()



while testChoice.upper() != "Q":
    print_Menu()
    testChoice = input("What test(s) would you like to run: ")
    if valid_Choice(testChoice):
        i = 0
        while i < len(testChoice):
            if testChoice[i].upper() in "AZ":
                run_Check(testChoice[i],"free_mem", "free -m")
                """The right two columns show:
buffers: For the buffer cache, used for block device I/O.
cached: For the page cache, used by file systems.
We just want to check that these aren’t near-zero in size, which can lead to higher disk I/O (confirm using iostat), and worse performance. The above example looks fine, with many Mbytes in each.
The “-/+ buffers/cache” provides less confusing values for used and free memory. Linux uses free memory for the caches, but can reclaim it quickly if applications need it. So in a way the cached memory should be included in the free memory column, which this line does. There’s even a website, linuxatemyram, about this confusion.
It can be additionally confusing if ZFS on Linux is used, as we do for some services, as ZFS has its own file system cache that isn’t reflected properly by the free -m columns. It can appear that the system is low on free memory, when that memory is in fact available for use from the ZFS cache as needed."""
            if testChoice[i].upper() in "BZ":
                run_Check(testChoice[i],"dmesg", "dmesg | tail")
                """This views the last 10 system messages, if there are any. Look for errors that can cause performance issues. The example above includes the oom-killer, and TCP dropping a request."""
            if testChoice[i].upper() in "CZ":
                run_Check(testChoice[i],"iostat", "iostat -txz 5 5", 25)
                """This is a great tool for understanding block devices (disks), both the workload applied and the resulting performance. Look for:
r/s, w/s, rkB/s, wkB/s: These are the delivered reads, writes, read Kbytes, and write Kbytes per second to the device. Use these for workload characterization. A performance problem may simply be due to an excessive load applied.
await: The average time for the I/O in milliseconds. This is the time that the application suffers, as it includes both time queued and time being serviced. Larger than expected average times can be an indicator of device saturation, or device problems.
avgqu-sz: The average number of requests issued to the device. Values greater than 1 can be evidence of saturation (although devices can typically operate on requests in parallel, especially virtual devices which front multiple back-end disks.)
%util: Device utilization. This is really a busy percent, showing the time each second that the device was doing work. Values greater than 60% typically lead to poor performance (which should be seen in await), although it depends on the device. Values close to 100% usually indicate saturation.
If the storage device is a logical disk device fronting many back-end disks, then 100% utilization may just mean that some I/O is being processed 100% of the time, however, the back-end disks may be far from saturated, and may be able to handle much more work.
Bear in mind that poor performing disk I/O isn’t necessarily an application issue. Many techniques are typically used to perform I/O asynchronously, so that the application doesn’t block and suffer the latency directly (e.g., read-ahead for reads, and buffering for writes)."""
            if testChoice[i].upper() in "DZ":
                run_Check(testChoice[i],"vmstat", "vmstat -t 2 5", 10)
                """Short for virtual memory stat, vmstat(8) is a commonly available tool (first created for BSD decades ago). It prints a summary of key server statistics on each line.
vmstat was run with an argument of 1, to print one second summaries. The first line of output (in this version of vmstat) has some columns that show the average since boot, instead of the previous second. For now, skip the first line, unless you want to learn and remember which column is which.
Columns to check:
r: Number of processes running on CPU and waiting for a turn. This provides a better signal than load averages for determining CPU saturation, as it does not include I/O. To interpret: an “r” value greater than the CPU count is saturation.
free: Free memory in kilobytes. If there are too many digits to count, you have enough free memory. The “free -m” command, included as command 7, better explains the state of free memory.
si, so: Swap-ins and swap-outs. If these are non-zero, you’re out of memory.
us, sy, id, wa, st: These are breakdowns of CPU time, on average across all CPUs. They are user time, system time (kernel), idle, wait I/O, and stolen time (by other guests, or with Xen, the guest’s own isolated driver domain).
The CPU time breakdowns will confirm if the CPUs are busy, by adding user + system time. A constant degree of wait I/O points to a disk bottleneck; this is where the CPUs are idle, because tasks are blocked waiting for pending disk I/O. You can treat wait I/O as another form of CPU idle, one that gives a clue as to why they are idle.
System time is necessary for I/O processing. A high system time average, over 20%, can be interesting to explore further: perhaps the kernel is processing the I/O inefficiently.
In the above example, CPU time is almost entirely in user-level, pointing to application level usage instead. The CPUs are also well over 90% utilized on average. This isn’t necessarily a problem; check for the degree of saturation using the “r” column."""
            if testChoice[i].upper() in "EZ":
                run_Check(testChoice[i],"mpstat", "mpstat -P ALL 2 5", 10)
                """This command prints CPU time breakdowns per CPU, which can be used to check for an imbalance. A single hot CPU can be evidence of a single-threaded application."""
            if testChoice[i].upper() in "FZ":
                run_Check(testChoice[i],"top_CPU", "top -n 1 -o %CPU -b")
                """The top command includes many of the metrics we checked earlier. It can be handy to run it to see if anything looks wildly different from the earlier commands, which would indicate that load is variable.
A downside to top is that it is harder to see patterns over time, which may be more clear in tools like vmstat and pidstat, which provide rolling output. Evidence of intermittent issues can also be lost if you don’t pause the output quick enough (Ctrl-S to pause, Ctrl-Q to continue), and the screen clears."""
            if testChoice[i].upper() in "GZ":
                run_Check(testChoice[i],"top_MEM", "top -n 1 -o %MEM -b")
            if testChoice[i].upper() in "HZ":
                run_Check(testChoice[i],"sar_dev", "sar -n DEV 1 5")
                """Use this tool to check network interface throughput: rxkB/s and txkB/s, as a measure of workload, and also to check if any limit has been reached. In the above example, eth0 receive is reaching 22 Mbytes/s, which is 176 Mbits/sec (well under, say, a 1 Gbit/sec limit).
This version also has %ifutil for device utilization (max of both directions for full duplex), which is something we also use Brendan’s nicstat tool to measure. And like with nicstat, this is hard to get right, and seems to not be working in this example (0.00)."""
            if testChoice[i].upper() in "IZ":
                run_Check(testChoice[i],"sar_tcp", "sar -n TCP,ETCP 1 5")
                """This is a summarized view of some key TCP metrics. These include:
active/s: Number of locally-initiated TCP connections per second (e.g., via connect()).
passive/s: Number of remotely-initiated TCP connections per second (e.g., via accept()).
retrans/s: Number of TCP retransmits per second.
The active and passive counts are often useful as a rough measure of server load: number of new accepted connections (passive), and number of downstream connections (active). It might help to think of active as outbound, and passive as inbound, but this isn’t strictly true (e.g., consider a localhost to localhost connection).
Retransmits are a sign of a network or server issue; it may be an unreliable network (e.g., the public Internet), or it may be due a server being overloaded and dropping packets. The example above shows just one new TCP connection per-second."""
            if testChoice[i].upper() in "JZ":
                run_Check(testChoice[i],"pidstat", "pidstat 1 5")
                """Pidstat is a little like top’s per-process summary, but prints a rolling summary instead of clearing the screen. This can be useful for watching patterns over time, and also recording what you saw (copy-n-paste) into a record of your investigation."""
            if testChoice[i].upper() in "KZ":
                run_Check(testChoice[i],"uptime", "uptime")
                """This is a quick way to view the load averages, which indicate the number of tasks (processes) wanting to run. On Linux systems, these numbers include processes wanting to run on CPU, as well as processes blocked in uninterruptible I/O (usually disk I/O). This gives a high level idea of resource load (or demand), but can’t be properly understood without other tools. Worth a quick look only.
The three numbers are exponentially damped moving sum averages with a 1 minute, 5 minute, and 15 minute constant. The three numbers give us some idea of how load is changing over time. For example, if you’ve been asked to check a problem server, and the 1 minute value is much lower than the 15 minute value, then you might have logged in too late and missed the issue."""
            if testChoice[i].upper() in "V":
                view_Logs()
            if testChoice[i].upper() in "Q":
                break
            i=+1
    else:
        print("Please choose from the options provided in the menu.")
print("Done.")

#
# Info about these checks can be found at https://medium.com/netflix-techblog/linux-performance-analysis-in-60-000-milliseconds-accc10403c55
# See more checks at https://medium.com/netflix-techblog/netflix-at-velocity-2015-linux-performance-tools-51964ddb81cf
#