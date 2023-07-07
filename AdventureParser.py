from Frame import Frame, DecisionFrame, DialogueFrame, TextFrame, ChanceFrame, CheckFrame
from Connection import Connection, ProbabilityConnection, PrereqConnection, ThresholdConnection, SkillConnection
from Adventure import Adventure
import os.path, os

class AdventureParser:
    
    def __init__(self):
        pass

    def getChoiceHeader(self, choice):
        return choice[1:choice.index(")")]
    
    def getChoiceContent(self, choice):
        return choice[choice.index(')')+1:].lstrip().rstrip()

    def getFrame(self, frameType, framelines, frameIndex, name):
        frame, jump = None, None
        match frameType:
            case "decision":
                frame, jump = self.getDecisionFrame(framelines, frameIndex, name)
            case "dialogue":
                frame, jump = self.getDialogueFrame(framelines, frameIndex, name)
            case "text":
                frame, jump = self.getTextFrame(framelines, frameIndex, name)
            case "chance":
                frame, jump = self.getChanceFrame(framelines, frameIndex, name)
            case "check":
                frame, jump = self.getCheckFrame(framelines, frameIndex, name)
            case _:
                raise Exception(f"Could not identify frame type of frame {frameIndex}: {frameType}")
        return (frame, jump)
    
    def getDecisionFrame(self, framelines, frameIndex, name):
        frame = DecisionFrame(frameNum=frameIndex, adventure=name)
        # reminder: header looks like: decision
        textContent = framelines[1]
        frame.setText(textContent)
        # read number of decisions
        decisionNum = int(framelines[2])
        choices = framelines[3:]
        # add them as connections
        for i in range(decisionNum):
            decision = choices[i]
            header = self.getChoiceHeader(decision)
            choiceContent = self.getChoiceContent(decision)
            if header.startswith("reg"):
                # reminder: header looks like: (reg->s#)
                c = Connection(frameIndex, int(header.split("->")[1].strip()[1:]), choiceContent)
                frame.addConnection(c)
            elif header.startswith("prob"):
                # reminder: header looks like: (prob:#->s#)
                prob, dest = header.split("->")
                prob = float(prob.split(":")[1].strip())
                dest = int(dest.strip()[1:])
                c = ProbabilityConnection(frameIndex, dest, choiceContent, prob)
                frame.addConnection(c)
            elif header.startswith("prereq"):
                # reminder: header looks like: (prereq:[smth,!smth]->s#)
                reqs, dest = header.split("->")
                reqs = reqs[1:-1].split(",")
                dest = int(dest.strip()[1:])
                c = PrereqConnection(frameIndex, dest, choiceContent, reqs)
                frame.addConnection(c)
            elif header.startswith("thresh"):
                # print(f"adding thresh connection to frame {frameIndex}")
                threshs, dest = header.split("->")
                threshs = threshs.split(':')[1][1:-1].split(",")
                dest = int(dest.strip()[1:])
                c = ThresholdConnection(frameIndex, dest, choiceContent, threshs)
                frame.addConnection(c)
            elif header.startswith("skill"):
                # print(f"adding thresh connection to frame {frameIndex}")
                threshs, dests = header.split("->")
                # should only take one threshold but support for multiple just in case
                threshs = threshs[1:-1].split(",")
                dests = [int(x) for x in dests.strip().split(",")]
                c = SkillConnection(frameIndex, dest[0], dest[1], choiceContent, threshs)
                frame.addConnection(c)
        return (frame, 3 + decisionNum)
    
    def getDialogueFrame(self, framelines, frameIndex, name):
        frame = DialogueFrame(frameNum=frameIndex, adventure=name)
        # reminder: header looks like: dialogue
        frame.setSpeaker(framelines[1])
        frame.setText(framelines[2])
        return (frame, 3)
    
    def getTextFrame(self, framelines, frameIndex, name):
        frame = TextFrame(frameNum=frameIndex, adventure=name)
        # reminder: header looks like: text
        frame.setText(framelines[1])
        return (frame, 2)
    
    def getChanceFrame(self, framelines, frameIndex, name):
        frame = ChanceFrame(frameNum=frameIndex, adventure=name)
        # reminder: header looks like: chance:#->s# // s# is skipTo
        chance, skipTo = framelines[0].strip().split("->")
        chance = float(chance.split(":")[1].strip())
        skipTo = int(skipTo.strip()[1:])
        frame.setChance(chance)
        frame.setText(framelines[1])
        frame.setSkipTo(skipTo)
        return (frame, 2)
    
    def getCheckFrame(self, framelines, frameIndex, name):
        frame = CheckFrame(frameNum=frameIndex, adventure=name)
        # reminder: header looks like: check:[STAT>smth]->s# // s# is skipTo
        checks, skipTo = framelines[0].strip().split(":")[1].split("->")
        checks = checks[1:-1].split(",")
        skipTo = int(skipTo.strip()[1:])
        frame.setChecks(checks)
        frame.setText(framelines[1])
        frame.setSkipTo(skipTo)
        return (frame, 2)

    def parse(self, adventurePath: str):
        if not os.path.isfile(adventurePath):
            raise Exception(f"AdventureParser could not find file {adventurePath}")
        adv = Adventure()
        filelines = []
        try:
            with open(adventurePath, 'r') as file:
                filelines = [line.rstrip() for line in file.readlines()]
        except Exception as exp:
            raise Exception(f"Could not open file. {exp}")
        # get speakers
        speakers = int(filelines[0])
        readLine = 1
        # read in speakers
        for _ in range(speakers):
            # error handling? or maybe have a separate validator class
            speaker = filelines[readLine]
            speakerPair = speaker.split(':',1)
            adv.addSpeaker(speakerPair[0], speakerPair[1])
            readLine = readLine + 1
        readLine = readLine + 1
        # sets adventure name
        name = filelines[readLine]
        print(name)
        adv.setName(name)
        # jump to frames & sequences
        readLine = readLine + 2
        frameIndex = 0
        while True:
            if readLine >= len(filelines):
                break
            line = filelines[readLine]
            if not line: # empty lines
                readLine = readLine + 1
                continue
            if line.startswith('//'): # comment lines
                readLine = readLine + 1
                continue
            if line.startswith('s'): # sequence headers
                adv.addSequenceHead(frameIndex)
                readLine = readLine + 1
                continue
            if line.find("//") > 0: # remove comments
                line = line[:line.find("//")]
            frame, jump = self.getFrame(line.split(':')[0], filelines[readLine:], frameIndex, name)
            readLine = readLine + jump
            endline = filelines[readLine]
            if endline.startswith("goto"):
                dest = int(endline.split('->')[1][1:])
                connection = Connection(frameIndex, dest, "goto connection")
                frame.addConnection(connection)
                readLine = readLine + 1
            if endline.startswith("advEnd"):
                frame.addFlag("endFrame")
                readLine = readLine + 1
            # implicit skip over "end [frametype]" line
            readLine = readLine + 1
            adv.addFrame(frame)
            frameIndex = frameIndex + 1
        print("Parse finished!")
        return adv
