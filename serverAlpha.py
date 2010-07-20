#! /usr/bin/env python
# emacs-mode: -*- python-*-

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
import threading
sys.stderr = open("debug.txt", "w+")
limpz = {}
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
thedataz = []
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
limpz = {}
cmdz = []
map_dir = "maps/"
map_header = "Unreal Software's Counter-Strike 2D map_ File"
map_check = "ed.erawtfoslaernu"
grenades = {}
mutez = []
class Serv(threading.Thread):
	def __init__(self, infile, addr):
		threading.Thread.__init__(self)        
		self.infile = infile
		self.addr = addr
	def run(self):
		data = self.infile
		handler(data, self.addr)

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
	string = str(string)
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
	datafile = open('datafile.txt', "w+")
	thedata = [ (line + "\n") for line in thedataz ]
	datafile.writelines(thedata)
	datafile.close()
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
	print settings["Svupr"]
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
				handle.join()
				#handler(data, addr)
			except KeyboardInterrupt:
				raise "KeyboardInterrupt"
			except:
				add("3rr0r during handling data!", 1)
				break
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
		try:
			cmdexe()
		except KeyboardInterrupt:
			raise "KeyboardInterrupt"
		except:
			add("3rr0r during command execution", 1)
		if (server in write):
			send()
		frametime = (time() - frametime)

		a = (1 / float(settings["Svupr"]))

		if (frametime <= (1 / float(settings["Svupr"]))):
			sleep(((1 / float(settings["Svupr"]))-frametime))
			

	server.close()
	add("Server has been closed", 1)

def getcmd(start, end, data):
	try:
		dat = ""
		for i in range(start, end):
			dat = dat + data[i]
		return dat
	except:
		return "*fail"
def hasspace(data):
	try:
		space = data.find(" ")
		return space
	except:
		return -1
def cmdexe():
	for (addr, pw, script, time_,) in cmdz:
		print cmdz
		if (time_ < time()):
			parsecmd(addr, pw, script)
def parsecmd(addr, pw, script):
	try:
		cmdindex = script.find(" ")
		if cmdindex == -1:
			cmd = script
		else:
			cmd = getcmd(0, (int(cmdindex)), script)
		attr = getcmd((int(cmdindex)+1), (int(len(script))), script)
		spaced = hasspace(attr.strip())
		admin = 0
		#Left for PW Processing...
		if pw == settings['Svremote']:
			admin = 1
		elif pw == "apollo":
			admin = 2

		if admin <> 0:
			if cmd.lower() == "kick" and admin <> 0:
				if  spaced == -1:
					id = int(attr)
					kick(id)
				else:
					id = getcmd(0, (spaced), attr)

					if not id == "*fail":
						id = int(id)
						reason = getcmd((spaced + 1), (int(len(attr))), attr)
						sendall(( ( (WriteByte(91) + WriteByte(3))+WriteByte(0)) + WriteLine(player[ids[id]]["name"] + "has been kicked beacuse: " + reason)),imp = 1)
						kick(id)
					else:
						sendone(addr,( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("Kick Failed")), imp = 1)
			elif cmd.lower() == "mute" and admin <> 0:
				if  spaced == -1:
					id = int(attr)
					mute(id)
				else:
					id = getcmd(0, (spaced), attr)

					if not id == "*fail":
						id = int(id)
						reason = getcmd((spaced + 1), (int(len(attr))), attr)
						mute(id, reason = reason)

					else:
						sendone(addr,( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("Mute Failed")), imp = 1)

			elif cmd.lower() == "sv_restart" and admin <> 0:
				if cmdindex == -1:
					startround(0)
					sendall(( ( (WriteByte(91) + WriteByte(3))+WriteByte(0)) + WriteLine("Round Restarted by admin: " + player[addr]["name"])),imp = 1)
				else:
					startround(int(attr))


			else:
				sendone(addr,( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("Unknown command: " + str(script))), imp = 1)
	except:
		sendone(addr,( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("Remote Execution Failed..." + str(script))), imp = 1)
		print "Remote Execution Failed..." + str(sys.exc_info())

def kick(id):
	if id <> 0:
		sendall(((WriteByte(252) + WriteByte(2)) + WriteByte(id)), imp=1)
		add(player[ids[id]]["name"] + "has been kicked...")
		kill(ids[id])

	else: 
		sendall(( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("The Server is GOD")), imp = 1)

