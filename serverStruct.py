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
import sys 
import atexit 
sys.stderr = open("debug.txt", "w+")
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
                handler(data, addr)
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



def handler(data, address):
    return 0

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
             "ammor": 0,
             "ping": 0,
             "playing": 0,
             "lastmove": 0,
             "lastping": 0,
             "hostages": []}}
    add("Round has been started", 1, 0)



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
        run()

