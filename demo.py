import json, math, os, copy


INPUT = "ExpertPlusStandard.dat"
OUTPUT = "ExpertStandard.dat"
difficulty = json.load(open(INPUT))

#region this just counts how many time you ran it for fun, feel free to remove.
if not os.path.exists("count.txt"):
    open("count.txt", 'w').write("0")

count = int(open('count.txt').read())
count += 1
open("count.txt", 'w').write(str(count))
print(f"GIVE IT UP FOR RUN {count}")
#endregion


difficulty["_customData"] = {"_pointDefinitions":[], "_customEvents":[]}

_customData = difficulty["_customData"]
_obstacles = difficulty["_obstacles"]
_notes = difficulty["_notes"]
_customEvents = difficulty["_customData"]["_customEvents"]
_pointDefinitions = difficulty["_customData"]["_pointDefinitions"]

filteredNotes = None

for wall in range(len(_obstacles)):
    if not _obstacles[wall].get("_customData"):
        _obstacles[wall].pop("_customData")

for note in range(len(_notes)):
    if not _notes[note].get("_customData"):
        _notes[note].pop("_customData")


#region helper functions

# round is a built-in python function

def getJumps(njs, offset):
    _startHalfJumpDurationInBeats = 4
    _maxHalfJumpDistance = 18 
    _startBPM = 170
    bpm = 170
    _startNoteJumpMovementSpeed = njs
    _noteJumpStartBeatOffset = offset

    _noteJumpMovementSpeed = (_startNoteJumpMovementSpeed * bpm) / _startBPM
    num = 60/bpm
    num2 = copy.deepcopy(_startHalfJumpDurationInBeats)

    while _noteJumpMovementSpeed * num * num2 > _maxHalfJumpDistance:
        num2 /= 2
    num2 += _noteJumpStartBeatOffset

    if num2 < 1:
        num2 = 1
    
    _jumpDuration = num*num2*2
    _jumpDistance = _noteJumpMovementSpeed * _jumpDuration
    return {"half":num2, "dist":_jumpDistance}

def offestOnNotesBetween(p1, p2, offset):
    filteredNotes = [x for x in _notes if x["_time"] >= p1 and x["_time"] <= p2]

    for filtered in range(len(filteredNotes)):
        #always worth having.
        #man this shit BETTER not be None.
        if offset is not None:
            filteredNotes[filtered]["_customData"]["_noteJumpStartBeatOffset"] = offset
        
    return filteredNotes

def lerp(v0,v1,t):
    return v0*(1-t)+v1*t

def trackOnNotesBetween(track, p1, p2, potentialOffset=None):
    filteredNotes = [x for x in _notes if x["_time"] >= p1 and x["_time"] <= p2]

    for filtered in range(len(filteredNotes)):
        filteredNotes[filtered]["_customData"]["_track"] = track
        if potentialOffset is not None:
            filteredNotes[filtered]["_customData"]["_noteJumpStartBeatOffset"] = potentialOffset
    
    return filteredNotes

#applies a track to notes on two tracks between two times based on the color of the notes
#IT GONNA FUCK UP WITH BOMBS I TELL YOU HWAT BOI
#red, blue, p1, p2, potentialOffset
def trackOnNotesBetweenRBSep(trackR, trackB, p1, p2, potentialOffset=None):
    filteredNotes = [x for x in _notes if x["_time"] >= p1 and x["_time"] <= p2]

    for filtered in range(len(filteredNotes)):
        if potentialOffset is not None:
            filteredNotes[filtered]["_customData"]["_noteJumpStartBeatOffset"] = potentialOffset
        
        if filteredNotes[filtered]["_type"] == 0:
            filteredNotes[filtered]["_customData"]["_track"] = trackR

        if filteredNotes[filtered]["_type"] == 1:
            filteredNotes[filtered]["_customData"]["_track"] = trackB

    
    return filteredNotes

#p1, p2, potentialoffset, up, down, left, right, 
#TODO: ADD OTHER DIRS

def trackOnNotesBetweenDirSep(p1, p2, potentialOffset=None, trackUp=None, trackDown=None, trackLeft=None, trackRight=None):
    filteredNotes = [x for x in _notes if x["_time"] >= p1 and x["_time"] <= p2]

    for filtered in range(len(filteredNotes)):
        if filteredNotes[filtered]["_cutDirection"] == 0 and trackUp is not None: filteredNotes[filtered]["_customData"]["_track"] = trackUp
        if filteredNotes[filtered]["_cutDirection"] == 1 and trackUp is not None: filteredNotes[filtered]["_customData"]["_track"] = trackDown
        if filteredNotes[filtered]["_cutDirection"] == 2 and trackUp is not None: filteredNotes[filtered]["_customData"]["_track"] = trackLeft
        if filteredNotes[filtered]["_cutDirection"] == 4 and trackUp is not None: filteredNotes[filtered]["_customData"]["_track"] = trackRight
        #i might want to make this only run if I assign a track...
        if potentialOffset is not None: filteredNotes[filtered]["_customData"]["_noteJumpStartBeatOffset"] = potentialOffset
        
    return filteredNotes

#endregion

#region use this area to do your stuff

#endregion

#region write file
precision = 4 # decimals to write to

jsonP = math.pow(10, precision)
sortP = math.pow(10, 2)
def deeperDaddy(obj):
    if obj:
        for key in obj.keys():
            if not obj.get(key):
                obj.pop(key)
            elif type(obj.get(key)) == dict:
                deeperDaddy(obj[key])
            elif type(obj.get(key)) == float or type(obj.get(key)) == int:
                obj[key] = float(round(obj[key] + math.e * jsonP) / jsonP)

deeperDaddy(difficulty)

difficulty["_notes"].sort(key=lambda x: x["_time"])
difficulty["_obstacles"].sort(key=lambda x: x["_time"])
difficulty["_events"].sort(key=lambda x: x["_time"])


json.dump(difficulty, open(OUTPUT, 'w'))

#endregion