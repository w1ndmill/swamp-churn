import re
from urllib.parse import unquote

class swampLogs(object):
    """
    Contain and manage all logs

    Attributes:
                            filename for...
        logsFilename ...... raw logs
        blacklistFilename . list of banned videos
        idFilename ........ list of steam ids of suspicious users
        wordFilename ...... list of suspicious words

        logList .......... list of logEntry instances

                            toggle retention of...
        retainVideos ...... video logs (default: True)
        retainSprays ...... spray logs (default: True)
        retainChat ........ chat logs (default: False)
        retainConnects .... connect/disconnect logs (default: False)
        retainStaff ....... staff action logs (default: False)
        retainHoratio ..... horatio sourced videos (default: False)
        retainTwitch ...... twitch sourced videos (default: False)

    """


    """
    Regex definition(s)
    """
    logRegex = re.compile(r"\[((?:\d+?.)+)\] (.{1,32})?\((STEAM_0:\d:\d+)\)(.+(?:\n\t.+){0,3})")


    def __init__(self, logsFilename, blacklistFilename = None, idFileName = None, wordFilename = None,
                 retainVideos = True, retainSprays = True, retainChat = False, retainConnects = False,
                 retainStaff = False, retainHoratio = False, retainTwitch = False):
        """
        Set default settings and filenames for logs list
        """
        self.logsFilename = logsFilename
        self.blacklistFilename = blacklistFilename
        self.idFileName = idFileName
        self.wordFilename = wordFilename

        self.logList = []

        self.retainVideos = retainVideos
        self.retainSprays = retainSprays
        self.retainChat = retainChat
        self.retainConnects = retainConnects
        self.retainStaff = retainStaff
        self.retainHoratio = retainHoratio
        self.retainTwitch = retainTwitch


    def build(self, encode="utf8"):
        """
        Read log file and create log entries via logEntry. Return false if building
        error occured, otherwise return true
        """

        try:
            with open(self.logsFilename, "r", encoding = encode) as rawFile:
                self.rawStrings = self.logRegex.findall(rawFile.read())

            for log in self.rawStrings:
                t,n,i,l = log
                toAppend = logEntry(t,n,i,l)
                toAppend.process()
                self.logList.append(toAppend)
        except:
            return False
        return True


    def getLists(self,*types):
        """
        Returns list(s) of a user-defined log type(s) and returns as tuple in
        order originally requested
        """

        self.logLists = [[] for type in types]
        for log in self.logList:
            for num,type in enumerate(types):
                if type == log.type():
                    if ((log.source == "horatio") and not self.retainHoratio) or ((log.source == "twitch") and not self.retainTwitch):
                        continue
                    self.logLists[num].append(log)
                    break

        return tuple(self.logLists)


class logEntry(object):
    """
    Individual log entry

    Attributes:
        time .............. exact time when event occured (format HH:MM:SS)
        username .......... username of person at time of event
        steamid ........... static steam id of person
        rawLog ............ preprocessed log entry

        logType ........... type of event that occurred (e.g. chat message, video played)
        title ............. title of video played; applicable for videos only
        source ............ source of the event (e.g. youtube, imgur); applicable for sprays/videos
        id ................ image/video id for event; applicble for sprays/videos
        message ........... message typed in chat; applicable for chat
        ip ................ partially censored IP address of user; applicable for connects

        risk .............. numerical value for suspectability of rule-breaking
    """

    """
    Regex definitions
    """
    vidRegex = re.compile(r"played (video): (.+) \((\w+) \/ (.+)\)")
    sprayRegex = re.compile(r"created (spray): \w+\.(imgur|gfycat).com\/(\w+)\.?")
    # chatRegex = re.compile(r'')
    # connectRegex = re.compile(r'')

    def __init__(self, time, username, steamid, rawLog):
        """
        Collect pre-analyzed log entries. Set post-analysis variables to None
        """

        self.time = time
        self.username = username.strip()
        self.steamid = steamid
        self.rawLog = rawLog.strip()

        self.logType = None
        self.title = None
        self.source = None
        self.id = None
        self.message = None
        self.ip = None
        self.risk = None


    def type(self):
        """
        Returns logType. If logType is None, run analyze to set it a value
        """

        if self.logType is None: self.process()
        return self.logType


    def process(self):
        """
        Determine the type of log the rawLog along with assigning
        applicable variables
        """

        self.rawLog = unquote((self.rawLog).replace("\t"," ").replace("\n",""))

        # Chat detection
        if self.rawLog[0] in {":","/"}:
            self.logType = "chat"

        # Connection detection
        elif self.rawLog[0] in {"d","s"}:
            self.logType = "connection"

        # Video + Twitch Detection
        elif self.rawLog[0:2] == "pl":
            self.temp = self.vidRegex.match(self.rawLog)
            if self.temp is not None:
                self.logType, self.title, self.source, self.id = self.temp.groups()
            else:
                self.logType = "twitch"

        # Spray detection
        elif self.rawLog[6:9] == "d s":
            # print(self.time,self.rawLog)
            self.logType, self.source, self.id = self.sprayRegex.match(self.rawLog).groups()

        # Vote detection
        elif self.rawLog[0:2] in {"fa","cr"}:
            self.logType = "vote"

        # Staff action detection
        elif self.rawLog[0:2] in {"pe","ba","us","ki"}:
            self.logType = "staffaction"

        else: self.logType = "unknown"

    def analyzeRisk(self):
        pass

    def __str__(self):
        """
        Return log as originally given
        """
        return f"[{self.time}] {self.username} ({self.steamid}) {self.rawLog}"