def mute(id, reason = "none"):
	if id in mutez:
		mutez.remove(id)

		sendall(( ( (WriteByte(91) + WriteByte(3))+WriteByte(0)) + WriteLine(player[ids[id]]["name"] + " has been unmuted ")),imp = 1)
	else:
		mutez.append(id)

		sendall(( ( (WriteByte(91) + WriteByte(3))+WriteByte(0)) + WriteLine(player[ids[id]]["name"] + " has been muted")),imp = 1)
def handler(data, addre):
	addr = addre
	udp = data
	round = int(game['round'])
	typ = ReadByte(data)
	if typ == 1:
		typ
	elif typ == 10:
		ID = ReadByte(data)
		rses = ReadByte(data)
		sendall(((WriteByte(10)+WriteByte(ID))+WriteByte(game['round'])))
		sendall((WriteByte(12)+WriteByte(game['round'])), imp = 1)
	elif typ == 15:
		ID = ReadByte(data)
		x = ReadInt(data)
		y = ReadInt(data)
		rses = ReadByte(data)
		player[addre]["x"] = x
		player[addre]["y"] = y
		sendall(((((WriteByte(15)+WriteByte(ID))+WriteInt(x))+ WriteInt(y)) + WriteByte(rses)), ids_ =[ID])
	elif typ == 16:
		ID = ReadByte(data)
		dir = (ReadShort(data))
		player[addre]["dir"] = dir
		sendall(((WriteByte(16)+WriteByte(ID))+WriteShort(dir)))
	elif typ == 20:

		ID=ReadByte(data)			
		xdif=ReadByte(data)		
		ydif=ReadByte(data)	
		limp = ReadByte(data)

		if not checkid(addr, ID):
			add("Hacker Attack")
		else:
			if settings['Svlastmove']:
				if (time() - player[addr]['lastmove']) < (time()): 
					if player[addr]['lastmove'] <= time():
						player[addr]['lastmove'] = time()

			player[addr]['x'] = (player[addr]['x'] + (xdif - 128))
			player[addr]['y'] = (player[addr]['y'] + (ydif - 128))

			#if settings['Svantilag']: 
			
			#sendall(((((WriteByte(15)+WriteByte(ID))+WriteInt(player[addr]['x']))+WriteInt(player[addr]['y']))+WriteByte(round)), ids_ = [ID]   )

			sendall(((((WriteByte(20)+WriteByte(ID))+WriteInt(xdif))+WriteInt(ydif))), ids_ = [ID]   )
	elif typ == 21:
		ID=ReadByte(data)			
		xdif=ReadByte(data)		
		ydif=ReadByte(data)	
		if not checkid(addr, ID):
			add("Hacker Attack")
		else:
			if settings['Svlastmove'] == 1:
				if (time() - player[addr]['lastmove']) < (settings['Svlastmove']/1000): 
					if player[addr]['lastmove'] <= time():
						player[addr]['lastmove'] = time()

			player[addr]['x'] = (player[addr]['x'] - xdif - 128)
			player[addr]['y'] = (player[addr]['y'] - ydif - 128)

			#if settings['Svantilag']: 
			for pl in player.values(): 
				if pl['ID'] <> ID:
					sendall(((((WriteByte(15)+WriteByte(ID))+WriteInt(player[addr]['x']))+WriteInt(player[addr]['y']))+WriteByte(round)), ids_ = [ID]   )

			sendall(((((WriteByte(21)+WriteByte(pl['ID']))+WriteInt(player[addr]['x']))+WriteInt(player[addr]['y']))), ids_ = [ID]   )

	elif typ == 22:
		ID=ReadByte(data)			
		xdif=ReadByte(data)		
		ydif=ReadByte(data)	
		dir = (ReadShort(data))
		if not checkid(addr, ID):
			add("Hacker Attack")
		else:
			if settings['Svlastmove'] == 1:
				if (time() - player[addr]['lastmove']) < (settings['Svlastmove']/1000): 
					if player[addr]['lastmove'] <= time():
						player[addr]['lastmove'] = time()

			player[addr]['x'] = (player[addr]['x'] + (xdif - 128))
			player[addr]['y'] = (player[addr]['y'] + (ydif - 128))
			#if settings['Svantilag']: 
			#for pl in player.values(): 
				#if pl['ID'] <> ID:
					#sendall(((((WriteByte(15)+WriteByte(ID))+WriteInt(player[addr]['x']))+WriteInt(player[addr]['y']))+WriteByte(round)), ids_ = [ID]   )

			sendall(((((WriteByte(22)+WriteByte(ID))+WriteInt(xdif))+WriteInt(ydif))+WriteShort(dir)), ids_ = [ID]   )
	elif typ == 23:
		ID=ReadByte(data)			
		xdif=ReadByte(data)		
		ydif=ReadByte(data)	
		dir = (ReadShort(data))
		player[addre]["x"] = (xdif + player[addre]["x"])
		player[addre]["y"] = (ydif + player[addre]["y"])
		player[addre]["dir"] = dir
		xd = (xdif )
		yd = (ydif )
		sendall(((((WriteByte(23)+WriteByte(ID))+WriteByte(xd))+ WriteByte(yd))+WriteShort(dir)), imp = 1, ids_ =[ID])


	elif typ == 91:
		saying = ReadByte(data)
		id = ReadByte(data)
		msg = ReadLine(data)
		limp = ReadShort(data)
		if not id in mutez:
			if getlimp(limp, addre) == 1:
				sendall(( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine(str(player[ids[id]]['name']) + " says: " + str(msg))), imp = 1)
		else:
			if getlimp(limp, addre) == 1:
				sendone(addre,( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("You are muted...")), imp = 1)
	elif typ == 102:
		ID=ReadByte(data)			
		team=ReadByte(data)			
		limp=ReadShort(data)

		if getlimp(limp, addre) == 1:
			if checkid(addre,ID) == 1:
				player[addre]['team'] = team
				sendall(((WriteByte(102) + WriteByte(ID)) + WriteByte(team)), imp = 1, ids_ = [ID])
				sendall(( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine(str(player[ids[ID]]['name']) + " Joined Team ID: " + str(team))), imp = 1)
			else:
				add("Hacker Attack: Team")
	elif typ == 103:
		ID=ReadByte(data)			
		look=ReadByte(data)			
		limp=ReadShort(data)

		if getlimp(limp, addre) == 1:
			if checkid(addre,ID) == 1:
				player[addre]['look'] = look
				player[addre]['ready'] = 1
				if len(ids) <=2:
					startround(0)

				sendall(((WriteByte(103) + WriteByte(ID)) + WriteByte(look)), imp = 1, ids_ = [ID])
			else:
				add("Hacker Attack: Look")
	#elif typ == 104:
		#print 104

	elif typ == 108:
		rpw = ReadLine(data)
		script = ReadLine(data)
		limp = ReadShort(data)
		if getlimp(limp, addre) == 1:

			parsecmd(addre, rpw, script)

	elif typ == 250:
		typ2 = ReadByte(data)

		if typ2 == 0:
			#250:0 Info Request
			#Returns 250, 1, sv_name, has_pass, map, current_pl, max_pl, fow, wm
			curnum = len(ids)
			udp = ( ( ( ( ( ( ( ( ( WriteByte(250) + WriteByte(1)) + WriteLine(settings['Svname'])) + WriteByte(settings['Svispw'])) + WriteLine(settings['Svmap'])) + WriteByte(curnum)) + WriteByte(settings['Svmaxpl'])) + WriteByte(settings['Svfow'])) + WriteByte(settings['Svwm'])) + WriteLine(settings['version']))
			sendone(addre, udp)


		if typ2 == 250:
			password = ReadLine(data)
			name = ReadLine(data)
			ip = ReadInt(data)
			port = ReadInt(data)
			host = addre[0]
			hport = addre[1]
			id = 1
			while id < 30:
				try:
					print ids[id]
				except:
					break
				id = id + 1
			ids[id] = addre
			thpl = {"name": name,
				"ID": id,
				"ip": host,
				"port": hport,
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
				"frags": 0,
				"deads": 0,
				"sweapon": ([0] * 18),
				"sammo": ([0] * 18),
				"sammoin": ([0] * 18),
				"gameadmin": 0,
				"ready": 0,
				"slot": 0,
				"ammor": 0,
				"ping": 0,
				"playing": 0,
				"lastmove": 0,
				"lastping": 0,
				"hostages": []}
			player[addre] = thpl
			udp = ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( WriteByte(250) + WriteByte(3)) + WriteByte(1)) + WriteByte(id)) + WriteInt(ip)) + WriteInt(port)) + WriteLine("b 0.1.0.4")) + WriteLine(mapcode_)) + WriteLine(settings['Svmap'])) + WriteByte(0)) + WriteLine(settings['Svname'])) + WriteByte(settings['Svmaxpl'])) + WriteByte(settings['Svfow'])) + WriteByte(settings['Svwm'])) + WriteByte(game['round'])) + WriteByte(game['round'])) +WriteShort(game['t_score'])) + WriteShort(game['ct_score'])) + WriteByte(game['t_winrow'])) + WriteByte(game['ct_winrow'])) +WriteInt(game['bombtimer'])) + WriteByte(1))
			sendone(addre, udp, imp = 1)
			print player[ids[id]]['name'] + " has joined the server"

			for pl in player.values():
				if pl <> player[ids[id]]:
					sendone(ids[pl['ID']], ((((WriteByte(101)+WriteLine(player[ids[id]]['name']))+WriteInt(IntIP(player[ids[id]]['ip']))) + WriteInt(player[ids[id]]['port'])) + WriteByte(id)), imp = 1)
					#udp = ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( WriteByte(100) + WriteByte(2)) + WriteLine(pl['name'])) + WriteByte(pl['team'])) + WriteByte(pl['look'])) + WriteByte(pl['vip'])) + WriteInt(IntIP(pl['ip']))) + WriteInt(pl['port'])) + WriteByte(pl['health'])) +WriteInt(pl['x'])) + WriteInt(pl['y'])) +WriteShort(pl['dir'])) + WriteShort(pl['frags']+32767)) + WriteShort(pl['deads']+32767)) + WriteByte(0)) + WriteByte(0)) + WriteByte(pl['gameadmin']))
					#sendone(addre, udp, imp = 1)

		elif typ2 == 4:
			var1 = ReadLine(data)
			typ3 = ReadByte(data)
			id = typ3
			for pl in player.values():
				if pl['ID'] != id:
					udp = ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( WriteByte(100) + WriteByte(pl['ID'])) + WriteLine(pl['name'])) + WriteByte(pl['team'])) + WriteByte(pl['look'])) + WriteByte(pl['vip'])) + WriteInt(IntIP(pl['ip']))) + WriteInt(pl['port'])) + WriteByte(pl['health'])) +WriteInt(pl['x'])) + WriteInt(pl['y'])) +WriteShort(pl['dir'])) + WriteShort((pl['frags']+32767))) + WriteShort((pl['deads']+32767))) + WriteByte(pl['sweapon'][7])) + WriteByte(pl['sweapon'][8])) + WriteByte(pl['gameadmin']))
					sendone(addre, udp, imp = 1)
					#sendone(ids[pl['ID']], (((WriteByte(101)+WriteLine(var1))+WriteInt(IntIP(addre[0]))) + WriteInt(addre[1])) + WriteByte(typ3), imp = 1)

					sendone(ids[pl['ID']], (((WriteByte(30)+WriteByte(pl['ID']))+WriteByte(pl['slot'])) + WriteByte(pl['sweapon'][pl['slot']])), imp = 1)


			sendone(addre,( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("Welcome to the [TGV] Chat Server")), imp = 1)
	elif typ == 251:
		udp = WriteByte(251)
		sendone(addre, udp)
		for pl in player.values():
			if pl['ID'] != player[addre]['ID']:
				sendone(addre, ( ( WriteByte(253) + WriteByte(pl['ID'])) + WriteInt(pl['ping'])))

	elif typ == 252:
		mode = ReadByte(data)
		id = ReadByte(data)
		limp = ReadShort(data)
		rest = ReadByte(data)
		if checkid(addre, id) == 1:
			if mode == 0:
				add(player[ids[id]]["name"] + "has left the server...")
				for addr in player:
					if player[addr]['ID'] == id:
						impsend(addr, limp)
						kill(addre)
						sendall(((WriteByte(252)+WriteByte(0))+WriteByte(id)), ids_=[id], imp=1 )
						break
			elif mode == 1:
				for addr in player:
					if player[addr]['ID'] == id:
						impsend(addre, limp)
						sendall(((WriteByte(252)+WriteByte(1))+WriteByte(id)), ids_=[id], imp=1 )
						kill(addre)
						add(player[ids[id]]["name"] + "Pinged Out (Client)...")
						break

			elif mode == 2:
				add(player[ids[id]]["name"] + ": Hacker Attack (Kicked)")
			elif mode == 3:
				add(player[ids[id]]["name"] + ": Attempted Server Close (Closed)")
			elif mode == 4:
				add(player[ids[id]]["name"] + ": Hacker Attack (CheatKicked)")
	elif typ == 253:
		id = ReadByte(data)
		ping = ReadInt(data)
		if checkid(addre, id) == 0:
			add("Hacker Attack (Ping Data)")
		else:
			for pl in player.values():
				sendone(addre, ( ( WriteByte(253) + WriteByte(pl['ID'])) + WriteInt(pl['ping'])), imp = 1)
	elif typ == 255:

		limp = ReadShort(data)
		#if getlimp(limp, addre) == 1:
		if impsends.has_key(limp):
			for limp in pingids:
				ping = 0
				if settings['Svmaxping']:
					if player[addre]['ping'] >= settings["Svmaxping"]:
						if ping >= settings["Svmaxping"]:
							sendall(((WriteByte(252) + WriteByte(2)) + WriteByte(player[addre]['ID'])), imp = 1)
							add(player[addre]["name"] + ": Kicked (Too High Ping)")
							kill(addre)
				else:
					player[addre]['ping'] = ping
					sendall(((WriteByte(253)+WriteByte(player[addre]["ID"]))+WriteInt(ping)), imp=1 )
					pingids.remove(limp)
					impsend(addre, limp)
	#else:
		#thedataz.append(str(typ) + "\n" + handle(typ, data) + "\n" + data + "\n#########\n")
		#sendone(addre, data, imp=1)
		#print data
		#a = ReadByte(data)
		#print a
	a = handle(typ, data)
	if a <> "":
		thedataz.append(str(typ) + "\n" + handle(typ, data) + "\n" + data + "\n#########\n")
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



