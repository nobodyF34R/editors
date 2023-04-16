#!/opt/local/bin/python3
# coding: utf-8

"""
dump2.py (SHINNUCHI)

======

The MIT License (MIT)

Copyright (c) 2023 Togenyan, Emilia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from data import * #will eventually remove, added to make program nicer

#functions
def get(read, place, length=1, integer=True, half=False, bigfloat=False):
    finished = ""
    if half:
        return [int(f'{read[place]:08b}'[:4], 2), int(f'{read[place]:08b}'[4:], 2)] 
    else:
        if integer == None: #float
            if read[place:place+length] == b'\x00'*4: #5.877471754111438e-39
                return 0
            hex_int = int.from_bytes(read[place:place+length], "little")
            sign_bit = (hex_int >> 31) & 1
            exponent = ((hex_int >> 23) & 0xFF) - 127
            mantissa = hex_int & 0x7FFFFF
            return (-1)**sign_bit*(1+mantissa/2**23)*2**exponent #may have to remove rounding
        elif integer: #int
            for i in read[place:place+length][-1::-1]:
                finished += f'{i:08b}'
            return int(finished, 2)
        else: #string
            if read[place:place+length][0]==0:
                return ""
            for i in read[place:place+length]:
                if i == 0:
                    break
                finished += chr(i)
            return finished

def give(floa): #some shenanigans to convert a float to bytes
    if floa == 0: return b"\x00"*4
    e = 0
    while floa >= 2: floa, e = floa / 2, e + 1
    while floa < 1: floa, e = floa * 2, e - 1
    return (0 | (e + 127) << 23 | int((floa - 1) * (2**23))).to_bytes(4, 'little')


def edit_yokai(yokailist, index, ownerid, yokai=None, attitude=None, nickname=None): #massively overcomplicated and broken simultaneously 
    try:
        if index < 0:
            index = len(yokailist)-index #appending shortcut
    except:
        pass
    try:
        yokailist[index]
    except:
        temp_yokailist = yokailist #pointless now???
        index = len(yokailist)
        yokailist.append({})
        yokailist[index]["num1"] = 0
        j=0
        for i in range(len(temp_yokailist)):
            if temp_yokailist[i]["num1"] != j:
                yokailist[index]["num1"] = j
                break
            if temp_yokailist[i]["num1"] > yokailist[index]["num1"]:
                yokailist[index]["num1"] = temp_yokailist[i]["num1"]+1
            j+=1
        yokailist[index]["num2"] = 1
        for i in range(j):
            if temp_yokailist[i]["num2"] > yokailist[index]["num2"]:
                yokailist[index]["num2"] = temp_yokailist[i]["num2"]
                location = i
        yokailist[index]["num2"]+=(j-location)
    if yokai != None:
        try:
            yokailist[index]["id"] = reverse_yokais[yokai]
        except:
            yokailist[index]["id"] = yokai
    if nickname != None:
        yokailist[index]["nickname"] = nickname
    yokailist[index]["attack"] = 255 
    yokailist[index]["technique"] = 255
    yokailist[index]["soultimate"] = 255
    yokailist[index]["xp"] = 0 #0 because level is 99
    yokailist[index]["ownerid"] = ownerid
    yokailist[index]["stats"] = {
        "IV_HP": 16, #IV rules: HP / 2 + Str + Spr + Def + Spd = 40
        "IV_Str": 8, 
        "IV_Spr": 8, 
        "IV_Def": 8, 
        "IV_Spd": 8, 
        "CB_HP": 8, #EV rules: HP / 2 + Str + Spr + Def + Spd <= 20
        "CB_Str": 4, 
        "CB_Spr": 4, 
        "CB_Def": 4, 
        "CB_Spd": 4, 
        "SC_HP": 0, #brokennnnn (probably written in a different way) +25, -10 per stat TODO figure out 15?
        "SC_Str": 0, 
        "SC_Spr": 0, 
        "SC_Def": 0, 
        "SC_Spd": 0  
    }
    yokailist[index]["level"] = 99 #255 works too but it automatically lowers to 99
    yokailist[index]["loaflevel"] = 5 #2?
    if attitude != None:
        try:
            yokailist[index]["attitude"] = attitudes.index(attitude)
        except:
            yokailist[index]["attitude"] = attitudes[attitude]

    return sorted(yokailist, key=lambda x:x["num1"])

def edit_item(itemlist, index, item=None, amount=None): #broken for some reason
    try:
        if index < 0:
            index = len(itemlist)-index #appending shortcut
    except:
        pass
    try:
        itemlist[index]
    except:
        index = len(itemlist)
        itemlist.append({})
    itemlist[index]["num1"] = index
    itemlist[index]["num2"] = index+1
    if item:
        try:
            itemlist[index]["item"] = reverse_items[item]
        except:
            itemlist[index]["item"] = item
    if amount:
        itemlist[index]["amount"] = amount
    return itemlist

def edit_equipment(equipmentlist, index, equipment=None, amount=None):
    try:
        if index < 0:
            index = len(equipmentlist)-index #appending shortcut
    except:
        pass
    try:
        equipmentlist[index]
    except:
        index = len(equipmentlist)
        equipmentlist.append({})
    equipmentlist[index]["num1"] = index
    equipmentlist[index]["num2"] = index+1
    if equipment:
        try:
            equipmentlist[index]["equipment"] = reverse_equipments[equipment]
        except:
            equipmentlist[index]["equipment"] = equipment
    if amount:
        equipmentlist[index]["amount"] = amount
    equipmentlist[index]["used"] = 0
    return equipmentlist

def edit_important(importantlist, index, important):
    try:
        if index < 0:
            index = len(importantlist)-index #appending shortcut
    except:
        pass
    try:
        importantlist[index]
    except:
        index = len(importantlist)
        importantlist.append({})
    importantlist[index]["num1"] = index
    importantlist[index]["num2"] = index+1
    try:
        importantlist[index]["important"] = reverse_importants[important]
    except:
        importantlist[index]["important"] = important
    return importantlist

def edit_soul(soullist, index, soul):
    try:
        if index < 0:
            index = len(soullist)-index #appending shortcut (semi-redundant)
    except:
        pass
    try:
        soullist[index]
    except:
        index = len(soullist)
        soullist.append({})
    soullist[index]["num1"] = index
    soullist[index]["num2"] = index+1
    try:
        soullist[index]["soul"] = reverse_souls[soul]
    except:
        soullist[index]["soul"] = soul
    soullist[index]["xp"] = 0 #65535 is too high but it already auto sets back to 0
    soullist[index]["level"] = 10 #10 is the highest (255 looks funny but it is weaker than 10 because of the way the game calculates soul stats)
    soullist[index]["used"] = 0
    return soullist

def edit_contact(contactlist, index, name=None, starred=None, ownerid=None, comment=None, favourite=None, game=None, face=None, hq=None, job=None, hobby=None, ambition=None, yokai=None): #can alse be used for profile
    try:
        if index < 0:
            index = len(contactlist)-index #appending shortcut (semi-redundant)
    except:
        pass
    dicti = False
    if isinstance(contactlist, dict): #for your profile
        dicti = True
        index = 0
        contactlist = [contactlist]
    else:
        try: #edited maxes to avoid overlapping text in-game
            contactlist[index]
        except:
            index = len(contactlist)
            contactlist.append({})
    if name != None:
        contactlist[index]["name"] = name
    if starred != None:
        contactlist[index]["name"] = starred #0 or 1
    if ownerid != None:
        contactlist[index]["ownerid"] = ownerid
    if comment != None:
        contactlist[index]["comment"] = comment
    if favourite != None:
        contactlist[index]["favourite"] = favourite #TODO compile a list of which value corresponds to which yokai
    contactlist[index]["bronze"] = 99 #255 35
    contactlist[index]["silver"] = 99 #255 30
    contactlist[index]["gold"] = 99 #255 15
    if game != None:
        contactlist[index]["game"] = game
    contactlist[index]["playtime"] = 4659.9997222222222 #999.9997222222222 ingame max
    contactlist[index]["tunnel"] = 9999999 #2147483647
    if face != None:
        contactlist[index]["face"] = face
    if hq != None:
        try:
            contactlist[index]["hq"] = hqs.index(hq)
        except:
            contactlist[index]["hq"] = hq
        contactlist[index]["hq"] = hq
    if job != None:
        try:
            contactlist[index]["job"] = jobs.index(job)
        except:
            contactlist[index]["job"] = job
    if hobby != None:
        try:
            contactlist[index]["hobby"] = hobbys.index(hobby)
        except:
            contactlist[index]["hobby"] = hobby
    if ambition != None:
        try:
            contactlist[index]["ambition"] = ambitions.index(ambition)
        except:
            contactlist[index]["ambition"] = ambition
    contactlist[index]["requests"] = 255
    contactlist[index]["arrested"] = 255
    contactlist[index]["medalium"] = 255 #technically 100 is max as it's a percentage
    contactlist[index]["bugs"] = 255
    contactlist[index]["fish"] = 255
    contactlist[index]["battles"] = 255
    contactlist[index]["battles"] = 255
    contactlist[index]["personal"] = 65535
    contactlist[index]["public"] = 9999 #65535
    contactlist[index]["rankl"] = 65535
    contactlist[index]["local"] = 99 #65535
    contactlist[index]["rankr"] = 65535
    contactlist[index]["random"] = 65535
    contactlist[index]["tagged"] = 65535
    contactlist[index]["photographs"] = 65535
    if yokai != None:
        contactlist[index]["yokai"] = yokai
    contactlist[index]["races"] = [.01,.01,.01,.01] #TODO could try 0.00001 so it shows as a 0 in the game
    if dicti:
        return contactlist[0]
    else:
        return contactlist


#main
def main(file): #TODO fix yokai.
    try:
        file = open(file, "r+b")
    except:
        import io
        file = io.BytesIO(file)
    with file as f:
        #money offset: 67808

        yokailist = []
        index = 0
        f.seek(20744) # 20744 is always yokai info location. 1 yokai takes up 92 bytes. offset same for all files. 00
        while True:
            yokai = f.read(92)
            if get(yokai, 0) == 0 and index != 0: #could be broken
                break

            yokailist.append({
                "num1": get(yokai, 0, 2), #0
                "num2": get(yokai, 2, 2), #2
                "id": get(yokai, 4, 4), #4-07
                "nickname": get(yokai, 8, 24, False), #8-32 maybe broken
                "attack": get(yokai, 42), #42
                "technique": get(yokai, 46), #46
                "soultimate": get(yokai, 50), #50
                "xp": get(yokai, 52, 4), #52 - 55
                "ownerid": get(yokai, 60, 4), #60 - 63
                "stats": { # 64 - 78
                    "IV_HP": get(yokai, 64), 
                    "IV_Str": get(yokai, 65), 
                    "IV_Spr": get(yokai, 66), 
                    "IV_Def": get(yokai, 67), 
                    "IV_Spd": get(yokai, 68), 
                    "CB_HP": get(yokai, 69), 
                    "CB_Str": get(yokai, 70), 
                    "CB_Spr": get(yokai, 71), 
                    "CB_Def": get(yokai, 72), 
                    "CB_Spd": get(yokai, 73), 
                    "SC_HP": get(yokai, 74), 
                    "SC_Str": get(yokai, 75), 
                    "SC_Spr": get(yokai, 76), 
                    "SC_Def": get(yokai, 77), 
                    "SC_Spd": get(yokai, 78)
                }, 
                "level": get(yokai, 79), #79
                "loaflevel": get(yokai, 84, half=True)[0], #84
                "attitude": get(yokai, 84, half=True)[0] #84 (shared byte)
            })

            index += 1
        original_yokai_amount = index

        #offset at the location "\xFE\x6D\x08\xFE\xFF\x00\x00\x03\x48\x24\x00\xFE\xFF" + 19th byte aka item location
        f.seek(0)
        offset = f.read(20744).index(b"\xFE\x6D\x08\xFE\xFF\x00\x00\x03\x48\x24\x00\xFE\xFF")+19 #certainly broken or at least bad

        itemlist = []
        index = 0
        f.seek(offset) # offset is item info location. 1 item takes up 12 bytes. 00
        while True:
            item = f.read(12)

            if get(item, 0) == 0 and index != 0: #could be broken
                break

            itemlist.append({
                "num1": get(item, 0, 2), #0
                "num2": get(item, 2, 2), #2
                "item": get(item, 4, 4), #4
                "amount": get(item, 8, 4) #8
            })

            index += 1
        original_item_amount = index

        equipmentlist = []
        index = 0
        f.seek(offset+5172) # offset + 5172 is equipment info location. 1 equipment takes up 16 bytes. 10
        while True:
            equipment = f.read(16)

            if get(equipment, 0) == 0 and index != 0: #could be broken
                break

            equipmentlist.append({
                "num1": get(equipment, 0, 1), #0
                "num2": get(equipment, 2, 2), #2
                "equipment": get(equipment, 4, 4), #4
                "amount": get(equipment, 8, 4), #8 #maybe 1 byte
                "used": get(equipment, 12, 4) #how many are in use (leave alone or set to zero)
            })

            index += 1
        original_equipment_amount = index

        importantlist = []
        index = 0
        f.seek(offset+6624) # offset + 6624 is important info location. 1 important takes up 8 bytes. 20
        while True:
            important = f.read(8)

            if get(important, 0) == 0 and index != 0: #could be broken
                break

            importantlist.append({
                "num1": get(important, 0, 2), #0
                "num2": get(important, 2, 2), #2 unsure.
                "important": get(important, 4, 4), #4
            })

            index += 1
        original_important_amount = index

        soullist = []
        index = 0
        f.seek(offset+8076) # offset + 8076 is soul info location. 1 soul takes up 12 bytes. 30
        while True:
            soul = f.read(12)

            if get(soul, 0) == 0 and index != 0: #could be broken
                break

            soullist.append({
                "num1": get(soul, 0, 1), #0
                "num2": get(soul, 2, 1), #2
                "soul": get(soul, 4, 4), #4
                "xp": get(soul, 8, 2), #8
                "level": get(soul, 10), #8
                "used": get(soul, 11) #11 true or false
            })

            index += 1
        original_soul_amount = index

        #extra stuff TODO add stuff like story progression
        f.seek(20744)
        postyokai = f.read() #for the stuff below that i commented out TODO
        unknown = postyokai.index(b"\xfe\xff\xd5\x08\x14\x90\x24\x00")+8+20744
        f.seek(unknown)  # this is your profile info location. your profile takes up 156 bytes
        contact = f.read(156)
        profile = { #name is stored in the head file (can decrypt head.yw as a yokai watch 1 save. may impliment in the future)
            "ownerid": get(contact, 0, 4),
            "comment": get(contact, 4, 64, False),
            "favourite": get(contact, 68, 4), #favourite yokai (by choice), TODO compile a list of which value corresponds to which yokai
            "bronze": get(contact, 72), #what medals they have
            "silver": get(contact, 73),
            "gold": get(contact, 74),
            "game": get(contact, 75),
            "playtime": get(contact, 76, 3)/3600, #in hours
            #00 inbetween
            "tunnel": get(contact, 80, 4),
            "face": get(contact, 84, 4), #can be a yokai or human, etc. TODO compile a list of which value corresponds to which yokai
            "hq": get(contact, 88),
            "job": get(contact, 89),
            "hobby": get(contact, 90),
            "ambition": get(contact, 91), 
            #00 inbetween
            "requests": get(contact, 93), #i can't remember what this is lol
            "arrested": get(contact, 94), #yo-criminals
            "medalium": get(contact, 95), #percentage
            "bugs": get(contact, 96),
            "fish": get(contact, 97),
            "battles": get(contact, 98),
            #something here?
            "personal": get(contact, 100, 2), #best tournament run, may have to remove ", 2"
            "public": get(contact, 102, 2), #best public tournament run
            "rankl": get(contact, 104, 2), #wether you're a beginner or master in local battles TODO look into this
            "local": get(contact, 106, 2), #local battle wins
            "rankr": get(contact, 108, 2),
            "random": get(contact, 110, 2),
            "tagged": get(contact, 112, 2),
            "photographs": get(contact, 114, 2),
            "yokai": [ #favourite yokai 1-6 (by playtime), TODO compile a list of which value corresponds to which yokai
                get(contact, 116, 4), #if it is a 0 then there is no yokai in the slot. (early game)
                get(contact, 120, 4),
                get(contact, 124, 4),
                get(contact, 128, 4),
                get(contact, 132, 4),
                get(contact, 136, 4)
            ],
            "races": [ #if it is a 0 then the race has not been completed. in minutes (floating point) displays in-game to two decimal places without rounding
                get(contact, 140, 4, None), #uptown springdale
                get(contact, 144, 4, None), #harrisville
                get(contact, 148, 4, None), #san fantastico
                get(contact, 152, 4, None), #(old) springdale
            ]
        }

        contactlist = []
        index = 0
        while True: # this is the contact info location. 1 contact takes up 184 bytes
            contact = f.read(184)

            if get(contact, 0) == 0:
                break

            contactlist.append({ #max 50 contacts
                "name": get(contact, 0, 25, False), #max length is 24 with a 00 on the end
                "starred": get(contact, 26), #true or false (1 or 0)
                #00 inbetween
                "ownerid": get(contact, 28, 4),
                "comment": get(contact, 32, 64, False),
                "favourite": get(contact, 96, 4), #favourite yokai (by choice), TODO compile a list of which value corresponds to which yokai
                "bronze": get(contact, 100), #what medals they have
                "silver": get(contact, 101),
                "gold": get(contact, 102),
                "game": get(contact, 103),
                "playtime": get(contact, 104, 3)/3600, #in hours
                #00 inbetween
                "tunnel": get(contact, 108, 4),
                "face": get(contact, 112, 4), #can be a yokai or human, etc. TODO compile a list of which value corresponds to which yokai
                "hq": get(contact, 116),
                "job": get(contact, 117),
                "hobby": get(contact, 118),
                "ambition": get(contact, 119), 
                #00 inbetween
                "requests": get(contact, 121), #i can't remember what this is lol
                "arrested": get(contact, 122), #yo-criminals
                "medalium": get(contact, 123), #percentage
                "bugs": get(contact, 124),
                "fish": get(contact, 125),
                "battles": get(contact, 126),
                #something here?
                "personal": get(contact, 128, 2), #best tournament run, may have to remove ", 2"
                "public": get(contact, 130, 2), #best public tournament run
                "rankl": get(contact, 132, 2), #wether you're a beginner or master in local battles TODO look into this
                "local": get(contact, 134, 2), #local battle wins
                "rankr": get(contact, 132, 2),
                "random": get(contact, 138, 2),
                "tagged": get(contact, 140, 2),
                "photographs": get(contact, 142, 2),
                "yokai": [ #favourite yokai 1-6 (by playtime), TODO compile a list of which value corresponds to which yokai
                    get(contact, 144, 4),
                    get(contact, 148, 4),
                    get(contact, 152, 4),
                    get(contact, 156, 4),
                    get(contact, 160, 4),
                    get(contact, 164, 4)
                ],
                "races": [ #if it is a 0 then the race has not been completed. in minutes (floating point)
                    get(contact, 168, 4, None), #uptown springdale
                    get(contact, 172, 4, None), #harrisville
                    get(contact, 176, 4, None), #san fantastico
                    get(contact, 180, 4, None), #(old) springdale
                ]
            })

            index += 1
        original_contact_amount = index

        # f.seek(postyokai.index(b"\xff\xfe\x6b\x08\xfe\xff")+20744) #!P & T ..... currently i have no idea what this is or how to use it. part of it is probably the medallium info & story progress
        # unknown1 = f.read(150) #138
        # # f.seek(postyokai.index(b"\xff\xfe\xd5\x08\xfe\xff\xd5\x08\x15")+20744) maybe this T
        # # unknown15 = f.read(10)
        # f.seek(postyokai.index(b"\xff\xfe\xd5\x08\xfe\xff\xd5\x08\x12")+20744) #N`
        # unknown2 = f.read(49)
        # f.seek(postyokai.index(b"\xff\xfe\xd5\x08\xfe\xff\xd5\x08\x0e\x00")+20744) #wArt
        # unknown3 = f.read(1036)
        # f.seek(postyokai.index(b"\xff\xfe\xd5\x08\xfe\xff\x00\x00\x08")+20744) #<==>
        # unknown4 = f.read(272)
        # f.seek(postyokai.index(b"\xff\xfe\x47\x08\xfe")+20744) #??@@AABBCCDD
        # unknown5 = f.read(1636)

        #editor goes here
        if 0:
            #to append yokai make index None. must include yokai, attitude & nickname if appending. (can all be "" except for yokai)
            #append a pandle
            yokailist = edit_yokai(yokailist, None, profile["ownerid"], "pandle", "", "bob") #if you get the index wrong it will mess everything up
            #change to a rough ake
            yokailist = edit_yokai(yokailist, -1, profile["ownerid"], "ake", "rough") #broken
            #append 60 milk
            itemlist = edit_item(itemlist, None, "milk", 65535) #currently broken, max is 255, 65535 or 99
            #append 60 cheap bracelet
            equipmentlist = edit_equipment(equipmentlist, None, "cheap bracelet", 65535) #255 works, testing 65535
            #append a swosh soul
            soullist = edit_soul(soullist, None, "snartle")

            importantlist = edit_important(importantlist, None, "hose")

            profile = edit_contact(profile, None)

        # #print data 
        # if 1:



        #write everything back to file
        if 0:
            #write items back
            j=0
            for i in itemlist:
                f.seek(offset+12*j)
                f.write(i["num1"].to_bytes(1, "little")) 
                f.seek(offset+12*j+2)
                f.write(i["num2"].to_bytes(2, "little"))
                f.seek(offset+12*j+4)
                f.write(i["item"].to_bytes(4, "little"))
                f.seek(offset+12*j+8)
                f.write(i["amount"].to_bytes(4, "little"))
                j+=1
            
            #clear item overflow
            if original_item_amount - len(itemlist) > 0: #TODO test if this works
                f.seek(offset+12*j)
                f.write(b"\x00"*12*(original_item_amount - len(itemlist)))
            
            #write equipment back
            j=0
            for i in equipmentlist:
                f.seek(offset+5172+16*j)
                f.write(i["num1"].to_bytes(2, "little"))
                f.seek(offset+5172+16*j+1)
                f.write(b"\x10") # i don't know what this does, may be unnecessary
                f.seek(offset+5172+16*j+2)
                f.write(i["num2"].to_bytes(2, "little"))
                f.seek(offset+5172+16*j+4)
                f.write(i["equipment"].to_bytes(4, "little"))
                f.seek(offset+5172+16*j+8)
                f.write(i["amount"].to_bytes(4, "little"))
                f.seek(offset+5172+16*j+12)
                f.write(i["used"].to_bytes(4, "little"))
                j+=1

            #clear equipment overflow
            if original_equipment_amount - len(equipmentlist) > 0: #TODO test if this works
                f.seek(offset+5172+16*j)
                f.write(b"\x00"*16*(original_equipment_amount - len(equipmentlist)))

            #write important back
            j=0
            for i in importantlist:
                f.seek(offset+6624+8*j)
                f.write(i["num1"].to_bytes(2, "little"))
                f.seek(offset+6624+8*j+1)
                f.write(b"\x20") # i don't know what this does, may be unnecessary
                f.seek(offset+6624+8*j+2)
                f.write(i["num2"].to_bytes(2, "little"))
                f.seek(offset+6624+8*j+4)
                f.write(i["important"].to_bytes(4, "little"))
                j+=1

            #clear important overflow
            if original_important_amount - len(importantlist) > 0: #TODO test if this works
                f.seek(offset+6624+8*j)
                f.write(b"\x00"*8*(original_important_amount - len(importantlist)))

            #write soul back
            j=0
            for i in soullist:
                f.seek(offset+8076+12*j)
                f.write(i["num1"].to_bytes(2, "little"))
                f.seek(offset+8076+12*j+1)
                f.write(b"\x30") # i don't know what this does, may be unnecessary
                f.seek(offset+8076+12*j+2)
                f.write(i["num2"].to_bytes(2, "little"))
                f.seek(offset+8076+12*j+4)
                f.write(i["soul"].to_bytes(4, "little"))
                f.seek(offset+8076+12*j+8)
                f.write(i["xp"].to_bytes(2, "little"))
                f.seek(offset+8076+12*j+10)
                f.write(i["level"].to_bytes(1, "little"))
                f.seek(offset+8076+12*j+11)
                f.write(i["used"].to_bytes(1, "little"))
                j+=1

            #clear soul overflow
            if original_soul_amount - len(soullist) > 0: #TODO test if this works
                f.seek(offset+8076+12*j)
                f.write(b"\x00"*12*(original_soul_amount - len(soullist)))

            #write yokai back
            j=0
            for i in yokailist:
                f.seek(20744+92*j)
                f.write(i["num1"].to_bytes(2, "little")) #no need to seek, may remove
                f.seek(20744+92*j+2)
                f.write(i["num2"].to_bytes(2, "little"))
                f.seek(20744+92*j+4)
                f.write(i["id"].to_bytes(4, "little"))
                f.seek(20744+92*j+8)
                f.write((bytearray([ord(k)for k in i["nickname"]])+bytearray(24))[:24]) # to be more accurate to game could just append
                f.seek(20744+92*j+42)
                f.write(i["attack"].to_bytes(1, "little"))
                f.seek(20744+92*j+46)
                f.write(i["technique"].to_bytes(1, "little"))
                f.seek(20744+92*j+50)
                f.write(i["soultimate"].to_bytes(1, "little"))
                f.seek(20744+92*j+52)
                f.write(i["xp"].to_bytes(4, "little"))
                f.seek(20744+92*j+60)
                f.write(i["ownerid"].to_bytes(4, "little"))
                statnum = 64
                for stat in i["stats"]:
                    f.seek(20744+92*j+statnum)
                    f.write(i["stats"][stat].to_bytes(1, "little"))
                    statnum +=1
                f.seek(20744+92*j+79)
                f.write(i["level"].to_bytes(1, "little"))
                f.seek(20744+92*j+84)
                f.write(int(f'{i["loaflevel"]:04b}'+f'{i["attitude"]:04b}', 2).to_bytes(1, "little"))
                j+=1

            #clear yokai overflow
            if original_yokai_amount - len(yokailist) > 0: #TODO test if this works
                f.seek(20744+92*j)
                f.write(b"\x00"*92*(original_yokai_amount - len(yokailist)))

            #write profile back (the beginning part of your contact list)
            f.seek(unknown)
            f.write(profile["ownerid"].to_bytes(4, "little"))
            f.write((bytearray([ord(k)for k in profile["comment"]])+bytearray(64))[:64])
            f.write(profile["favourite"].to_bytes(4, "little"))
            f.write(profile["bronze"].to_bytes(1, "little"))
            f.write(profile["silver"].to_bytes(1, "little"))
            f.write(profile["gold"].to_bytes(1, "little"))
            f.write(profile["game"].to_bytes(1, "little"))
            f.write(int(profile["playtime"]*3600).to_bytes(3, "little")) #may cause problems
            f.seek(unknown+80)
            f.write(profile["tunnel"].to_bytes(4, "little"))
            f.write(profile["face"].to_bytes(4, "little"))
            f.write(profile["hq"].to_bytes(1, "little"))
            f.write(profile["job"].to_bytes(1, "little"))
            f.write(profile["hobby"].to_bytes(1, "little"))
            f.write(profile["ambition"].to_bytes(1, "little"))
            f.seek(unknown+93)
            #00 inbetween
            f.write(profile["requests"].to_bytes(1, "little"))
            f.write(profile["arrested"].to_bytes(1, "little"))
            f.write(profile["medalium"].to_bytes(1, "little"))
            f.write(profile["bugs"].to_bytes(1, "little"))
            f.write(profile["fish"].to_bytes(1, "little"))
            f.write(profile["battles"].to_bytes(1, "little"))
            f.seek(unknown+100)
            #something here?
            f.write(profile["personal"].to_bytes(2, "little")) #may have to rename this
            f.write(profile["public"].to_bytes(2, "little"))
            f.write(profile["rankl"].to_bytes(2, "little")) #ffff = master, 0000 = beginner
            f.write(profile["local"].to_bytes(2, "little"))
            f.write(profile["rankr"].to_bytes(2, "little")) #120 >= master (maybe less)
            f.write(profile["random"].to_bytes(2, "little"))
            f.write(profile["tagged"].to_bytes(2, "little"))
            f.write(profile["photographs"].to_bytes(2, "little"))
            for k in profile["yokai"]:
                f.write(k.to_bytes(4, "little"))
            for k in profile["races"]:
                f.write(give(k))

            #no need to clear profile overflow as it can't be deleted

            #write contact back
            j=0
            for i in contactlist:
                f.write((bytearray([ord(k)for k in i["name"]])+bytearray(25))[:25])
                f.write(i["starred"].to_bytes(1, "little"))
                f.seek(unknown+156+184*j+28)
                f.write(i["ownerid"].to_bytes(4, "little"))
                f.write((bytearray([ord(k)for k in i["comment"]])+bytearray(64))[:64])
                f.write(i["favourite"].to_bytes(4, "little"))
                f.write(i["bronze"].to_bytes(1, "little"))
                f.write(i["silver"].to_bytes(1, "little"))
                f.write(i["gold"].to_bytes(1, "little"))
                f.write(i["game"].to_bytes(1, "little"))
                f.write(int(i["playtime"]*3600).to_bytes(3, "little")) #may cause problems
                f.seek(unknown+156+184*j+108)
                f.write(i["tunnel"].to_bytes(4, "little"))
                f.write(i["face"].to_bytes(4, "little"))
                f.write(i["hq"].to_bytes(1, "little"))
                f.write(i["job"].to_bytes(1, "little"))
                f.write(i["hobby"].to_bytes(1, "little"))
                f.write(i["ambition"].to_bytes(1, "little"))
                f.seek(unknown+156+184*j+121)
                #00 inbetween
                f.write(i["requests"].to_bytes(1, "little"))
                f.write(i["arrested"].to_bytes(1, "little"))
                f.write(i["medalium"].to_bytes(1, "little"))
                f.write(i["bugs"].to_bytes(1, "little"))
                f.write(i["fish"].to_bytes(1, "little"))
                f.write(i["battles"].to_bytes(1, "little"))
                f.seek(unknown+156+184*j+128)
                #something here?
                f.write(i["personal"].to_bytes(2, "little"))
                f.write(i["public"].to_bytes(2, "little"))
                f.write(i["rankl"].to_bytes(2, "little")) #ffff = master, 0000 = beginner
                f.write(i["local"].to_bytes(2, "little"))
                f.write(i["rankr"].to_bytes(2, "little")) #120 >= master (maybe less)
                f.write(i["random"].to_bytes(2, "little"))
                f.write(i["tagged"].to_bytes(2, "little"))
                f.write(i["photographs"].to_bytes(2, "little"))
                for k in i["yokai"]:
                    f.write(k.to_bytes(4, "little"))
                for k in i["races"]:
                    f.write(give(k))
                j+=1

            #clear contact overflow
            if original_contact_amount - len(contactlist) > 0: #TODO test if this works
                f.seek(unknown+156+184*j)
                f.write(b"\x00"*184*(original_contact_amount - len(contactlist)))
                
        f.seek(0)
        return f.read() #for the .yw files


infile = "/Volumes/3DS/3ds/Checkpoint/saves/0x01B28 YO-KAI WATCH 2  PSYCHIC …/20230410-142023/game1.yw"

if infile[-3:] == "ywd":
    main(infile)
else:
    from pathlib import Path
    import sys
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent)+"/save-tools") #TODO make nicer
    except:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent)+"\\save-tools")
    import yw_save
    with open(infile, "r+b") as f:
        if 0:
            with open(infile+"b", "r+b") as g: #TODO fix backup system
                g.write(f.read())
                f.seek(0)
        out = main(yw_save.yw2_proc(f.read(), False, head=infile[-1::-1].split("/",1)[1][-1::-1]+"head.yw")) #out is the edited binary data
        f.seek(0)
        f.write(yw_save.yw2_proc(out, True, head=infile[-1::-1].split("/",1)[1][-1::-1]+"head.yw"))