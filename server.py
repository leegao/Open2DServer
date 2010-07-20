from socket import * 
from time import * 
from bb_udp import * 
from map import * 
from weapons import * 
from select import select 
from urllib import urlopen 
from random import randint, shuffle 
from os.path import isfile 
from math import cos, sin, radians 
from re import compile 
from packetid import *
import dis
import sys 
import atexit 
import threading
sys.stderr = open("debug.txt", "w+")
#sys.stdout = open("data.txt", "w+")
startime = time()
usgn = 0
running = 0
usgnhost = "http://usgn.unrealsoftware.de/game_cs2d/"
settings = {"Svname": "Cs2d Server",
 "Svport": 36963,
 "Svpw": "",
 "Svmaxpl": 32,
 "Svfow": 1,
 "Svwm": 0,
 "Svff": 0,
 "Svac": 1,
 "Svmap": "de_dust",
 "Svispw": 0,
 "version": "b 0.1.0.4",
 "Svfragslimit": 100,
 "Svmaxrounds": 10,
 "Svtimelimit": 30,
 "timeout": 30,
 "Svwelcome": "",
 "Svrestarttimer": 5,
 "Svstartmoney": 800,
 "Svroundtime": 5,
 "Svmaxping": 200,
 "Svbombtimer": 35,
 "Svautoteam": 1,
 "Svupr": 1000,
 "Svremote": "",
 "Svlastmove": 0.0,
 "Svhostagemaxmove": 10,
 "Svantilag": 0,
 "Svusgnregister": 0.0,
 "Svbind": ""}
cfgs = {"sv_name": "Svname",
 "sv_port": "Svport",
 "sv_password": "Svpw",
 "sv_maxpl": "Svmaxpl",
 "sv_maxplayers": "Svmaxpl",
 "sv_fow": "Svfow",
 "sv_wm": "Svwm",
 "sv_warmode": "Svwm",
 "sv_ff": "Svff",
 "map": "Svmap",
 "mp_fragslimit": "Svfragslimit",
 "mp_maxrounds": "Svmaxrounds",
 "mp_timilimit": "Svtimelimit",
 "sv_welcome": "Svwelcome",
 "sv_autoteambalance": "Svautoteam",
 "sv_uprate": "Svupr",
 "sv_timeout": "timeout",
 "sv_pinglimit": "Svmaxping",
 "sv_remotepw": "Svremote",
 "sv_roundtime": "Svroundtime",
 "sv_lastmove": "Svlastmove",
 "sv_antilag": "Svantilag",
 "sv_usgnregister": "Svusgnregister",
 "sv_bind": "Svbind"}
player = {}
ids = {}
ban = []
slotreservation = []
updater = {"startround": 1}
game = {"roundstart": 0,
 "ct_score": 0,
 "t_score": 0,
 "ct_winrow": 0,
 "t_winrow": 0,
 "bombstart": 0,
 "bombtimer": 0,
 "round": 0,
 "restartmode": 0,
 "bombx": 0,
 "bomby": 0,
 "bombplanter": 0,
 "vipid": 0,
 "usgnregister": 0}
ip = ""
log = ""
sends = []
limp = 0
impsends = {}
pingids = []
map_dir = "maps/"
map_header = "Unreal Software's Counter-Strike 2D map_ File"
map_check = "ed.erawtfoslaernu"
grenades = {}

class Serv(threading.Thread):
    def __init__(self, infile, addr):
        threading.Thread.__init__(self)        
        self.infile = infile
        self.addr = addr
    def run(self):
        data = self.infile
        handler(data, self.addr)
