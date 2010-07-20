#-----------------------------------------------------------------#
# Blitz Basic cType streamers
#-----------------------------------------------------------------#
from struct import pack, unpack

#Specials:
def IntIP(ip):
	bytes = ip.rsplit(".")
	ip = ""
	for i in bytes:
		ip = chr(int(i)) + ip
	return ReadInt(ip)

def DottedIP(int):
	hex = WriteInt(int)
	ip = ""
	for i in hex:
		ip = str(ord(i)) + "." + ip
	return ip[:-1]

def delStream(stream):
	if readcount.has_key(stream):
		del readcount[stream]
#Writes:
def WriteShort(short):
	return pack("H", short)

def WriteInt(int):
	return pack("i", int)

def WriteFloat(float):
	return("f", float)

def WriteByte(Byte):
	if Byte < 0: Byte = 0
	if Byte > 255: Byte = 255
	return chr(Byte)

def WriteLine(Line):
	return Line + chr(13) + chr(10)

def WriteString(string):
	return WriteInt(len(string)) + string


#Reades:
readcount = {}
def get(string):
	if string in readcount:
		return string[readcount[string]:]
	else:
		readcount[string] = 0
		return string

def update(string, ln):
	readcount[string] += ln
	if readcount[string] >= len(string):
		del readcount[string]

def ReadShort(stream):
	string = get(stream)
	if len(string) >= 2:
		hex = string[:2]
	else:
		return 0
	dez = unpack("H", hex)[0]
	update(stream, len(hex))
	return dez
def ReadLong(stream):
	string = get(stream)
	if len(string) >= 4:
		hex = string[:4]
	else:
		return 0
	dez = unpack("L", hex)[0]
	update(stream, len(hex))
	return dez
def ReadInt(stream):
	string = get(stream)
	if len(string) >= 4:
		hex = string[:4]
	else:
		return 0
	dez = unpack("i", hex)[0]
	update(stream, len(hex))
	return dez


def ReadFloat(stream):
	string = get(stream)
	if len(string) >= 4:
		hex = string[:4]
	else:
		return 0
	dez = unpack("f", hex)
	update(stream, len(hex))
	return dez

def ReadByte(stream):
	string = get(stream)
	byte = ord(string[0])
	update(stream, 1)
	return byte
	
def ReadLine(stream):
	string = get(stream)
	line =  string.split(chr(13) + chr(10), 1)[0]
	update(stream, len(line) + 2)
	return line

def ReadString(stream, ln):
	#ln = ReadInt(stream)
	string = get(stream)
	string = string[:ln]
	update(stream, len(string))
	return string

