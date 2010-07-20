from time import * 
from bb_udp import * 
from os.path import isfile 
import sys 
thedataz = ["The Log ID's Are: \n", "\nThe data: "]
theid = 0
def upid():
    global theid
    theid = theid + 1
def logto(tag, data, startime):
    thedataz.append("\n#ID: "+ str(theid) +"\n---------\nTag: " + str(tag) + "\n" + "Log Data: " + str(data) + "\n" + "Time: "+ str(time() - startime) + "\n---------\n")
    thedataz[0]= thedataz[0] + ("# "+str(theid)+" => "+str(tag) + ", \n")
    upid()
def startid(typ, data, ishandled, startime):
    if not typ == 0 and not typ == 255:
        if ishandled:
            hand = "Handled"
        else:
            hand = "Not Handled"
        thedataz.append("\n#ID: "+ str(theid) +"\n#########\nPacket Type: " + str(typ) + " is " + hand + "\nProcessed Data: " + handle(typ, data) + "\n" + "Time: "+ str(time() - startime) + "\n#########\n")
        upid()
def endid():
    datafile = open('datafile.txt', "w+")
    thedata = [ (line + "\n") for line in thedataz ]
    datafile.writelines(thedata)
    datafile.close()
def handle(typ , udp):

    if typ == 1:
        return "Foreign Server... Ignoring Message"
    elif typ == 10:
        ID = ReadByte(udp)
        rses = ReadByte(udp)
        return "Shoot from " + str(ID) + ": rses = " + str(rses)
    elif typ == 11:
        ID = ReadByte(udp)
        wepmode = ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "Weaponmode from: " + str(ID) + " weapon = " + str(wepmode) + " and limp = " + str(limp)
    elif typ == 12:
        rses = ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:

            return "ShootImp Rses from: " + str(rses) + " limp = " + str(limp)
    elif typ == 13:
        damage = ReadByte(udp)
        for i in range(1, damage):
            i
        wepID = ReadByte(udp)
        wepmode = ReadByte(udp)

        rses = ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:

            return "Shoot+Hit Rses from: " + str(rses) + " limp = " + str(limp) + ", wepId= " + str(wepID) + ", wepmode= " + str(wepmode) + ", and damagecount = " + str(damage)
    elif typ == 15:
        ID = ReadByte(udp)
        x = ReadInt(udp)
        y = ReadInt(udp)
        rses = ReadByte(udp)
        return "Position from: " + str(ID)  + " x= " + str(x) + ", y= " + str(y) + ", and rses = " + str(rses)
    elif typ == 16:
        ID = ReadByte(udp)            
        dir = (ReadShort(udp)-32767)    
        return "Direction from: " + str(ID)  + " dir= " + str(dir)
    elif typ == 20:
        ID=ReadByte(udp)            
        xdif=(ReadByte(udp)-128)        
        ydif=(ReadByte(udp)-128)        
        return "Move from: " + str(ID)  + " xdif= " + str(xdif) + " and ydif= " + str(ydif) 
    elif typ == 21:
        ID=ReadByte(udp)            
        xdif=(ReadByte(udp)-128)        
        ydif=(ReadByte(udp)-128)        
        return "Walk from: " + str(ID)  + " xdif= " + str(xdif) + " and ydif= " + str(ydif)
    elif typ == 22:
        ID=ReadByte(udp)            
        xdif=(ReadByte(udp)-128)        
        ydif=(ReadByte(udp)-128)        
        dir=(ReadShort(udp)-32767)    
        return "MoveDir from: " + str(ID)  + " xdif= " + str(xdif) + " and ydif= " + str(ydif) + " and dir= " + str(dir)
    elif typ == 23:
        ID=ReadByte(udp)            
        xdif=(ReadByte(udp)-128)        
        ydif=(ReadByte(udp)-128)        
        dir=(ReadShort(udp)-32767)    
        return "WalkDir from: " + str(ID)  + " xdif= " + str(xdif) + " and ydif= " + str(ydif) + " and dir= " + str(dir)
    elif typ == 30:
        ID=ReadByte(udp)
        wep1=ReadByte(udp)
        wep2=ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "WepSelect from: " + str(ID)  + " wep1= " + str(wep1) + " and wep2= " + str(wep2) + " and limp= " + str(limp)
    elif typ == 31:
        ID=ReadByte(udp)
        slot=ReadByte(udp)
        item=ReadByte(udp)
        ammo=ReadInt(udp)
        ammoin=ReadInt(udp)
        x=ReadInt(udp)
        y=ReadInt(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "Drop from: " + str(ID)  + " slot= " + str(slot) + " item= " + str(item) + " ammo= " + str(ammo) + " ammoin= " + str(ammoin) + " x= " + str(x) + " y= " + str(y) + " and limp= " + str(limp)
    elif typ == 32:
        ID=ReadByte(udp)
        item=ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else: 
            return "Buy from: " + str(ID)  + " item= " + str(item) + " and limp= " + str(limp)
    elif typ == 33:
        ID=ReadByte(udp)
        act=ReadByte(udp)
        mode=ReadByte(udp)
        rses=ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "Action from: " + str(ID)  + " action= " + str(act)  + " mode= " + str(mode)  + " rses= " + str(rses) + " and limp= " + str(limp)
    elif typ == 34:
        ID=ReadByte(udp)
        item=ReadByte(udp)
        x=ReadInt(udp)
        y=ReadInt(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "Collect from: " + str(ID) + " item= " + str(item) + " x= " + str(x) + " y= " + str(y) + " and limp= " + str(limp)
    elif typ == 40:
        ID=ReadByte(udp)
        hurter=ReadByte(udp)
        power=ReadByte(udp)
        weapon=ReadByte(udp)
        armor=ReadByte(udp)
        rses=ReadByte(udp)
        return "Hurt from: " + str(ID) + " By= " + str(hurter) + " power= " + str(power) + " weapon= " + str(weapon) + "  armor= " + str(armor)+ " and rses= " + str(rses)
    elif typ == 41:
        ID=ReadByte(udp)
        killer=ReadByte(udp)
        rses=ReadByte(udp)
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "Kill from: " + str(ID) + " By= " + str(killer) + " rses= " + str(rses)+ " limp= " + str(limp)
    elif typ == 42:
        ID=ReadByte(udp)
        health=ReadByte(udp)
        armor=ReadByte(udp)
        rses=ReadByte(udp)
        return "Health from: " + str(ID) + " Health= " + str(health) + " armor= " + str(armor)+ " rses= " + str(rses)
    elif typ == 50:
        ID=ReadByte(udp)            
        gID=ReadByte(udp)            
        x=ReadInt(udp)            
        y=ReadInt(udp)            
        dir=ReadInt(udp)            
        type=ReadByte(udp)            
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "Grenade from: " + str(ID)  + " gID= " + str(gID) + " x= " + str(x) + " y= " + str(y) + " dir= " + str(dir) + " type= " + str(type) + " and limp= " + str(limp)
    elif typ == 51:
        gID=ReadByte(udp)
        x=ReadInt(udp)            
        y=ReadInt(udp)            
        type=ReadByte(udp)            
        ID=ReadByte(udp)            
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:
            return "GrenadeExplode from: " + str(ID)  + " gID= " + str(gID) + " x= " + str(x) + " y= " + str(y) + " type= " + str(type) + " and limp= " + str(limp)
    elif typ == 60:
        return "Hostage Data"
    elif typ == 61:
        return "Hostage Damage"
    elif typ == 62:
        return "Hostage Kill"
    elif typ == 63:
        return "Hostage Rescue"
    elif typ == 90:
        ID=ReadByte(udp)             
        x=ReadInt(udp)             
        y=ReadInt(udp)             
        file=ReadLine(udp)            
        rses=ReadByte(udp)            
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:    
            return "SprayLogo from: " + str(ID)  + " x= " + str(x) + " y= " + str(y) + " file= " + str(file) + " rses= " + str(rses)+ " and limp= " + str(limp)
    elif typ == 91:
        type=ReadByte(udp)            
        ID=ReadByte(udp)             
        msg=ReadLine(udp)            
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:            
            return "SayMsg from: " + str(ID)  + " type= " + str(type) + " msg= " + str(msg) + " and limp= " + str(limp)

    elif typ == 92:
        ID=ReadByte(udp)            
        radio=ReadByte(udp)            
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:            
            return "Radio from: " + str(ID)  + " radio= " + str(radio) + " and limp= " + str(limp)
    elif typ == 93:
        ID=ReadByte(udp)            
        name=ReadLine(udp)            
        limp = ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:            
            return "NameChange from: " + str(ID)  + " name= " + str(name) + " and limp= " + str(limp)
    elif typ == 94:
        ID=ReadByte(udp)
        name=ReadLine(udp)            
        frags=ReadShort(udp)            
        deads=ReadShort(udp)            
        admin=ReadByte(udp)            
        return "NameChange from: " + str(ID)  + " name= " + str(name) + " frags= " + str(frags)+ " deads= " + str(deads)+ " and admin= " + str(admin)
    elif typ == 230:
        return "Cheat Detection kicked someone..."
    elif typ == 100:
        id=ReadByte(udp)
        name=ReadLine(udp)    
        team=ReadByte(udp)
        look=ReadByte(udp)
        vip=ReadByte(udp)
        ip=ReadInt(udp)
        port=ReadInt(udp)
        health=ReadByte(udp)
        x=ReadInt(udp)
        y=ReadInt(udp)
        dir=ReadShort(udp)
        frags=(ReadShort(udp)-32767)
        deads=(ReadShort(udp)-32767)
        sweapon1=ReadByte(udp)
        sweapon2=ReadByte(udp)
        gameadmin=ReadByte(udp)
        limp=ReadShort(udp)
        if limprep(limp) == 1:
            return "Duplication"
        else:        
            return "Player: ID=" + str(id) + " name = " + str(name) + " team = " + str(team) + " look = " + str(look) + " vip = " + str(vip) + " ip = " + str(ip)+ " port = " + str(port)+ " health = " + str(health)+ " x = " + str(x)+ " y = " + str(y)+ " dir = " + str(dir)+ " frags = " + str(frags)+ " deads = " + str(deads)+ " sweapon1 = " + str(sweapon1)+ " sweapon2 = " + str(sweapon2)+ " gameadmin = " + str(gameadmin) + " and limp=" +str(limp)
    elif typ == 251:
        #server.sendto(WriteByte(251), addr)
        return "Ping"
    elif typ == 253:
        ID=ReadByte(udp)
        ping=ReadInt(udp)
        #server.sendto(WriteByte(251), addr)
        return "OPing From :" + str(ID) + " is " + str(ping)
    else:
        return "Not Yet Implemented: " + udp
def limprep(limp):
    try:
        #a = limpz[limp]
        return 0
    except:
        #limpz[limp] = '1'
        return 0