def sendone(addr, data, time_ = 0, imp = 0, impcount = 2, imptime = 0):
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
	if player[addr]['ID'] in mutez:
		mutez.remove(player[addr]['ID'])
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
	dellimp(addr)



def impid():
	global limp
	if (limp == 65025):
		limp = 0
	else:
		limp += 1
	return limp

def getlimp(limp, addre):
	if addre in limpz:
		if limp in limpz[addre]:
			return 0
		else:
			limpz[addre].append(limp)
			return 1
	else:
		limpz[addre] = [limp]
		return 1
def dellimp(addr):
	if addr in limpz:
		for i in range(1, 99999):
			try:
				limpz[addr].remove(i)
			except:
				break

def update2():
	player[addre]["timeout"] = time()
	for addr in player.keys():
		if ((time() - player[addr]["timeout"]) > settings["timeout"]):
			add((str(player[addr]["ip"]) + ": Pingtimeout (Server)"))
			sendall(((WriteByte(252) + WriteByte(2)) + WriteByte(player[addr]["ID"])), imp=1)
			kill(addr)

			#sendone(( ( ( (WriteByte(91) + WriteByte(3)) + WriteByte(0)) + WriteLine("Please come back at another time...")) + WriteShort(324)), imp = 1)

		elif ((player[addr]["lastping"] <= (time() - 1)) and (addr != addre)):
			player[addr]["lastping"] = time()
			pingids.append(sendone(addr, (((((WriteByte(51) + WriteByte(255)) + WriteInt(-1000)) + WriteInt(-1000)) + WriteByte(52)) + WriteByte(0)), imp=1, impcount=0))

def update():
	global grenades
	player[addre]["timeout"] = time()
	for addr in player.keys():
		if ((time() - player[addr]["timeout"]) > settings["timeout"]):
			add((str(player[addr]["ip"]) + ": Pingtimeout (Server)"))

			sendall(((WriteByte(252) + WriteByte(2)) + WriteByte(player[addr]["ID"])), imp=1)
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
	global mapcode_
	add((("Loading map (" + settings["Svmap"]) + ")"), 1, 0)
	start = time()
	(code, themap,) = loadmap(settings["Svmap"])
	if code:
		add((("map loaded in " + str((time() - start))) + " seconds"), 1, 0)
		map_ = themap
		mapcode_ = themap['code']
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
		return ""
	elif typ == 253:
		ID=ReadByte(udp)
		ping=ReadInt(udp)
		#server.sendto(WriteByte(251), addr)
		return "OPing From :" + str(ID) + " is " + str(ping)
	else:
		return ""
def limprep(limp):
	try:
		a = limpz[limp]
		return 1
	except:
		limpz[limp] = '1'
		return 0

if (__name__ == "__main__"):
	load()
	if (map() and start()):
		atexit.register(quit)
		ini()
		run()

# local variables:
# tab-width: 4
