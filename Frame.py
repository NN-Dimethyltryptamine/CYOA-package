import Connection

class Frame:
    """
    Param stuff:
    - adventure- name of the current adventure
    - speaker- person speaking
    - text- body text
    - connections[]- Connection objects out
    - flags- flags, not sure what for
    """
    
    def __init__(self, frameNum, adventure="", text="", connections=[], flags=[]):
        self.adventure = adventure
        self.text = text
        self.connections = []
        self.flags = []
        self.frameNum = frameNum
        """ flags contain info about the frame
        - chanceN: on a non decision frame, path can branch with probability
        - chanceD: on a decision frame, certain decisions may show up with probability
        - more tags to be added, potientially
        """

    def setAdventure(self, adventure):
        self.adventure = adventure
    
    def setText(self, text: str):
        self.text = text
    
    def getText(self):
        return self.text
    
    def addConnection(self, connection):
        self.connections.append(connection)

    def getConnections(self):
        return self.connections
    
    def addFlag(self, flag):
        self.flags.append(flag)
    
    def getFlags(self):
        return self.flags
    
    def __str__(self):
        return f"{self.adventure}: {self.frameNum} | Text: {self.text}"

class DecisionFrame(Frame):
    
    def __init__(self, frameNum, adventure="", text="", connections=[], flags=[]):
        super().__init__(frameNum, adventure, text, connections, flags)

class DialogueFrame(Frame):
    
    def __init__(self, frameNum, adventure="", speaker="", text="", flags=[]):
        self.speaker = speaker
        super().__init__(frameNum, adventure, text, [], flags)
    
    def setSpeaker(self, speaker):
        self.speaker = speaker
    
    def getSpeaker(self):
        return self.speaker

class TextFrame(Frame):
    
    def __init__(self, frameNum, adventure="", text="", flags=[]):
        super().__init__(frameNum, adventure, text, [], flags)


class ChanceFrame(Frame):

    def __init__(self, frameNum, adventure="", text="", chance=1, skipTo=-1, flags=[]):
        self.chance = chance
        self.skipTo = skipTo
        super().__init__(frameNum, adventure, text, [], flags)
    
    def setChance(self, chance):
        self.chance = chance
    
    def getChance(self):
        return self.chance

    def setSkipTo(self, skipTo):
        self.skipTo = skipTo
    
    def getSkipTo(self):
        return self.skipTo

class CheckFrame(Frame):

    def __init__(self, frameNum, adventure="", text="", checks=[], skipTo=-1, flags=[]):
        self.checks = checks
        self.skipTo = skipTo
        super().__init__(frameNum, adventure, text, [], flags)
    
    def setChecks(self, checks):
        self.checks = checks
    
    def getChecks(self):
        return self.checks
    
    def setSkipTo(self, skipTo):
        self.skipTo = skipTo
    
    def getSkipTo(self):
        return self.skipTo

    # note to self: driver can look through list of checks, make the necessary checks, and decide whether or not to render the frame