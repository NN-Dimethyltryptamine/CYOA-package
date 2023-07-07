class AdventureInfo:

    def __init__(self):
        self.inAdventure = False
        self.activeAdventure = "" # name of current adventure
        self.currentFrame = -1 # frame in current adventure
        self.flags = {} # we'll figure something out

class Character:

    def __init__(self, name, adventureInfo):
        self.name = name
        self.stats = {
            "physical": {
                "vitality": 10, # VIT
                "strength": 5, # STR
                "dexterity": 5 # DEX
            },
            "mental": {
                "poise": 5, # deception, keeping calm under pressure/intimidation, willpower
                # ^ control of oneself (internal), POI
                "presence": 5, # intimidation, command of respect, authoritativeness
                # ^ control of one's image (external), PRS
                "insight": 5, # persuasion, reading people, awareness of surroundings, perceptiveness
                # ^ awareness of one's surroundings, environment, and people, INS
                # note to self: maybe split environmental awareness and social awareness?
                # do we even need this many social stats here
            },
            "magical": {
                "capacity": 5, # CAP
                "regen": 5, # RGN
                "control": 5 # CTL
            }
        }
        self.items = {
            "weapon": None,
            "armour": None,
            "trinket": None, # could be a charm, an amulet, a talisman, a banner, a ring, a necklance, whatever
            "misc": [
                None # should prolly cap a carrying capacity
            ]
        }
        self.adventureInfo = adventureInfo
        self.companions = [
            None
        ]

    def getStat(self, stat):
        match stat:
            case "vitality" | "strength" | "dexterity":
                return self.stats["physical"][stat]
            case "poise" | "presence" | "insight":
                return self.stats["mental"][stat]
            case "capacity" | "regen" | "control":
                return self.stats["magical"][stat]
            case _:
                print("we shouldn't be here!")
                None
