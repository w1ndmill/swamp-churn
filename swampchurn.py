# swampchurn
# by slipperyslope
#
# TODO:
# - Chat monitoring
# - Keyword detection
# - Prompt to continue if forcelogs doesn't exist
# - Database implementation and arguement

from logClasses import swampLogs, logEntry
from os.path import isfile as isFile
from sys import exit
import argparse
import configparser

configFile = "settings.ini"

def verifyFile(filename, fromParser = True):
    if not isFile(filename):
        if fromParser: raise argparse.ArgumentTypeError(f"File {filename} not found. Aborting...")
        print(f"File {filename} not found. Aborting...")
        exit()
    return filename

def createConfig(cfg):
    with open(cfg,'w+') as newSettings:
        newSettings.write("[Paths]\nrawLogs = \ndatabase = \nchatDump = logs\chatDump.txt")
    print(f"No settings file found. New \"{configFile}\" created")
    exit()

def appendToFile(lst,filename):
    with open(filename,"a+",encoding="utf8") as dump:
        for item in lst:
            dump.write(str(item.message) + "\n")

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
    filegroup.add_argument('-n', '--noBuild', action='store_true', help = 'prevent building of logs')
    filegroup.add_argument('-f', '--forceLogs', type=verifyFile,  help = 'override raw log filename from config')
    parser.add_argument('-d', '--forcedb', type=verifyFile, help = 'override database filename from config')
    parser.add_argument('--storeChatLogs', action='store_true', help = 'store chat logs into file for misc use')

    args = parser.parse_args()

    global configFile
    config = configparser.ConfigParser()
    if isFile(configFile): config.read(configFile)
    else: createConfig(configFile)


    if not args.noBuild:
        rawLogs = args.forceLogs if args.forceLogs else verifyFile(config["Paths"]["rawLogs"], False)
        logs = swampLogs(rawLogs)
        logs.build()

        if args.storeChatLogs:
            messages = logs.getLists("chat")
            appendToFile(messages[0],verifyFile(config["Paths"]["chatDump"]))

if __name__ == "__main__":
    main()
