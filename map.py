#! /usr/bin/env python
# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from bb_udp import * 
from os.path import isfile 
map = {'code': '99856x63$160312%28176708',
 'name': 'de_dust',
 2: [],
 1: [],
 'collision': [[]],
 'maxx': 0,
 'maxy': 0,
 'vipspawn': [0,
              0],
 'vipescape': [],
 'hostages': {},
 'hostagecount': 0,
 'resethostages': {},
 'hostagerescue': []}
mapdir = 'maps/'
mapheader = "Unreal Software's Counter-Strike 2D Map File"
mapcheck = 'ed.erawtfoslaernu'
_3rr0r = ''

def loadmap(mapname):
    global _3rr0r
    map['name'] = mapname
    map['typ'] = 0
    if (not isfile(((mapdir + mapname) + '.map'))):
        _3rr0r = 'Map does not exist!'
        return (0,
         _3rr0r)
    mapc = open(((mapdir + mapname) + '.map'), 'rb')
    mapname = mapc.read()
    mapc.close()
    if (not (ReadLine(mapname) == mapheader)):
        _3rr0r = 'Mapheader wrong!'
        return (0,
         _3rr0r)
    for i in range(9):
        ReadByte(mapname)

    for i in range(10):
        ReadInt(mapname)

    for i in range(10):
        ReadLine(mapname)

    map['code'] = ReadLine(mapname)
    ReadLine(mapname)
    maptilesc_loaded = ReadByte(mapname)
    maxx = ReadInt(mapname)
    maxy = ReadInt(mapname)
    map['maxx'] = maxx
    map['maxy'] = maxy
    ReadLine(mapname)
    ReadInt(mapname)
    ReadInt(mapname)
    ReadByte(mapname)
    ReadByte(mapname)
    ReadByte(mapname)
    if (not (ReadLine(mapname) == mapcheck)):
        _3rr0r = 'Wrong mapcheck'
        return (0,
         _3rr0r)
    tile_modes = ([0] * (maptilesc_loaded + 1))
    for i in range((maptilesc_loaded + 1)):
        tile_modes[i] = ReadByte(mapname)

    map['map'] = []
    for i in map['map']:
        print i

    for i in range((maxx + 1)):
        cache = []
        for o in range((maxy + 1)):
            bytecache = ReadByte(mapname)
            if (bytecache > maptilesc_loaded):
                bytecache = 0
            else:
                bytecache = tile_modes[bytecache]
            cache.append(bytecache)

        map['map'].append(cache)

    ec = ReadInt(mapname)
    for i in range(ec):
        ReadLine(mapname)
        typ = ReadByte(mapname)
        x = ReadInt(mapname)
        y = ReadInt(mapname)
        ReadLine(mapname)
        for i in range(10):
            ReadInt(mapname)
            ReadLine(mapname)

        if (typ == 0):
            map[1].append((x,
             y))
        elif (typ == 1):
            map[2].append((x,
             y))
        elif (typ == 2):
            map['typ'] = 1
            map['vipspawn'] = [x,
             y]
        elif (typ == 3):
            if (map['hostagecount'] <= 256):
                map['typ'] = 2
                map['hostages'][map['hostagecount']] = [map['hostagecount'],
                 (x * 32),
                 (y * 32),
                 0,
                 -1,
                 100,
                 0]
                map['hostagecount'] += 1
        elif (typ == 4):
            map['hostagerescue'].append(((x - 1),
             (y - 1)))
            map['hostagerescue'].append((x,
             (y - 1)))
            map['hostagerescue'].append(((x + 1),
             (y - 1)))
            map['hostagerescue'].append(((x - 1),
             y))
            map['hostagerescue'].append((x,
             y))
            map['hostagerescue'].append(((x + 1),
             y))
            map['hostagerescue'].append(((x - 1),
             (y + 1)))
            map['hostagerescue'].append((x,
             (y + 1)))
            map['hostagerescue'].append(((x + 1),
             (y + 1)))
        elif (typ == 5):
            map['typ'] = 3
        elif (typ == 6):
            map['vipescape'].append((x,
             y))

    for i in map['hostages']:
        map['resethostages'][i] = map['hostages'][i][:]

    delStream(mapname)
    return (1,
     map)


if (__name__ == '__main__'):
    map_ = raw_input('map name: ')
    if loadmap(map_):
        print ('name: ' + map['name'])
        print ('code: ' + map['code'])
        print 'Terror Spawns:'
        for i in map[1]:
            print ((('X: ' + str(i[0])) + ' Y: ') + str(i[1]))

        print 'CT Spawns:'
        for i in map[2]:
            print ((('X: ' + str(i[0])) + ' Y: ') + str(i[1]))

        print 'maploading finished'
    else:
        print (("Couldn't load map (" + _3rr0r) + ')')

# local variables:
# tab-width: 4
