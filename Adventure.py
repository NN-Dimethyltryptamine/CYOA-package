class Adventure:
    # speaker dicts are objects of name: imageUrl
    # knownspeakers might be stored externally
    # knownspeakers is a global thing shared across all adventures
    knownspeakers = {
        "???": "https://as1.ftcdn.net/v2/jpg/00/57/04/58/500_F_57045887_HHJml6DJVxNBMqMeDqVJ0ZQDnotp5rGD.jpg"
    }

    def __init__(self):
        self.name = ""
        self.speakers = {}
        self.sequenceHeads = []
        self.frames = []
        
    def setName(self, advName):
        self.name = advName
    
    def getName(self):
        return self.name

    def addSpeaker(self, speaker, imgUrl):
        self.speakers.update({speaker: imgUrl})
    
    def addFrame(self, frame):
        self.frames.append(frame)
    
    def getFrame(self, frameNum):
        return self.frames[frameNum]
    
    def addSequenceHead(self, frameNum):
        self.sequenceHeads.append(frameNum)
    
    def getSequenceHead(self, sequenceNum):
        '''
        Returns the first Frame in the sequence specified by sequenceNum
        '''
        return self.frames[self.sequenceHeads[sequenceNum]]
    
    def getSpeakerUrl(self, speaker):
        return {**Adventure.knownspeakers, **self.speakers}[speaker]
    
    def numFrames(self):
        return len(self.frames)
    
    def info(self):
        return {
            "name": self.name,
            "speakers": {**Adventure.knownspeakers, **self.speakers},
            "sequenceCount": len(self.sequenceHeads),
            "frameCount": len(self.frames)
        }
    
    