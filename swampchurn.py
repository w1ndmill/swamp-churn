# swampchurn
# by slipperyslope
#
# TODO:
# - Chat monitoring
# - Connect monitoring
# - Keyword detection
#

from logClasses import *
import os.path

# log file name (optional)
rawLogs = ""

def main():
    global rawLogs
    
    if not rawLogs:
        rawLogs = input("Enter log file name: ")
    while not os.path.isfile(rawLogs):
        rawLogs = input("Error: File \"" + rawLogs + "\" not found\nEnter log file name: ")
    print("Log file \"" + rawLogs + "\" found. Processing...")

    logs = swampLogs(rawLogs)
    logs.build()

    for log in logs.logList:
        if(log.type() == "video"):
            print(log)

if __name__ == "__main__":
    main()
