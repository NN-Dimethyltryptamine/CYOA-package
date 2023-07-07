from Adventure import Adventure
from AdventureParser import AdventureParser
from Character import Character, AdventureInfo
from Frame import Frame
import random

class AdventureDriver:

    def startAdventure(adv: Adventure, char: Character):
        char.adventureInfo.inAdventure = True
        char.adventureInfo.activeAdventure = adv.getName
        char.adventureInfo.currentFrame = 0
        return adv.getFrame(0)
    
    def endAdventure(adv: Adventure, char: Character):
        char.adventureInfo.inAdventure = False
        char.adventureInfo.activeAdventure = ""
        char.adventureInfo.currentFrame = -1
        return

    def frame(adv: Adventure, char: Character):
        if char.adventureInfo.currentFrame == -1:
            return
        frame = adv.getFrame(char.adventureInfo.currentFrame)
        frameType = type(frame).__name__
        match frameType:
            case "DecisionFrame" | "DialogueFrame":
                return frame
            case "ChanceFrame":
                rand = random.random()
                if rand <= frame.getChance():
                    return frame
                else:
                    # gotta remember that getSkipTo returns sequence number and not frame number!!!
                    skipTo = frame.getSkipTo()
                    char.adventureInfo.currentFrame = skipTo
                    return adv.getSequenceHead(skipTo)
            case "CheckFrame":
                advInfo = char.adventureInfo
                skipTo = frame.getSkipTo()
                for check in frame.getChecks():
                    # random roll for each check
                    # should probably find a way to give feedback to players
                    rand = random.randint(1,100)
                    # if anything does not pass, fail and go to skipTo frame
                    if '<' in check:
                        stat, boundary = check.strip().split('<')
                        if (char.getStat(stat) + rand) >= int(boundary):
                            advInfo.currentFrame = skipTo
                            return adv.getSequenceHead(skipTo)
                    elif '>' in check:
                        print(check)
                        stat, boundary = check.strip().split('>')
                        if (char.getStat(stat) + rand) <= int(boundary):
                            advInfo.currentFrame = skipTo
                            return adv.getSequenceHead(skipTo)
                    else:
                        # checking flags
                        pass
                # passes all checks
                return frame
            case _:
                # just TextFrame here lmao
                return frame

    
    def renderFrame(adv: Adventure, frame: Frame, char: Character):
        frameType = type(frame).__name__
        nextConnections = frame.getConnections()
        print()
        print('=======================================')
        print(f'> Frame {char.adventureInfo.currentFrame} <')
        match frameType:
            case "DecisionFrame":
                print("Decision Time!")
                nextConnections = []
                connections = frame.getConnections()
                for connection in connections:
                    connectionType = type(connection).__name__
                    match connectionType:
                        case 'ProbabilityConnection':
                            rand = random.random()
                            if rand <= connection.getProbability():
                                nextConnections.append(connection)
                        case "PrereqConnection":
                            # something to do with character flags. we'll figure that out later
                            pass
                        case "ThresholdConnection":
                            checks = connection.getThresholds()
                            checkTotal = len(checks)
                            checkNum = 0
                            stats = char.stats
                            for check in checks:
                                if '<' in check:
                                    stat, boundary = check.strip().split('<')
                                    if (char.getStat(stat) + rand) < int(boundary):
                                        checkNum = checkNum + 1
                                elif '>' in check:
                                    stat, boundary = check.strip().split('>')
                                    # print(stat)
                                    if (char.getStat(stat) + rand) > int(boundary):
                                        checkNum = checkNum + 1
                            if checkNum == checkTotal:
                                nextConnections.append(connection)
                        case "Connection" | _:
                            nextConnections.append(connection)
                for number, connection in enumerate(nextConnections):
                    print(f"{number}. {connection.getLabel()}")
            case "DialogueFrame":
                print(f"Speaker: {frame.getSpeaker()}")
                print(f"Speaker imgUrl: {adv.getSpeakerUrl(frame.getSpeaker())}")
                print(frame.getText())
            case _: # TextFrame, ChanceFrame, and ChecKFrame have essentially the same content. any rolls/checks will be done before rendering, so all three can be rendered the same way
                print(frame.getText())
        if "endFrame" in frame.getFlags():
            print("End Frame Reached")
            AdventureDriver.endAdventure(adv, char)
            return
        AdventureDriver.choice(adv, char, nextConnections)
        
    # the callback function
    def next(adv, char, connections, choice):
        # print(connections)
        char.adventureInfo.currentFrame = adv.sequenceHeads[connections[choice].getToSequence()]

    def choice(adv, char, connections=[]):
        choice = int(input("input something pls: "))
        if not connections:
            char.adventureInfo.currentFrame = char.adventureInfo.currentFrame + 1
            return
        AdventureDriver.next(adv, char, connections, choice)
