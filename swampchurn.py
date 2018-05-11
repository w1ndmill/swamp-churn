# swampchurn
# by slipperyslope
#
# TODO:
# - Chat monitoring
# - Keyword detection
# - Prompt to continue if forcelogs doesn't exist

from logClasses import swampLogs, logEntry
from os.path import isfile as isFile
from sys import exit
import argparse
import configparser

def verifyFile(filename, fromParser = True):
    if not isFile(filename):
        if fromParser: raise argparse.ArgumentTypeError(f"File {filename} not found. Aborting...")
        print(f"File {filename} not found. Aborting...")
        exit()
    return filename

def main():
    desc = """
                                           _
             ____ __ ____ _ _ __  _ __  __| |_  _ _ _ _ _ _
            (_-< V  V / _` | '  \| '_ \/ _| ' \| | | '_| ' \\
            /__/\_/\_/\__,_|_|_|_| .__/\__|_||_\_,_|_| |_|_|
                                 |_|
                    version 0.2 -- by slipperyslope
    """
    parser = argparse.ArgumentParser(description=desc,formatter_class=argparse.RawTextHelpFormatter)
    filegroup = parser.add_mutually_exclusive_group()
    parser.add_argument('-k', '--addKeyword', action='store', help = 'add/overwrite keyword to database ')
    parser.add_argument('-u', '--addUser', action='store', help = 'add/overwrite user to database')
    parser.add_argument('-s', '--addSpray', action='store', help = 'add/overwrite spray id to database')
    parser.add_argument('-v', '--addVideo', action='store', help = 'add/overwrite video id to database')

    filegroup.add_argument('-n', '--noBuild', action='store_false', help='prevent building of logs')
    filegroup.add_argument('-f', '--forceLogs', type=verifyFile,  help = 'override raw log file from config')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    if isFile("settings.ini"):
        config.read("settings.ini")
    else:
        with open("settings.ini",'w+') as newSettings:
            newSettings.write("[Paths]\nrawLogs = \ndatabase = ")
        print("No settings file found. New \"settings.ini\" created")
        exit()

    if args.forceLogs: rawLogs = args.forceLogs
    else: rawLogs = verifyFile(config["Paths"]["rawLogs"], False)

    logs = swampLogs(rawLogs)
    logs.build()

    videos, sprays = logs.getLists("video","spray")
    for video in videos:
        print(video)

if __name__ == "__main__":
    main()
