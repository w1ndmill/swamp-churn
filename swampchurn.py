# swampchurn
# by slipperyslope
#
# TODO:
# - Chat monitoring
# - Connect monitoring
# - Keyword detection
# - rad

from logClasses import swampLogs, logEntry
import os.path
import argparse

def main():
    desc = """
                                           _
             ____ __ ____ _ _ __  _ __  __| |_  _ _ _ _ _ _
            (_-< V  V / _` | '  \| '_ \/ _| ' \| | | '_| ' \\
            /__/\_/\_/\__,_|_|_|_| .__/\__|_||_\_,_|_| |_|_|
                                 |_|
                      version 0.2 -- slipperyslope
    """
    parser = argparse.ArgumentParser(description=desc,formatter_class=argparse.RawTextHelpFormatter)
    filegroup = parser.add_mutually_exclusive_group()
    parser.add_argument('-k', '--addKeyword', action='store', help = 'add/overwrite keyword to database ')
    parser.add_argument('-u', '--addUser', action='store', help = 'add/overwrite user to database')
    parser.add_argument('-s', '--addSpray', action='store', help = 'add/overwrite spray id to database')
    parser.add_argument('-v', '--addVideo', action='store', help = 'add/overwrite video id to database')

    filegroup.add_argument('-n', action='store_false', help='prevent building of logs')
    filegroup.add_argument('-f', help = 'force raw logs file')
    parser.parse_args()

    rawLogs = ""

    if not rawLogs:
        rawLogs = input("Enter log file name: ")
    while not os.path.isfile(rawLogs):
        rawLogs = input("Error: File \"" + rawLogs + "\" not found\nEnter log file name: ")
    print("Log file \"" + rawLogs + "\" found. Processing...")

    logs = swampLogs(rawLogs)
    logs.build()
    videos, sprays = logs.getLists("video","spray")
    for video in videos:
        print(video)

if __name__ == "__main__":
    main()