botact = {"move":0}
botstop = 0
class Bot(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)        
        self.addr = addr
    def run(self):
        id = self.addr[1]
        global ids
        global player
        global game
        global botstop
        distance = {}
        while 1:
            frametime = time()
            if botstop == 1:
                break
            if botact['move'] != 0:
                sendall((((WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine('Bot' + "Says: e.....")), imp = 1)
                priority = 0
                pos_prio = []
                pl = player[ids[botact['move']]]
                #if player[ids[id]]['team'] != pl['team']and pl['ip'] != addre[0] and pl['playing']:
                distance[pl['ID']] = ((pl['x'] - player[ids[id]]['x'])**2 + (pl['y'] - player[ids[id]]['y'])**2)**(0.5)
                print "qualified"
                if distance[pl['ID']] <= 100:
                    pos_prio.append(pl['ID'])
                    print 'posId'
                #botact['move'] = 0
            
            sleep(((1 / float(settings["Svupr"])) - frametime))

def cfgsplitter(cfg):
    cfg = compile('\n(\\w+)\\s+([\\w.]+)|\n(\\w+)\\s+"([^"^\n]+)"').findall(cfg)
    commands = {}
    for (com1, para1, com2, para2,) in cfg:
        if (com1 != ""):
            commands[com1.lower()] = para1
        else:
            commands[com2.lower()] = para2

    return commands



def parser(cfg):
    commands = cfgsplitter(cfg)
    for (com, para,) in commands.items():
        log4 = ""
        if (com in cfgs):
            if (type(settings[cfgs[com]]) == type(0)):
                settings[cfgs[com]] = int(para)
            elif (type(settings[cfgs[com]]) == type(0.0)):
                settings[cfgs[com]] = float(para)
            else:
                settings[cfgs[com]] = para
            log4 += (((("+ " + com) + " = '") + para) + "'")
            if (log4 != ""):
                add(log4, 0, 0)

    if (len(settings["Svpw"]) > 0):
        settings["Svispw"] = 1



def load():
    add("Loading Settings:", 1, 0)
    if isfile("config.cfg"):
        config = open("config.cfg", "r")
        cfgs = config.read()
        config.close()
        parser(cfgs)
    if isfile("banlist.txt"):
        banlist = open("banlist.txt", "r")
        bans = banlist.readlines()
        banlist.close()
        for line in bans:
            line = line.replace("\n", "")
            add(("- Banned: " + line), 0, 0)
            ban.append(line)

    if isfile("slotreservation.txt"):
        banlist = open("slotreservation.txt", "r")
        bans = banlist.readlines()
        banlist.close()
        for line in bans:
            line = line.replace("\n", "")
            add(("# Slot reservated for: " + line), 0, 0)
            slotreservation.append(line)




def add(string, priority = 0, logtime = 1):
    if (priority == 1):
        string = (("*** " + string) + " ***")
    elif (priority == 2):
        string = (("!!! " + string) + " !!!")
    if logtime:
        string = ((((((("[" + str(localtime()[3])) + ":") + str(localtime()[4])) + ":") + str(localtime()[5])) + "] ") + string)
    print string



def start():
    global ip
    global addre
    global usgn
    global running
    global server
    if (usgn == 0):
        if (settings["Svusgnregister"] and (register() == 0)):
            add("Server couldn't register on USGN", 1, 0)
        elif settings["Svusgnregister"]:
            usgn = 1
            add((((("Server is registered in the USGN (" + ip) + ":") + str(settings["Svport"])) + ")"), 1, 0)
        elif settings["Svbind"]:
            ip = settings["Svbind"]
        if (not ip):
            ip = "127.0.0.1"
    else:
        add("Server is already on USGN registered", 1, 0)
    if (running == 0):
        try:
            server = socket(AF_INET, SOCK_DGRAM)
            server.setblocking(0)
            if settings["Svbind"]:
                addre = (settings["Svbind"],
                 int(settings["Svport"]))
            else:
                addre = (gethostname(),
                 int(settings["Svport"]))
            server.bind(addre)
            running = 1
            add("Server has been Started", 1, 0)
            return 1
        except:
            running = 0
            add("Server couldn't start", 1, 0)
            return 0
    else:
        add("Server is currently running", 1, 0)



def quit():
    global running
    global usgn
    global botstop
    endid()
    if isfile("banlist.txt"):
        banlist = open("banlist.txt", "w+")
        bans = [ (line + "\n") for line in ban ]
        banlist.writelines(bans)
        banlist.close()
    if (usgn == 1):
        if (shutdown() == 0):
            add("Server couldn't delete from USGN", 1, 0)
        else:
            usgn = 0
            add("Server deleted from USGN", 1, 0)
    else:
        add("Server is currently not registered on USGN", 1, 0)
    if (running == 1):
        try:
            running = 0
            server.close()
            add("Server has been closed", 1, 0)
        except:
            add("Server couldn't quit", 1, 0)
    else:
        add("Server is currently not running", 1, 0)



def key():
    add = ip.split(".")
    key = (((((int(add[0]) * 3) + (int(add[1]) * 8)) - int(add[2])) + (int(add[3]) * 5)) - 9346)
    return key



def register():
    global ip
    try:
        ip = urlopen(((usgnhost + "sv_save.php?game=Counter-Strike%202D&port=") + str(settings["Svport"]))).read()[2:]
        game["usgnregister"] = (time() + (settings["Svusgnregister"] * 3600))
        return 1
    except:
        return 0



def shutdown():
    try:
        urlopen(((((usgnhost + "sv_kill.php?game=Counter-Strike%202D&ip=") + ip) + "&key=") + str(key())))
        return 1
    except:
        return 0



def run():
    while (running == 1):
        frametime = time()
        (read, write, error,) = select([server], [server], [server])
        if (server in read):
            try:
                (data, addr,) = server.recvfrom(128)
            except KeyboardInterrupt:
                raise "KeyboardInterrupt"
            except:
                add("3rr0r during receiving data!", 1)
            try:
                handle = Serv(data, addr)
                handle.start()
                #handle.join()
                #handler(data, addr)
            except KeyboardInterrupt:
                raise "KeyboardInterrupt"
            except:
                add("3rr0r during handling data!", 1)
        try:
            resendimp()
        except KeyboardInterrupt:
            raise "KeyboardInterrupt"
        except:
            add("3rr0r during resending important data!", 1)
        try:
            update()
        except KeyboardInterrupt:
            raise "KeyboardInterrupt"
        except:
            add("3rr0r during updating data!", 1)
        if (server in write):
            send()
        frametime = (time() - frametime)
        if (frametime <= (1 / float(settings["Svupr"]))):
            sleep(((1 / float(settings["Svupr"])) - frametime))

    server.close()
    add("Server has been closed", 1)



def handler(data, addr):
    ans = ''
    if player.has_key(addr):
        prefix = addr[0]+'(#' + str(player[addr]['ID']) + ', ' + player[addr]['name'] + '): '
    else:
        prefix = addr[0] + ': '
    log4 = ''
    byte = ReadByte(data)
    ishandled = 1
    if addr[0] == 607:
        print "bots"
        return 0
    if not player.has_key(addr):
        if not byte == 250:
              log4 = 'Unauthorized access blocked(' + str(byte) + ')'
              return 0
    if byte:  
        if byte == 250:
            byte = ReadByte(data)
            if byte == 0: 
                ans = ans + ( ( ( ( ( ( ( ( ( WriteByte(250) + WriteByte(1)) + WriteLine(settings['Svname'])) + WriteByte(settings['Svispw'])) + WriteLine(settings['Svmap'])) + WriteByte(len(ids))) + WriteByte(settings['Svmaxpl'])) + WriteByte(settings['Svfow'])) + WriteByte(settings['Svwm'])) + WriteLine(settings['version']))
                sendone(addr, ans)
            elif byte == 250:
                pw = ReadLine(data)
                name = ReadLine(data)
                ip = DottedIP(ReadInt(data))
                port = ReadInt(data)
                ans = WriteByte(250) + WriteByte(3)
                if pw != settings['Svpw']:
                    if addr[0] not in slotreservation: 
                        log4 = log4 + 'Join Request -> wrong pw'
                        ans = ans + WriteByte(2) 
                elif len(player) >= settings['Svmaxpl']:
                    if addr[0] not in slotreservation: 
                        log4 = log4 + 'Join Request -> Server Full'
                        ans = ans + WriteByte(3) 
                elif addr[0] in ban: 
                    if addr[0] not in slotreservation: 
                        log4 = log4 + 'Join Request -> player banned'
                        ans = ans + WriteByte(4)
                else:
                    if player.has_key(addr):
                        kill(addr) 
                    temp_ids = ids.keys()
                    id_ = 1
                    while id_ in temp_ids: 
                        id_ = id_ + 1
                    
                    player[addr] = {"name": name,
                        "ID": id_,
                        "ip": addr[0],
                        "port": addr[1],
                        "timeout": time(),
                        "money": 0,
                        "roundlived": -1,
                        "ping": 0,
                        "team": 0,
                        "look": 0,
                        "vip": 0,
                        "x": 0,
                        "y": 0,
                        "dir": 0,
                        "health": 0,
                        "frags": 32767,
                        "deads": 32767,
                        "sweapon": ([0] * 18),
                        "sammo": ([0] * 18),
                        "sammoin": ([0] * 18),
                        "gameadmin": 0,
                        "ready": 0,
                        "slot": 0,
                        "ammor": 0,
                        "ping": 0,
                        "playing": 0,
                        "lastmove": time(),
                        "lastping": time(),
                        "hostages": []}
                    ids[id_] = addr
                    ans = ans + ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (  WriteByte(1)) + WriteByte(id_)) + WriteInt(IntIP(player[addr]['ip']))) + WriteInt(player[addr]['port'])) + WriteLine("b 0.1.0.4")) + WriteLine(map_['code'])) + WriteLine(settings['Svmap'])) + WriteByte(0)) + WriteLine(settings['Svname'])) + WriteByte(settings['Svmaxpl'])) + WriteByte(settings['Svfow'])) + WriteByte(settings['Svwm'])) + WriteByte(game['round'])) + WriteByte(game['round'])) +WriteShort(game['t_score'])) + WriteShort(game['ct_score'])) + WriteByte(game['t_winrow'])) + WriteByte(game['ct_winrow'])) +WriteInt(game['bombtimer'])) + WriteByte(1))
                sendone(addr, ans) 
            elif byte == 4: 
                name = ReadLine(data)
                id_ = ReadByte(data)
                
                if id_ in ids: 
                    for pl in player.values(): 
                        
                        if pl['ID'] != id_: 
                            ans = ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( WriteByte(100) + WriteByte(pl['ID'])) + WriteLine(pl['name'])) + WriteByte(pl['team'])) + WriteByte(pl['look'])) + WriteByte(pl['vip'])) + WriteInt(IntIP(pl['ip']))) + WriteInt(pl['port'])) + WriteByte(pl['health'])) +WriteInt(pl['x'])) + WriteInt(pl['y'])) +WriteShort(pl['dir'])) + WriteShort((pl['frags']))) + WriteShort((pl['deads']))) + WriteByte(pl['sweapon'][7])) + WriteByte(pl['sweapon'][8])) + WriteByte(pl['gameadmin']))
                            sendone(addr, ans, imp = 1)
                            ans =( ( ( (WriteByte(101) + WriteLine(name)) + WriteInt(IntIP(player[addr]['ip'])))+ WriteInt(addr[1])) + WriteByte(id_))
                            sendone((pl['ip'],pl['port']), ans, imp = 1)
                            ans = (((WriteByte(30)+WriteByte(pl['ID']))+WriteByte(pl['slot'])) + WriteByte(pl['sweapon'][pl['slot']]))
                            sendone(addr, ans, imp = 1)
                    ans = ( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine(settings['Svwelcome']))
                    sendone(addr, ans, imp = 1)
                    log4 = log4 + 'Joined as ' + name
            elif byte == 5:
                log4 = log4 + "Couldn't Join"
                kill(addr) 
            elif byte == 6:
                log4 = log4 + 'item data (250:6)'
            elif byte == 7:
                log4 = log4 + 'broken (250:7)' 
    
        elif byte == 251:
            sendone(addr, WriteByte(251))
            sendone(addr, ( ( WriteByte(253) + WriteByte(player[addr]['ID'])) + WriteInt(player[addr]['ping'])))
        elif byte == 252: 
            
            mode = ReadByte(data)
            id_ = ReadByte(data)
            impid = ReadShort(data)
            if mode == 0 and checkid(addr, id_):
                if addr in player and player[addr]['ID'] == id_:
                    log4 = log4 + "Left the game"
                    impsend(addr, impid)
                    kill(addr)
                    sendall(((WriteByte(252)+WriteByte(0))+WriteByte(id_)),ids_=[id_], imp=1 )       
            elif mode == 1:
                    log4 = log4 + "Pinged Out"
                    impsend(addr, impid)
                    kill(addr)
                    sendall(((WriteByte(252)+WriteByte(1))+WriteByte(id_)),ids_=[id_], imp=1 )
                    
        elif byte == 253: 
            id_ = ReadByte(data)
            ping = ReadInt(data)
            if not checkid(addr, id_):
                log4 = log4 + 'HAcker Attack: PingData'
        elif byte == 255: 
            msgid = ReadShort(data)
            if impsends.has_key(msgid): 
                if msgid in pingids: 
                    ping = int(((time() - impsends[msgid][2]) + 1) * 1000)
                    if settings['Svmaxping']:
                        if player[addre]['ping'] >= settings["Svmaxping"]:
                            if ping >= settings["Svmaxping"]:
                                sendall(((WriteByte(252) + WriteByte(2)) + WriteByte(player[addre]['ID'])), imp = 1)
                                add(player[addre]["name"] + ": Kicked (Too High Ping)")
                                kill(addre)
                        else:
                            player[addr]['ping'] = ping
                            sendall(( ( WriteByte(253) + WriteByte(player[addr]['ID'])) + WriteInt(player[addr]['ping'])))
                            pingids.remove(msgid) 
                            del impsends[msgid] 
        elif byte == 10:
            id_ = ReadByte(data)
            round = ReadByte(data)
            if not checkid(addr, id_):
                log4 = log4 + "Hacker Attack: Shoot"
            else:
                if player[addr]['slot'] == 2:
                    for addr_ in player:
                        if player[addr]['dir'] >= 0:
                            
                            dir = (player[addr]['dir'] - 32767)
                            richtung = (sin(radians(dir)), (-cos(radians(dir))))
                            distance = 4
                            stutzpunkt = ((player[addr]['x']+16),(player[addr]['x']+16))
                            collision = ((stutzpunkt[0]+(richtung[0]*distance)),(stutzpunkt[1]+(richtung[1]*distance)))
                            if collision[0] <= (player[addr_]['x']+48) and collision[0] >= (player[addr_]['x'] + 16) and collision[1] <= (player[addr_]['y']+48) and collision[1] >= (player[addr_]['y'] + 16) and addr != addr_ and player[addr]['health'] != 0 and player[addr_]['health'] != 0:
                                if settings['Svff'] or player[addr]['team'] != player[addr_]['team']:
                                    power = (weapon_damage[50]/3)
                                    if player[addr_]['armor'] == 0:
                                        player[addr_]['health'] = player[addr_]['health'] - power
                                    elif player[addr_]['armor'] < 150:
                                        player[addr_]['health'] = int(player[addr_]['health']-(0.65*power))
                                    if player[addr_]['armor'] > 0:
                                        player[addr_]['armor'] = player[addr_]['armor'] - power
                                        if player[addr_]['armor'] < 0:
                                            player[addr_]['armor'] = 0
                                    log("shootHit", 496, player[addr_])
                                    if player[addr_]['health'] <= 0 and player[addr_]['playing']:
                                        player[addr_]['health'] = 100
                                        player[addr_]['playing'] = 0
                                        player[addr_]['ready'] = 1
                                        player[addr_]['sweapon'] = [0]*18
                                        player[addr_]['sammo'] = [0]*18
                                        player[addr_]['sammoin'] = [0]*18
                                        player[addr_]['deads'] = player[addr_]['deads'] + 1
                                        if player[addr]['team'] == player[addr_]['team']:
                                            player[addr]['frags'] = player[addr]['frags'] - 1
                                        else:
                                            player[addr]['frags'] = player[addr]['frags'] + 1
                                        sendall((((WriteByte(41) + WriteByte(player[addr_]['ID'])) + WriteByte(50)) + WriteByte(round)), imp = 1)
                                        sleep(2)
                                        player[addr_]['playing'] = 1
                                        ans = ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( WriteByte(100) + WriteByte(player[addr_]['ID'])) + WriteLine(player[addr_]['name'])) + WriteByte(player[addr_]['team'])) + WriteByte(player[addr_]['look'])) + WriteByte(player[addr_]['vip'])) + WriteInt(IntIP(player[addr_]['ip']))) + WriteInt(player[addr_]['port'])) + WriteByte(player[addr_]['health'])) +WriteInt(player[addr_]['x'])) + WriteInt(player[addr_]['y'])) +WriteShort(player[addr_]['dir'])) + WriteShort((player[addr_]['frags']))) + WriteShort((player[addr_]['deads']))) + WriteByte(player[addr_]['sweapon'][7])) + WriteByte(player[addr_]['sweapon'][8])) + WriteByte(player[addr_]['gameadmin']))
                                        sendall(ans, imp = 1)
                                        sendall((((WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine( "You will be revived now...")), imp = 1, ids_ = [id_])
                                        sendall(((((((WriteByte(104) + WriteInt(player[ids[i]]['x'])) + WriteInt(player[ids[i]]['y'])) + WriteShort(player[ids[i]]['dir'])) + WriteByte(0)) + WriteInt(player[ids[i]]['money'])) + WriteByte(round)), imp=1)
                                        print "eh -.-"
                                        if player[addr_]['vip']:
                                            startround(11)
                                        restart = 1
                                        draw = 1
                                        for o in player.values():
                                            if o['team'] == player[addr_]['team'] and o['health'] != 0:
                                                restart = 0
                                                
                                            if o['team'] != player[addr_]['team'] and o['team'] != 0:
                                                draw = 0
                                                
                                        if draw:
                                            startround(0)
                                            
                                        elif restart:
                                            startround(player[addr]['team'] * 10)
                                            
                                    sendall(((((((WriteByte(40) + WriteByte(player[addr_]['ID'])) + WriteByte(player[addr]['ID'])) + WriteByte(player[addr_]['health'])) + WriteByte(50)) + WriteByte(player[addr_]['armor'])) + WriteByte(round)))
                    sendall(((WriteByte(10) + WriteByte(player[addr]['ID'])) + WriteByte(round)), ids_ = [id_])
        elif byte == 11:
            id_ = ReadByte(data)
            mode = ReadByte(data)
            if not checkid(addr, id_): 
                log4 = log4 + 'Hacker Attack: ID: Weaponmode' 
            else:
                impsend(addr, ReadShort(data))
                sendall(((WriteByte(11) + WriteByte(id_)) + WriteByte(mode)), imp = 1) 
        elif byte == 12:
            round = ReadByte(data)
            impsend(addr, ReadShort(data))
            sendall(((WriteByte(10)+WriteByte(player[addr]['ID']))+WriteByte(round)), ids_=[player[addr]['ID']]) 
        elif byte == 13:
            damagecount = ReadByte(data)
            damage = []
            for i in range(damagecount):
                id_ = ReadByte(data)
                if id_ in ids.keys():
                    damage.append(id_)
            weapon = ReadByte(data)
            weaponmode = ReadByte(data)
            round = ReadByte(data)
            impsend(addr, ReadShort(data))
            sendall(((WriteByte(10) + WriteByte(player[addr]['ID'])) + WriteByte(round)), [player[addr]['ID']])
            for i in damage:
                stutzpunkt = ((player[addr]['x']+16),(player[addr]['x']+16))
                if player[addr]['dir'] >= 0:
                    dir = player[addr]['dir']
                dir = (360 + player[addr]['dir']) - 32767
                richtung = (sin(radians(dir)), (-cos(radians(dir))))
                distance = ((player[ids[i]]['x']-player[addr]['x'])**2 + (player[ids[i]]['y']-player[addr]['y'])**2)**0.5
                collision = ((stutzpunkt[0]+(richtung[0]*distance)),(stutzpunkt[1]+(richtung[1]*distance)))
                if collision[0] <= (player[ids[i]]['x']+48) or collision[0] >= (player[ids[i]]['x'] + 16) or collision[1] <= (player[ids[i]]['y']+48) or collision[1] >= (player[ids[i]]['y'] + 16) and addr != ids[i] and player[addr]['health'] != 0 and player[ids[i]]['health'] != 0 and player[ids[i]]['playing']:
                    if settings['Svff'] or player[addr]['team'] != player[ids[i]]['team']:
                        if weaponmode == 2:
                            power = weapon_damage_z2[weapon]/3
                        elif weaponmode == 1:
                            power = weapon_damage_z1[weapon]/3
                        else:
                            power = weapon_damage[weapon]/3
                        if player[ids[i]]['armor'] == 0:
                            player[ids[i]]['health'] = player[ids[i]]['health'] - power
                        elif player[ids[i]]['armor'] < 150:
                            player[ids[i]]['health'] = int(player[ids[i]]['health']-(0.65*power))
                        if player[ids[i]]['armor'] > 0:
                            player[ids[i]]['armor'] = player[ids[i]]['armor'] - power
                            if player[ids[i]]['armor'] < 0:
                                player[ids[i]]['armor'] = 0
                        if player[ids[i]]['health'] <= 0 and player[ids[i]]['playing']:
                            player[ids[i]]['health'] = 100
                            player[ids[i]]['playing'] = 0
                            sendall(((((WriteByte(41) + WriteByte(i)) + WriteByte(player[addr]['ID'])) + WriteByte(weapon)) + WriteByte(round)), imp = 1)
                            #player[ids[i]]['sweapon'] = [0]*18
                            #player[ids[i]]['sammo'] = [0]*18
                            #player[ids[i]]['sammoin'] = [0]*18
                            player[ids[i]]['deads'] = player[ids[i]]['deads'] + 1
                            if player[addr]['team'] == player[ids[i]]['team']:
                                player[addr]['frags'] = player[addr]['frags'] - 1
                            else:
                                player[addr]['frags'] = player[addr]['frags'] + 1
                            
                            #sleep(3)
                            player[ids[i]]['playing'] = 1
#                            for a in map_[player[ids[i]]['team']]:
#                                x = str(a[0]) 
#                                y = str(a[1])
                            
                            sendall((((WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine( "You will be revived now...")), imp = 1)
                            sendall(((((WriteByte(42) + WriteByte(player[ids[i]]['ID']))  + WriteByte(player[ids[i]]['health']))  + WriteByte(player[ids[i]][100])) + WriteByte(round + 1)),)
                            sendall(((((((WriteByte(104) + WriteInt(player[ids[i]]['x'])) + WriteInt(player[ids[i]]['y'])) + WriteShort(player[ids[i]]['dir'])) + WriteByte(0)) + WriteInt(player[ids[i]]['money'])) + WriteByte(round+1)), imp=1, time = (time()+3))
                            if player[ids[i]]['vip']:
                                startround(11)
                            restart = 1
                            draw = 1
                            for o in player.values():
                                if o['team'] == player[ids[i]]['team'] and o['health'] != 0:
                                    restart = 0
                                    
                                if o['team'] != player[ids[i]]['team'] and o['team'] != 0:
                                    draw = 0
                                    
                            if draw:
                                startround(0)
                                
                            elif restart:
                                startround(player[addr]['team'] * 10)
                                
                        sendall(((((((WriteByte(40) + WriteByte(player[ids[i]]['ID'])) + WriteByte(player[addr]['ID'])) + WriteByte(player[ids[i]]['health'])) + WriteByte(50)) + WriteByte(player[ids[i]]['armor'])) + WriteByte(round)))
        elif byte == 15:
            id_ = ReadByte(data)
            x = ReadInt(data)
            y = ReadInt(data)
            round = ReadByte(data)
            if not checkid(addr, id_): 
                log4 = log4 + 'Hacker Attack Pos' 
            else:
                player[addr]['lastmove'] = time()
                if ((player[addr]['x']-x)**2 + (player[addr]['y']-y)**2)**.5 <= 32: 
                    player[addr]['lastmove'] = time() + 1.5
                player[addr]['x'] = x
                player[addr]['y'] = y
                if settings['Svantilag']: 
                    for pl in player:
                        if pl['ID'] not in (0, id_) and  pl['team']: 
                            sendone(((((WriteByte(15)+WriteByte(pl['ID']))+WriteInt(pl['x']))+ WriteInt(pl['y'])) + WriteByte(rses)))     
                sendall(((((WriteByte(15)+WriteByte(id_))+WriteInt(x))+ WriteInt(y)) + WriteByte(round)), ids_ = [id_])
                if player[addr]['playing'] and  mapcolision((player[addr]['x'] + 16),(player[addr]['y'] + 16),[50,51,52,53]): 
                    player[addr]['health'] = 0
                    player[addr]['playing'] = 0
                    player[addr]['sweapon'] = [0]*18
                    player[addr]['sammo'] = [0]*18
                    player[addr]['sammoin'] = [0]*18
                    sendall(WriteByte(41)+WriteByte(player[addr]['ID'])+WriteByte(200)+(map_['code']+((x+16)/32 + (y+16)/32)-50) + round, imp = 1)
                    if player[addr]['vip']: 
                        startround(11)
                    restart = 1
                    draw = 1
                    
                    for o in player.values():
                        if o['team'] == player[addr]['team'] or  o['health'] != 0:
                                restart = 0  
                        elif o['team'] != plauer[addr]['team'] or  o['team'] != 0:
                                draw = 0  
                    log("something's wrong here...",629,str(draw) + " and " + str(restart))
                    if draw: 
                        startround(0)  
                    elif restart and player[addr]['team'] == 1:
                        startround(20)  
                    elif restart and team == 2: 
                        startround(10)
                if player[addr]['playing'] and  player[addr]['vip'] and (player[addr]['x']/32,player[addr]['y']/32) in map_['vipescape']: 
                    startround(21)  
                elif player[addr]['playing'] and map_['typ'] == 2 and player[addr]['hostages']:
                    Hostage 
    
    
    
    
    
    
    
    
    
    
    
    
        elif byte == 16: 
            id_ = ReadByte(data)
            dir = ReadShort(data)
            if not checkid(addr, id_):
                log4 = log4 + 'Hack : Dir'
            else:
                player[addr]['dir'] = dir
                sendall(((WriteByte(16)+ WriteByte(id_))+ WriteShort(dir))) 
        elif byte == 20: 
            id_ = ReadByte(data)
            xdif = ReadByte(data)
            ydif = ReadByte(data)
            botact['move'] = id_
            if not checkid(addr, id_):
                log4 = log4 + 'Hacker Attack ID: MOVE'
            else:
    
                if settings['Svlastmove']== 0 or (time() -player[addr]['lastmove']) < settings['Svlastmove']/1000: 
                    if player[addr]['lastmove']<=time():
                        player[addr]['lastmove'] = time()
                    player[addr]['x'] = player[addr]['x'] + (xdif - 128)
                    player[addr]['y'] = player[addr]['y'] + (ydif - 128)
                    if settings['Svantilag']: 
                        for pl in player: 
                            if pl['ID'] not in (0, id_) and pl['team']: 
                                sendone(WriteByte(15) + plID + pladdrx + pladdry + round)
                            else:
                                sendone(writebyte(15) + plID + plX + ply + round)
                    sendall((((WriteByte(20) + WriteByte(id_)) + WriteByte(xdif)) +WriteByte(ydif)), ids_ = [id_])
                    if player[addr]['playing'] and mapcolision(player[addr]['x'] + 16, player[addr]['y'] + 16, [50, 51, 52, 53]):
    
                        player[addr]['health'] = 0
                        player[addr]['playing'] = 0
                        player[addr]['sweapon'] = [0]*18
                        player[addr]['sammo'] = [0]*18
                        player[addr]['sammoin'] = [0]*18
                        sendall(WriteByte(41)+addID + 200 + (map_map + addrx+16/32 / addry+16/32)-50 + round, imp = 1)
                        if player[addr]['vip']: 
                            startround(11)
                        draw = 1
                        restart = 1
                        for o in plaer.values: 
                            if o['team'] == player[addr]['team'] and o['health'] != 0:
                                restart = 0 
                            elif o['team'] != player[addr]['team'] and o['team'] != 0:
                                draw = 0
                        if draw:
                            startround(o)  
                        elif restart and player[addr]['team'] == 1: 
                            startround(20)
                        elif restart and player[addr]['team'] == 2:
                            startround(10)
                    if player[addr]['playing'] and player[addr]['vip'] and [player[addr]['x']/32, player[addr]['y']/32] in map_['vipescape']:
                        startround(21)
                else:
                    sendall(WriteByte(252) + 2 + addrID, imp = 1)
                    kill(addr)
                    log4 = log4 + 'kicked (too high lastmove)'
        elif byte == 21: 
            id_ = ReadByte(data)
            xdif = ReadByte(data)
            ydif = ReadByte(data)
            if not checkid(addr, id_):
                log4 = log4 + 'Hacker Attack ID: Walk'
            else:
                if settings['Svlastmove']== 0 or (time() -player[addr]['lastmove']) < settings['Svlastmove']/1000: 
                    
                    player[addr]['lastmove'] = time()
                    player[addr]['x'] = player[addr]['x'] + (xdif - 128)
                    player[addr]['y'] = player[addr]['y'] + (ydif - 128)
                    if settings['Svantilag']: 
                        for pl in player: 
                            if pl['ID'] not in (0, id_) and pl['team']: 
                                sendone(WriteByte(15) + plID + pladdrx + pladdry + round)
                    else: 
                        sendall((((WriteByte(21) + WriteByte(id_)) + WriteByte(xdif)) +WriteByte(ydif)), ids_ = [id_])
                    if player[addr]['playing'] and mapcolision(player[addr]['x'] + 16, player[addr]['y'] + 16, [50, 51, 52, 53]):
    
                        player[addr]['health'] = 0
                        player[addr]['playing'] = 0
                        player[addr]['sweapon'] = [0]*18
                        player[addr]['sammo'] = [0]*18
                        player[addr]['sammoin'] = [0]*18
                        sendall(WriteByte(41)+addID + 200 + (map_map + addrx+16/32 / addry+16/32)-50 + round, imp = 1)
                        if player[addr]['vip']: 
                            startround(11)
                        draw = 1
                        restart = 1
                        for o in player.values: 
                            if o['team'] == player[addr]['team'] and o['health'] != 0:
                                restart = 0 
                            elif o['team'] != player[addr]['team'] and o['team'] != 0:
                                draw = 0
                        if draw:
                            startround(o) 
                        elif restart and player[addr]['team'] == 1: 
                            startround(20)
                        elif restart and player[addr]['team'] == 2:
                            startround(10)
                    if player[addr]['playing'] and player[addr]['vip'] and [player[addr]['x']/32, player[addr]['y']/32] in map_['vipescape']:
                        startround(21)
                else:
                    sendall(WriteByte(252) + 2 + addrID, imp = 1)
                    kill(addr)
                    log4 = log4 + 'kicked (too high lastmove)'
        elif byte == 22: 
            id_ = ReadByte(data)
            xdif = ReadByte(data)
            ydif = ReadByte(data)
            dir = ReadShort(data)
            if not checkid(addr, id_):
                log4 = log4 + 'Hacker Attack ID: Move + Dir'
            else:
                if settings['Svlastmove']== 0 or (time() -player[addr]['lastmove']) < settings['Svlastmove']/1000:                 
                    player[addr]['lastmove'] = time()
                    player[addr]['x'] = player[addr]['x'] + (xdif - 128)
                    player[addr]['y'] = player[addr]['y'] + (ydif - 128)
                    player[addr]['dir'] = dir
                    if settings['Svantilag']: 
                        for pl in player: 
                            if pl['ID'] not in (0, id_) and pl['team']: 
                                sendone(WriteByte(15) + plID + pladdrx + pladdry + round)
                    else: 
                        sendall(((((WriteByte(22) + WriteByte(id_)) + WriteByte(xdif)) +WriteByte(ydif))+WriteShort(dir)), ids_ = [id_])
                    if player[addr]['playing'] and  mapcolision(player[addr]['x'] + 16, player[addr]['y'] + 16, [50, 51, 52, 53]):
    
                        player[addr]['health'] = 0
                        player[addr]['playing'] = 0
                        player[addr]['sweapon'] = [0]*18
                        player[addr]['sammo'] = [0]*18
                        player[addr]['sammoin'] = [0]*18
                        sendall(WriteByte(41)+addID + 200 + (map_map + addrx+16/32 / addry+16/32)-50 + round, imp = 1)
                        if player[addr]['vip']: 
                            startround(11)
                        draw = 1
                        restart = 1
                        for o in player.values: 
                            if o['team'] == player[addr]['team'] and o['health'] != 0:
                                restart = 0 
                            elif o['team'] != player[addr]['team'] and o['team'] != 0:
                                draw = 0
                        if draw:
                            startround(o)  
                        elif restart and player[addr]['team'] == 1: 
                            startround(20)
                        elif restart and player[addr]['team'] == 2:
                            startround(10)
                    if player[addr]['playing'] and player[addr]['vip'] and [player[addr]['x']/32, player[addr]['y']/32] in map_['vipescape']:
                        startround(21)
                else:
                    sendall(WriteByte(252) + 2 + addrID, imp = 1)
                    kill(addr)
                    log4 = log4 + 'kicked (too high lastmove)'
        elif byte == 23: 
            id_ = ReadByte(data)
            xdif = ReadByte(data)
            ydif = ReadByte(data)
            dir = ReadShort(data)
            if not checkid(addr, id_):
                log4 = log4 + 'Hacker Attack ID: Walk + Dir'
            else:
                if settings['Svlastmove']== 0 or (time() -player[addr]['lastmove']) < settings['Svlastmove']/1000:                 
                    player[addr]['lastmove'] = time()
                    player[addr]['x'] = player[addr]['x'] + (xdif - 128)
                    player[addr]['y'] = player[addr]['y'] + (ydif - 128)
                    player[addr]['dir'] = dir
                    if settings['Svantilag']: 
                        for pl in player: 
                            if pl['ID'] not in (0, id_) and pl['team']: 
                                sendone(WriteByte(15) + plID + pladdrx + pladdry + round)
                    else: 
                        sendall(((((WriteByte(23) + WriteByte(id_)) + WriteByte(xdif)) +WriteByte(ydif))+WriteShort(dir)), ids_ = [id_])
                    if player[addr]['playing'] and mapcolision(player[addr]['x'] + 16, player[addr]['y'] + 16, [50, 51, 52, 53]):
                        player[addr]['health'] = 0
                        player[addr]['playing'] = 0
                        player[addr]['sweapon'] = [0]*18
                        player[addr]['sammo'] = [0]*18
                        player[addr]['sammoin'] = [0]*18
                        sendall(WriteByte(41)+addID + 200 + (map_map + addrx+16/32 / addry+16/32)-50 + round, imp = 1)
                        if player[addr]['vip']: 
                            startround(11)
                        draw = 1
                        restart = 1
                        for o in player.values: 
                            if o['team'] == player[addr]['team'] and o['health'] != 0:
                                restart = 0 
                            elif o['team'] != player[addr]['team'] and o['team'] != 0:
                                draw = 0
                        if draw:
                            startround(o) 
                        elif restart and player[addr]['team'] == 1: 
                            startround(20)
                        elif restart and player[addr]['team'] == 2:
                            startround(10)
                    if player[addr]['playing'] and player[addr]['vip'] and [player[addr]['x']/32, player[addr]['y']/32] in map_['vipescape']:
                        startround(21)
                else:
                    sendall(WriteByte(252) + 2 + addrID, imp = 1)
                    kill(addr)
                    log4 = log4 + 'kicked (too high lastmove)'
        elif byte == 30:
            id_ = ReadByte(data)
            slot = ReadByte(data)
            weapon = ReadByte(data)
            if not checkid(addr, id_):
                impsend(addr,ReadShort(data))
            else:
                impsend(addr, ReadShort(data))
                player[addr]['slot'] = slot
                sendall((((WriteByte(30) + WriteByte(player[addr]['ID'])) + WriteByte(slot)) + WriteByte(weapon)), imp = 1, ids_ = [id_])
        elif byte == 31:
            id_ = ReadByte(data)
            slot = ReadByte(data)
            typ = ReadByte(data)
            ammo = ReadInt(data)
            ammoin = ReadInt(data)
            x = ReadInt(data)
            y = ReadInt(data)
            if not checkid(addr, id_):
                log4 = log4 + "Hacker Attack (ID: Drop)"
            else:
                impsend(addr, ReadShort(data))
                player[addr]['sweapon'][slot] = 0
                player[addr]['sammo'][slot] = ammo
                player[addr]['sammoin'][slot] = ammoin
                sendall((((((((WriteByte(31) + WriteByte(player[addr]['ID'])) + WriteByte(slot)) + WriteByte(typ)) + WriteInt(ammo)) + WriteInt(ammoin)) + WriteInt(x)) + WriteInt(y)), imp = 1, ids_ = [player[addr]['ID']])
        elif byte == 32:
            id_ = ReadByte(data)
            typ = ReadByte(data)
            if not checkid(addr, id_):
                log4 = log4 + "Hacker Attack (ID: Buy)"
            else:
                if typ in range(10, 47):
                    player[addr]['sweapon'][0] = typ
                elif typ in range(2, 7):
                    player[addr]['sweapon'][1] = typ
                elif typ == 61 or typ == 62:
                    slot = typ - 61
                    if player[addr]['sammo'][slot] >= (weapon_ammo[player[addr]['sweapon'][slot]]-weapon_ammoin[player[addr]['sweapon'][slot]]):
                        player[addr]['sammo'][slot] = weapon_ammo[player[addr]['sweapon'][slot]]
                    else:
                        player[addr]['sammo'][slot] =(player[addr]['sammo'][slot] + weapon_ammo[player[addr]['sweapon'][slot]])
                elif typ == 63 or typ == 64:
                    slot = typ - 63
                    player[addr]['sammo'][slot] = weapon_ammo[player[addr]['sweapon'][slot]]
                elif typ == 57:
                    if player[addr]['armor'] < 60:
                        player[addr]['armor'] = 60
                elif typ == 58:
                    player[addr]['armor'] = 100
                elif typ == 56:
                    player[addr]['sweapon'][8] = typ
                impsend(addr, ReadShort(data))
                sendall(((WriteByte(32) + WriteByte(player[addr]['ID'])) + WriteByte(typ)), imp = 1, ids_ = [id_])
        elif byte in (40, 42):
            pass
        elif byte == 41: 
            id_ = ReadByte(data)
            killer = ReadByte(data)
            weapon = ReadByte(data)
            round = ReadByte(data)
            if not checkid(addr, id_):
                return 0
            else:
                impsend(addr, ReadShort(data))
                player[addr]['health'] = 0
                player[addr]['playing'] = 0
                player[addr]['sweapon'] = [0] * 18
                player[addr]['sammo'] = [0] * 18
                player[addr]['sammoin'] = [0] * 18
                if killer  == 202 and round == game['round']:
                    player[addr]['frags'] = player[addr]['frags'] - 1
                    player[addr]['deads'] = player[addr]['deads'] + 1
                    sendall(((((WriteByte(41) + WriteByte(player[addr]['ID'])) + WriteByte(202)) + WriteByte(weapon)) + WriteByte(round)), imp = 1)
                if player[addr]['vip']:
                    startround(11)
                draw = 1
                restart = 1
                for o in player.values():
                    if o['team'] == player[addr]['team'] and o['health'] != 0:
                        restart = 0
                    if o['team'] != player[addr]['team'] and o['team'] != 0:
                        draw = 0
                if draw:
                    startround(0)
                elif restart:
                    if player[addr]['team'] == 1:
                        startround(20)
                    elif player[addr]['team'] == 2:
                        startround(10)
        elif byte == 91:
            mode = ReadByte(data)
            id_ = ReadByte(data)
            message = ReadLine(data)
            if message == "restart":
                startround(0)
            elif message == "bot":
                addbot()
            mode = 4
            if not checkid(addr, id_):
                log4 = log4 + "Hacker Attack: Say"
            else:
                impsend(addr, ReadShort(data))
                if mode == 1:
                    log4 = log4 + "Said: " + message
                    sendall((((WriteByte(91) + WriteByte(1)) + WriteByte(id_)) + WriteLine(message)), imp = 1, ids_ = [id_])
                elif mode == 2:
                    log4 = log4 + "Said: " + message
                    for pl in player.values():
                        if pl['team'] == player[addr]['team']:
                            if player[addr]['health'] > 0 and pl['health'] < 0:
                                ids_.append(pl['ID'])
                            elif pl['health'] > 0:
                                ids_.append(pl['ID'])
                    sendall((((WriteByte(91) + WriteByte(2)) + WriteByte(id_)) + WriteLine(message)), imp = 1, ids_ = [id_])
                elif mode == 3:
                    log4 = log4 + "Hacker Attack: servermsg"
                else:
                    log4 = log4 + "Said: " + message
                    sendall((((WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine(player[addr]['name'] + "Says: " + message)), imp = 1, ids_ = [id_])
                    
        elif byte == 102:
            id_ = ReadByte(data)
            team = ReadByte(data)
            if not checkid(addr, id_):
                log4 = log4 + "Hacker Attack: Teams"
            else:
                log4 = log4 + "Joined team " + str(team)
                impsend(addr, ReadShort(data))
                if player[addr]['team'] != 0 and player[addr]['health'] != 0:
                    sendall(((((WriteByte(41)+WriteByte(player[addr]['ID'])) + WriteByte(200)) + WriteByte(0)) + WriteByte(game['round'])), imp = 1)
                    player[addr]['deads'] = player[addr]['deads'] + 1
                player[addr]['health'] = 0
                player[addr]['armor'] = 0
                player[addr]['playing'] = 0
                player[addr]['ready'] = 0
                player[addr]['sweapon'] = [0]*19
                ids_ = [player[addr]['ID']]
                if settings['Svautoteam'] and team != 0:
                    cts = 0
                    ts = 0
                    for pl in player.values():
                        if pl['team'] == 1:
                            ts = ts + 1
                        elif pl['team'] == 2:
                            cts = cts + 1
                    if cts > ts and team != 1:
                        team = 1
                        ids_ = []
                    elif cts < ts and team != 2:
                        team = 2
                        ids_ = []
                player[addr]['team'] = team
                sendall(((WriteByte(102) + WriteByte(player[addr]['ID'])) + WriteByte(player[addr]['team'])), imp = 1, ids_ = ids_)
        elif byte == 103:
            id_ = ReadByte(data)
            look = ReadByte(data)
            if not checkid(addr, id_):
                log4 = log4 + "Hacker Attack: Look"
            else:
                impsend(addr, ReadShort(data))
                player[addr]['look'] = look
                if not player[addr]['ready']:
                    player[addr]['slot'] = 1
                    player[addr]['ready'] = 1
                player[addr]['sweapon'][1] = player[addr]['team']
                sendall(((WriteByte(103)+WriteByte(player[addr]['ID'])) + WriteByte(player[addr]['look'])), imp = 1, ids_ = [id_])
                log4 = log4 + "Changed look to " + str(look)
                emptyt = 1
                emptyct = 1
                for pl in player.values():
                    if pl['team'] == 1 and pl['ID'] != player[addr]['ID']:
                        emptyt = 0
                    elif pl['team'] == 2 and pl['ID'] != player[addr]['ID']:
                        emptyct = 0
                if emptyt or emptyct:
                    startround(0)
                    add ('Round Started (empty team)')
        else:
            ishandled = 0

    if log4 != "":
        add(prefix + log4)
    
    
    #startid(byte, data, ishandled, startime)
    delStream(data)
    
    if player.has_key(addr):
        player[addr]['timeout'] = time()
def startround(mode):
    if (not updater["startround"]):
        updater["startround"] = 1
        game["restartmode"] = mode
        game["roundstart"] = (time() + settings["Svrestarttimer"])
        if (mode in (10, 11, 12)):
            game["t_score"] += 1
        elif (mode in (20, 21, 22)):
            if ((mode == 20) and (game["bombtimer"] != 0)):
                updater["startround"] = 0
                return 0
            game["ct_score"] += 1
            if (mode == 21):
                player[ids[game["vipid"]]]["health"] = 0
                player[ids[game["vipid"]]]["playing"] = 0
                player[ids[game["vipid"]]]["sweapon"] = ([0] * 18)
                player[ids[game["vipid"]]]["sammo"] = ([0] * 18)
                player[ids[game["vipid"]]]["sammoin"] = ([0] * 18)
                sendall(((((WriteByte(41) + WriteByte(game["vipid"])) + WriteByte(203)) + WriteByte(0)) + WriteByte(game["round"])), imp=1)
        game["bombtimer"] = 0
        sendall(((WriteByte(105) + WriteByte(mode)) + WriteInt(settings["Svrestarttimer"])), imp=1)



def checkid(addr, id_):
    if (player[addr]["ID"] == id_):
        return 1
    else:
        return 0



def sendall(data, ids_ = [], time = 0, imp = 0, impcount = 5, imptime = 1):
    msgids = []
    for pl in player.values():
        if ((pl["ID"] != 0) and (pl["ID"] not in ids_)):
            if imp:
                msgids.append(sendone((pl["ip"],
                 pl["port"]), data, time_=time, imp=imp, impcount=impcount, imptime=imptime))
            else:
                sendone((pl["ip"],
                 pl["port"]), data, time_=time, imp=imp)

    if imp:
        return msgids



def sendone(addr, data, time_ = 0, imp = 0, impcount = 5, imptime = 1):
    if (addr != addre):
        if (time_ == 0):
            time_ = time()
        if imp:
            msgid = impid()
            sends.append((addr,
             (data + WriteShort(msgid)),
             time_))
            impsends[msgid] = [addr,
             (data + WriteShort(msgid)),
             (time_ + imptime),
             impcount,
             msgid]
        else:
            sends.append((addr,
             data,
             time_))
        if imp:
            return msgid



def kill(addr):
    if player.has_key(addr):
        ctlives = 0
        tlives = 0
        player[addr]["health"] = 0
        for o in player.values():
            if (o["health"] != 0):
                if (o["team"] == 1):
                    tlives = 1
                elif (o["team"] == 2):
                    ctlives = 2

        if player[addr]["vip"]:
            startround(11)
        if ((not ctlives) and (not tlives)):
            startround(0)
        if (not tlives):
            startround(20)
        if (not ctlives):
            startround(10)
        if ids.has_key(player[addr]["ID"]):
            del ids[player[addr]["ID"]]
        else:
            add(("3rr0r: Deleting ID of " + addr[0]))
        del player[addr]
    else:
        add(("3rr0r: Deleting " + addr[0]))



def impid():
    global limp
    if (limp == 65025):
        limp = 0
    else:
        limp += 1
    return limp



def update():
    global grenades
    player[addre]["timeout"] = time()
    for addr in player.keys():
        if not addr[0] == 607:
            if ((time() - player[addr]["timeout"]) > settings["timeout"]):
                add((player[addr]["ip"] + ": Pingtimeout (Server)"))
                sendall(((WriteByte(252) + WriteByte(1)) + WriteByte(player[addr]["ID"])), imp=1)
                kill(addr)
            elif ((player[addr]["lastping"] <= (time() - 1)) and (addr != addre)):
                player[addr]["lastping"] = time()
                pingids.append(sendone(addr, (((((WriteByte(51) + WriteByte(255)) + WriteInt(-1000)) + WriteInt(-1000)) + WriteByte(52)) + WriteByte(0)), imp=1, impcount=0))

    for gren in grenades.values():
        if (time() >= gren["explode"]):
            stutzpunkt = [gren["x"],
             gren["y"]]
            dir = (gren["dir"] % 360)
            richtung = [sin(radians(dir)),
             -cos(radians(dir))]
            coll = 0
            gren["x"] += (richtung[0] * 15)
            gren["y"] += (richtung[1] * 15)
            for i in range(250):
                gren["x"] += richtung[0]
                gren["y"] += richtung[1]
                if (coll == 0):
                    cx = [(gren["x"] + 10),
                     (gren["x"] + 20),
                     (gren["x"] + 10),
                     (gren["x"] + 20)]
                    cy = [(gren["y"] + 10),
                     (gren["y"] + 10),
                     (gren["y"] + 20),
                     (gren["y"] + 20)]
                    ca = ([0] * 4)
                    for i in range(4):
                        inside = 0
                        tx = int((cx[i] / 32))
                        ty = int((cy[i] / 32))
                        if ((tx >= 0) and ((ty >= 0) and ((tx <= map_["maxx"]) and (ty <= map_["maxy"])))):
                            inside = 1
                            if (map_["map"][tx][ty] in (1, 3)):
                                ca[i] = 1
                                coll = 11
                        if (not inside):
                            ca[i] = 1

                    if ca[0]:
                        if ca[1]:
                            richtung[1] = -richtung[1]
                        else:
                            richtung[0] = -richtung[0]
                    elif ca[1]:
                        if ca[3]:
                            richtung[0] = -richtung[0]
                        else:
                            richtung[1] = -richtung[1]
                    elif ca[2]:
                        richtung[1] = -richtung[1]
                    elif ca[3]:
                        richtung[0] = -richtung[0]
                else:
                    coll -= 1

            sendall((((((WriteByte(51) + WriteByte(gren["id"])) + WriteInt(gren["x"])) + WriteInt(gren["y"])) + WriteByte(gren["typ"])) + WriteByte(gren["owner"])), imp=1)
            gren["x"] += 16
            gren["y"] += 16
            if (gren["typ"] == 51):
                for pl in player.values():
                    if ((pl["health"] != 0) and ((pl["team"] != 0) and (settings["Svff"] or (pl["team"] != gren["team"])))):
                        distance = ((((gren["x"] - pl["x"]) ** 2) + ((gren["y"] - pl["y"]) ** 2)) ** 0.5)
                        if (distance < 160):
                            distance = abs((distance - 160))
                            factor = (distance / 160)
                            power = int((115 * factor))
                            if (player[(pl["ip"],
                             pl["port"])]["armor"] == 0):
                                player[(pl["ip"],
                                 pl["port"])]["health"] -= power
                            elif (player[(pl["ip"],
                             pl["port"])]["armor"] < 150):
                                player[(pl["ip"],
                                 pl["port"])]["health"] = int((player[(pl["ip"],
                                 pl["port"])]["health"] - (power * 0.65000000000000002)))
                            if (player[(pl["ip"],
                             pl["port"])]["armor"] > 0):
                                player[(pl["ip"],
                                 pl["port"])]["armor"] -= power
                                if (player[(pl["ip"],
                                 pl["port"])]["armor"] < 0):
                                    player[(pl["ip"],
                                     pl["port"])]["armor"] = 0
                            if (player[(pl["ip"],
                             pl["port"])]["health"] <= 0):
                                player[(pl["ip"],
                                 pl["port"])]["health"] = 0
                                player[(pl["ip"],
                                 pl["port"])]["playing"] = 0
                                player[(pl["ip"],
                                 pl["port"])]["sweapon"] = ([0] * 18)
                                player[(pl["ip"],
                                 pl["port"])]["sammo"] = ([0] * 18)
                                player[(pl["ip"],
                                 pl["port"])]["sammoin"] = ([0] * 18)
                                player[(pl["ip"],
                                 pl["port"])]["deads"] += 1
                                if (player[addr]["team"] == player[(pl["ip"],
                                 pl["port"])]["team"]):
                                    player[addr]["frags"] -= 1
                                else:
                                    player[addr]["frags"] += 1
                                sendall(((((WriteByte(41) + WriteByte(pl["ID"])) + WriteByte(gren["owner"])) + WriteByte(gren["typ"])) + WriteByte(game["round"])), imp=1)
                                if player[addr]["vip"]:
                                    startround(11)
                                restart = 1
                                draw = 1
                                for o in player.values():
                                    if ((o["team"] == player[(pl["ip"],
                                     pl["port"])]["team"]) and (o["health"] != 0)):
                                        restart = 0
                                    elif ((o["team"] != player[(pl["ip"],
                                     pl["port"])]["team"]) and (o["team"] != 0)):
                                        draw = 0

                                if draw:
                                    startround(0)
                                elif restart:
                                    startround((player[addr]["team"] * 10))
                            sendall(((((((WriteByte(40) + WriteByte(pl["ID"])) + WriteByte(gren["owner"])) + WriteByte(player[(pl["ip"],
                             pl["port"])]["health"])) + WriteByte(gren["typ"])) + WriteByte(player[(pl["ip"],
                             pl["port"])]["armor"])) + WriteByte(game["round"])))

            del grenades[gren["id"]]

    if ((game["roundstart"] + (settings["Svroundtime"] * 60)) <= time()):
        startround(0)
    if ((game["bombtimer"] != 0) and ((game["bombtimer"] + settings["Svbombtimer"]) <= time())):
        for pl in player.values():
            if ((pl["health"] != 0) and (pl["team"] != 0)):
                distance = ((((game["bombx"] - pl["x"]) ** 2) + ((game["bomby"] - pl["y"]) ** 2)) ** 0.5)
                if (distance < 800):
                    distance = abs((distance - 800))
                    factor = (distance / 800)
                    power = int((300 * factor))
                    if (player[(pl["ip"],
                     pl["port"])]["armor"] == 0):
                        player[(pl["ip"],
                         pl["port"])]["health"] -= power
                    elif (player[(pl["ip"],
                     pl["port"])]["armor"] < 150):
                        player[(pl["ip"],
                         pl["port"])]["health"] = int((player[(pl["ip"],
                         pl["port"])]["health"] - (power * 0.65000000000000002)))
                    if (player[(pl["ip"],
                     pl["port"])]["armor"] > 0):
                        player[(pl["ip"],
                         pl["port"])]["armor"] -= power
                        if (player[(pl["ip"],
                         pl["port"])]["armor"] < 0):
                            player[(pl["ip"],
                             pl["port"])]["armor"] = 0
                    if (player[(pl["ip"],
                     pl["port"])]["health"] <= 0):
                        player[(pl["ip"],
                         pl["port"])]["health"] = 0
                        player[(pl["ip"],
                         pl["port"])]["playing"] = 0
                        player[(pl["ip"],
                         pl["port"])]["sweapon"] = ([0] * 18)
                        player[(pl["ip"],
                         pl["port"])]["sammo"] = ([0] * 18)
                        player[(pl["ip"],
                         pl["port"])]["sammoin"] = ([0] * 18)
                        player[(pl["ip"],
                         pl["port"])]["deads"] += 1
                        sendall(((((WriteByte(41) + WriteByte(pl["ID"])) + WriteByte(255)) + WriteByte(55)) + WriteByte(game["round"])), imp=1)
                    sendall(((((((WriteByte(40) + WriteByte(pl["ID"])) + WriteByte(255)) + WriteByte(player[(pl["ip"],
                     pl["port"])]["health"])) + WriteByte(255)) + WriteByte(player[(pl["ip"],
                     pl["port"])]["armor"])) + WriteByte(game["round"])))

        startround(12)
    if (updater["startround"] and (time() >= game["roundstart"])):
        updater["startround"] = 0
        game["round"] += 1
        if (game["round"] < 255):
            game["round"] = 0
        grenades = {}
        start_begin = (((((WriteByte(105) + WriteByte(game["restartmode"])) + WriteInt(0)) + WriteByte(game["round"])) + WriteInt(game["t_score"])) + WriteInt(game["ct_score"]))
        count = 0
        start_end = ""
        pls = player.keys()
        shuffle(pls)
        givemission = 1
        for addr in pls:
            if (player[addr]["team"] and player[addr]["ready"]):
                randomfactor = randint(0, (len(map_[player[addr]["team"]]) - 1))
                player[addr]["x"] = (map_[player[addr]["team"]][randomfactor][0] * 32)
                player[addr]["y"] = (map_[player[addr]["team"]][randomfactor][1] * 32)
                if ((((map_["typ"] == 1) and (player[addr]["team"] == 2)) or ((map_["typ"] == 3) and (player[addr]["team"] == 1))) and givemission):
                    givemission = 0
                    mission = 1
                else:
                    mission = 0
                if ((map_["typ"] == 1) and (player[addr]["team"] == 2)):
                    player[addr]["vip"] = mission
                    if mission:
                        player[addr]["x"] = (map_["vipspawn"][0] * 32)
                        player[addr]["y"] = (map_["vipspawn"][1] * 32)
                        game["vipid"] = player[addr]["ID"]
                        player[addr]["armor"] = 200
                elif (map_["typ"] == 1):
                    player[addr]["vip"] = 0
                elif (0 and (map_["typ"] == 2)):
                    for i in map_["resethostages"]:
                        map_["hostages"][i] = map_["resethostages"][i][:]

                player[addr]["playing"] = 1
                player[addr]["health"] = 100
                player[addr]["dir"] = 0
                player[addr]["lastmove"] = time()
                count += 1
                start_end += (((((WriteByte(player[addr]["ID"]) + WriteInt(player[addr]["x"])) + WriteInt(player[addr]["y"])) + WriteShort(player[addr]["dir"])) + WriteByte(mission)) + WriteInt(0))

        sendall(((start_begin + WriteByte(count)) + start_end), imp=1)
    if (settings["Svusgnregister"] and (time() >= game["usgnregister"])):
        if register():
            add("Reregister in Gaming Network successful", 1)
        else:
            add("Reregister in Gaming Network failed")



def impsend(addr, id_):
    sendone(addr, (WriteByte(255) + WriteShort(id_)))



def map():
    global map_
    add((("Loading map (" + settings["Svmap"]) + ")"), 1, 0)
    start = time()
    (code, map_,) = loadmap(settings["Svmap"])
    if code:
        add((("map loaded in " + str((time() - start))) + " seconds"), 1, 0)
        return 1
    else:
        add((("Couldn't load map (" + map_) + ")"), 1, 0)
        return 0



def mapcolision(x, y, typs):
    if (((x // 32) < 0) or (((y // 32) < 0) or (((x // 32) > map_["maxx"]) or ((x // 32) > map_["maxy"])))):
        return 0
    elif (map_["map"][int((x // 32))][int((y // 32))] in typs):
        return 1
    else:
        return 0

def log(tag,line,data):
    logto(tag + " @ " + str(line),data, startime)
    
def ini():
    global player
    global game
    global grenades
    global ids
    grenades = {}
    game = {"roundstart": time(),
     "ct_score": 0,
     "t_score": 0,
     "ct_winrow": 0,
     "t_winrow": 0,
     "bombstart": 0,
     "bombtimer": 0,
     "round": 0,
     "restartmode": 0,
     "bombx": 0,
     "bomby": 0,
     "bombplanter": 0,
     "vipid": 0,
     "usgnregister": (time() + (settings["Svusgnregister"] * 3600))}
    ids = {0: addre}
    player = {addre: {"name": "",
             "ID": 0,
             "ip": ip,
             "port": addre[1],
             "timeout": 0,
             "money": 0,
             "roundlived": 0,
             "ping": 0,
             "team": 0,
             "look": 0,
             "vip": 0,
             "x": 0,
             "y": 0,
             "dir": 0,
             "health": 0,
             "frags": 0,
             "deads": 0,
             "sweapon": ([0] * 18),
             "sammo": ([0] * 18),
             "sammoin": ([0] * 18),
             "gameadmin": 1,
             "ready": 0,
             "slot": 0,
             "armor": 0,
             "ping": 0,
             "playing": 0,
             "lastmove": 0,
             "lastping": 0,
             "hostages": []}}
    add("Round has been started", 1, 0)

def addbot():
    global player
    global ids
    prefix = 607
    temp_ids = ids.keys()
    id_ = 1
    while id_ in temp_ids: 
        id_ = id_ + 1
    addr = (607,id_)
    player[addr] = {"name": "bot",
                        "ID": id_,
                        "ip": addre[0],
                        "port": addre[1],
                        "timeout": time(),
                        "money": 0,
                        "roundlived": -1,
                        "ping": 0,
                        "team": 1,
                        "look": 2,
                        "vip": 0,
                        "x": 0,
                        "y": 0,
                        "dir": 0,
                        "health": 0,
                        "frags": 32767,
                        "deads": 32767,
                        "sweapon": ([0] * 18),
                        "sammo": ([0] * 18),
                        "sammoin": ([0] * 18),
                        "gameadmin": 0,
                        "ready": 1,
                        "slot": 0,
                        "armor": 0,
                        "ping": 0,
                        "playing": 0,
                        "lastmove": time(),
                        "lastping": time(),
                        "hostages": []}
    ids[id_]= addr
    for pl in player.values(): 
        if pl['ID'] != id_: 
            ans =( ( ( (WriteByte(101) + WriteLine("bot")) + WriteInt(IntIP(player[addr]['ip'])))+ WriteInt(addr[1])) + WriteByte(id_))
            sendone((pl['ip'],pl['port']), ans, imp = 1)
    sendall(((WriteByte(102) + WriteByte(player[addr]['ID'])) + WriteByte(player[addr]['team'])), imp = 1)
    sendall(((WriteByte(103)+WriteByte(player[addr]['ID'])) + WriteByte(player[addr]['look'])), imp = 1,)
    #thebot = Bot(addr)
    #thebot.start()
    startround(0)

def send():
    for (addr, data, time_,) in sends:
        if (time_ < time()):
            server.sendto(data, addr)
            sends.remove((addr,
             data,
             time_))




def resendimp():
    for (addr, data, time_, count, msgid,) in impsends.values():
        if (addr not in player.keys()):
            del impsends[msgid]
        elif (time_ < time()):
            if (count >= 0):
                sendone(addr, data)
                impsends[msgid][3] -= 1
                impsends[msgid][2] += 1
                delStream(data)
            else:
                del impsends[msgid]



if (__name__ == "__main__"):
    load()
    if (map() and start()):
        atexit.register(quit)
        ini()
        startime = time()
        run()

