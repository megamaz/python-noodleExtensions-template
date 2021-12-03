import json


LEVELIN = "ExpertStandard.dat"
LEVELOUT = "ExpertPlusStandard.dat"


# just like the JS version, this simply counts how many times you ran the program. 
count = int(open("./count.txt").read())
print(f"GIVE IT UP FOR ROUND {count}")
count += 1
open("./count.txt", 'w').write(str(count))

#region seutp
level = json.load(open(f"./{LEVELIN}"))

# clear all existing customData
f = lambda x: level["_notes"][x].pop("_customData")
_ = [f(x) for x in range(len(level["_notes"])) if level["_notes"][x].get("_customData")]
f = lambda x: level["_obstacles"][x].pop("_customData")
_ = [f(x) for x in range(len(level["_obstacles"])) if level["_obstacles"][x].get("_customData")]

level["_customData"] = {
    "_customEvents":[],
    "_pointDefinitions":[]
}

_notes:list = level["_notes"]
_obstacles:list = level["_obstacles"]
_customEvents:list = level["_customData"]["_customEvents"]
_pointDefinitions:list = level["_customData"]["_pointDefinitions"]


#endregion

#region helper functions

def lerp(v0, v1, t):
    return v0*(1-t)+v1*t

def trackOnNotesBetween(track:str, p1:float, p2:float):
    """Simply puts a track on all notes between two beats."""
    for x in range(len(_notes)):
        if not (_notes[x]["_time"] >= p1 and _notes[x]["_time"] <= p2):
            continue

        if not _notes[x].get("_customData"):
            _notes[x]["_customData"] = {}

        _notes[x]["_customData"]["_track"] = track

def offsetOnNotesBetween(offset:float, p1:float, p2:float):

    for x in range(len(_notes)):
        if not (_notes[x]["_time"] >= p1 and _notes[x]["_time"] <= p2):
            continue

        if not _notes[x].get("_customData"):
            _notes[x]["_customData"] = {}

        _notes[x]["_customData"]["_noteJumpStartBeatOffset"] = offset

def trackOnNotesBetweenRBSep(trackR:float, trackB:float, p1:float, p2:float, offset:float=None):

    for x in range(len(_notes)):
        if not (_notes[x]["_time"] >= p1 and _notes[x]["_time"] <= p2):
            continue

        if not _notes[x].get("_customData"):
            _notes[x]["_customData"] = {}

        if offset: _notes[x]["_customData"]["_noteJumpStartBeatOffset"] = offset

        if _notes[x]["_type"] == 0: _notes[x]["_customData"]["_track"] = trackR
        elif _notes[x]["_type"] == 1: _notes[x]["_customData"]["_track"] = trackB


def trackOnNotesBetweenDirSep(p1:float, p2:float, dir:int, track:str, offset=None):
    """Works a bit differently than the demo.js one\n
    (the center should look like a square on most OS, though imagine it's the note and the number is the direction it's point in)\n
    ```
    4 0 5
    2 ■ 3
    6 1 7
    ```\n
    dot-note: 8\n
    """

    for x in range(len(_notes)):
        if not (_notes[x]["_time"] >= p1 and _notes[x]["_time"] <= p2):
            continue

        if not _notes[x].get("_customData"):
            _notes[x]["_customData"] = {}

        if offset: _notes[x]["_customData"]["_noteJumpStartBeatOffset"] = offset

        if _notes[x]["_cutDirection"] == dir: _notes[x]["_customData"]["_track"] = track


#endregion
level["_notes"] = _notes
level["_obstacles"] = _obstacles
level["_customData"]["_customEvents"] = _customEvents
level["_customData"]["_pointDefinitions"] = _pointDefinitions

json.dump(level, open(f"./{LEVELOUT}", 'w'))
