from dump4 import * #get specific ids from data.py

infile = "/Volumes/SWITCH SD/switch/Checkpoint/saves/0x010086C00AF7C000 0x010086C00AF7C000/20470220-172708 XAW/USERDATA00/data.bin"
#infile = "/Volumes/UNTITLED/switch/Checkpoint/saves/0x010086C00AF7C000 0x010086C00AF7C000/0 copy/USERDATA00/data.bin"

def edit(position, location, money, namelist, gatcharemaining, gatchamax, characterlist, yokailist, itemlist, specialsoullist, yokaisoullist, equipmentlist):
    #helper functions defined in dump4.py
    namelist = {'nate': 'Nate', 'katie': 'Katie', 'summer': 'Summer', 'cole': 'Cole', 'bruno': 'Bruno', 'jack': 'Jack'} #fix names
    
    for i in range(len(yokailist)):
        yokailist = edit_yokai(yokailist, i, "shogunyan", "") #get id from data.py if it isn't working

    for i in range(6):
        characterlist = edit_yokai(characterlist, i) #max stats


    print(", ".join([characters[i["yokai"]]for i in characterlist]))
    print(", ".join([characters[i["yokai"]]for i in yokailist]))
    print(", ".join([items[i["item"]]for i in itemlist]))
    print(", ".join([equipments[i["equipment"]]for i in equipmentlist]))
    print(locations[location])

    return position, location, money, namelist, gatcharemaining, gatchamax, characterlist, yokailist, itemlist, specialsoullist, yokaisoullist, equipmentlist #all editable


main(infile, edit)