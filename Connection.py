class Connection:
    """
    Param stuff:
    - fromFrame: number of frame of origin
    - toSequence: number of destination sequence (is a list because SkillCheckConnection requires it :/)
    - label: text to show on button
    - probability: probability of this connection showing up
    - prereqs: list of prereqs for this connection to show up (still figuring out how to do this one)
    - thresholds: list of thresholds that need to be passed for this connection to show up (mostly stats)
    """

    def __init__(self, fromFrame, toSequence, label):
        self.fromFrame = fromFrame
        self.toSequence = toSequence
        self.label = label
    
    def getLabel(self):
        return self.label
    
    def getToSequence(self):
        return self.toSequence
    
    def __str__(self):
        return f"{type(self).__name__} connection from {self.fromFrame} to {self.toSequence} with label {self.label}"


class ProbabilityConnection(Connection):

    def __init__(self, fromFrame, toSequence, label, probability):
        self.probability = probability
        super().__init__(fromFrame, toSequence, label)
    
    def getProbability(self):
        return self.probability


class PrereqConnection(Connection):

    def __init__(self, fromFrame, toSequence, label, prereqs):
        self.prereqs = prereqs
        super().__init__(fromFrame, toSequence, label)


class ThresholdConnection(Connection):

    def __init__(self, fromFrame, toSequence, label, thresholds):
        self.thresholds = thresholds
        super().__init__(fromFrame, toSequence, label)
    
    def getThresholds(self):
        return self.thresholds

class SkillConnection(Connection):

    def __init__(self, fromFrame, toSequence, toFailSequence, label, threshold):
        self.toFailSequence = toFailSequence
        self.threshold = threshold
        super().__init__(fromFrame, toSequence, label)

    # note to self: how this works is in the driver it checks whether or not the roll meets the threshold. if it does, it gets the toSequence of this connection. if it doesn't, it gets the toFailSequence of this connection. scuffed? yeah. what are you gonna do about it huh