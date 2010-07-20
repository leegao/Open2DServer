def handler(data, addr):
    ans = ''
    if player.has_key(addr):
        prefix = addr[0]+'(#' + str(player[addr]['ID']) + ', ' + player[addr]['name'] + '): '
    else:
        prefix = addr[0] + ': '
    log4 = ''
    byte = ReadByte(data)
    ishandled = 1
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
#                    impsend(addr, impid)
#                    kill(addr)
#                    sendall(((WriteByte(252)+WriteByte(1))+WriteByte(id_)),ids_=[id_], imp=1 )
#                    
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
                log4 = log4 + 'Hacker Attack (ID: Shoot)'
            else:
                if player[addr]['slot'] == 2: 
                    for addr_ in player: 
                        if player[addr]['dir'] >= 0: 
                            dir = (player[addr]['dir'] - 32767)
                        else:
                            dir = (360 + player[addr]['dir'] - 32767)
                        richtung = (sin(radians(dir)), -(cos(radians(dir))))
                        distance = 4
                        stutzpunkt = (player[addr]['x'] + 16, player[addr]['y'] + 16)
                        collision = (stutzpunkt[0] + (richtung[0] * distance), stutzpunkt[1] + (richtung[1] * distance))
                        if collision[0] <= (player[addr_]['x'] + 48) and collision[0] >= (player[addr_]['x'] - 16) and collision[1] <= (player[addr_]['y'] + 48) and collision[1] >= (player[addr_]['y'] - 16) and player[addr] != player[addr_] and player[addr]['health'] > 0 and player[addr_]['health'] > 0: 
                            if settings['Svff'] or  player[addr]['team'] != player[addr_]['team']: 
                                power = (weapon_damage[50] - 3)
                                if player[addr_]['armor'] == 0:
                                    player[addr_]['health'] = player[addr_]['health'] - power 
                                else:
                                    if player[addr_]['armor'] < 150: 
                                        player[addr_]['health'] = int(player[addr_]['health']-(.65 * power)) 
                                    if player[addr_]['armor'] > 0: 
                                        player[addr_]['armor'] = player[addr_]['armor'] - power
                                        if player[addr_]['armor'] < 0: 
                                            player[addr_]['armor'] = 0 
                                    if player[addr_]['health'] <= 0 and  player[addr_]['playing']:
                                        player[addr_]['health'] = 0
                                        player[addr_]['playing'] = 0
                                        player[addr_]['sweapon'] = [0]*18
                                        player[addr_]['sammo'] = [0]*18
                                        player[addr_]['sammoin'] = [0]*18
                                        player[addr_]['deads'] = player[addr_]['deads'] + 1
                                        if player[addr]['team'] == player[addr_]['team']: 
                                            player[addr]['frags'] = player[addr]['frags'] - 1  
                                        else:
                                            player[addr]['frags'] = player[addr]['frags'] + 1
                                        sendall(((((WriteByte(41) + WriteByte(player[addr_]['ID'])) + id_) + WriteByte(50))+ WriteByte(round)), imp = 1)
                                        if player[addr_]['vip']: 
                                            startround(11)  
                                        restart = 1
                                        draw = 1
                                        for o in player.values():
                                            if o['team'] == player[addr_]['team'] and  o['health'] != 0:
                                                restart = 0  
                                            elif o['team'] != player[addr_]['team'] and  o['team'] != 0:
                                                draw = 0  
                                            if draw: 
                                                startround(0)  
                                            elif restart: 
                                                startround(player[addr]['team'] * 10)  
                                    sendall(((((((WriteByte(40) + WriteByte(player[addr_]['ID']))) + WriteByte(player[addr_]['health'])) + WriteByte(50)) + WriteByte(player[addr_]['armor'])) + WriteByte(round))) 
                        sendall(((WriteByte(10)+WriteByte(id_))+WriteByte(round)), ids_=[id_])
                         
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
            sendall(((WriteByte(10)+WriteByte(player[addr]['ID']))+WriteByte(round)), [player[addr]['ID']])
            for i in damage: 
                
                addr_ = ids[i]
                stutzpunkt = (player[addr]['x'] + 16, player[addr]['y'] + 16)
                if player[addr]['dir'] >= 0: 
                    dir = player[addr]['dir'] - 32767  
                else:
                    dir = 360 + player[addr]['dir'] - 32767
                richtung = (sin(radians(dir)), -(cos(radians(dir))))
                distance = ((player[ids[i]]['x']-player[addr]['x'])**2+(player[ids[i]]['y']-player[addr]['y'])**2)**0.5
                collision = (stutzpunkt[0]+richtung[0]*distance,stutzpunkt[1]+richtung[1]*distance)
                if collision[0] <= player[addr_]['x'] + 48 and collision[0] >= player[addr_]['x'] - 16: 
                    if settings['Svff'] or player[addr]['team'] != player[addr_]['team']:
                        if weaponmode == 2:
                            power = weapon_damage_z2[weapon]/3  
                        elif weaponmode == 1:
                            power = weapon_damage_z1[weapon]/3  
                        else:
                            power = weapon_damage[weapon]/3
                        if player[addr_]['armor'] == 0:
                                player[addr_]['health'] = player[addr_]['health'] - power  
                        else:
                                if player[addr_]['armor'] < 150: 
                                    player[addr_]['health'] = int(player[addr_]['health']-(.65 * power)) 
                                elif player[addr_]['armor'] > 0: 
                                    player[addr_]['armor'] = player[addr_]['armor'] - power
                                    if player[addr_]['armor'] < 0: 
                                        player[addr_]['armor'] = 0  
                                if player[addr_]['health'] <= 0 and  player[addr_]['playing']:
                                    player[addr_]['health'] = 0
                                    player[addr_]['playing'] = 0
                                    player[addr_]['sweapon'] = [0]*18
                                    player[addr_]['sammo'] = [0]*18
                                    player[addr_]['sammoin'] = [0]*18
                                    player[addr_]['deads'] = player[addr_]['deads'] + 1
                                    if player[addr]['team'] == player[addr_]['team']: 
                                        player[addr]['frags'] = player[addr]['frags'] - 1 
                                    else:
                                        player[addr]['frags'] = player[addr]['frags'] + 1
                                    sendall(((((WriteByte(41) + WriteByte(player[addr_]['ID'])) + WriteByte(player[addr]['ID'])) + WriteByte(50))+WriteByte(round)), imp = 1)
                                    if player[addr_]['vip']: 
                                        startround(11) 
                                    restart = 1
                                    draw = 1
                                    for o in player.values():
                                        if o['team'] == player[addr_]['team'] or  o['health'] != 0:
                                            restart = 0  
                                        elif o['team'] != player[addr_]['team'] or o['team'] != 0:
                                            draw = 0  
                                        if draw: 
                                            startround(0)  
                                        elif restart: 
                                            startround(player[addr]['team'] * 10)  
                        sendall(((((((WriteByte(40) + WriteByte(i)) + WriteByte(player[addr]['ID'])) + WriteByte(player[addr_]['health'])) + WriteByte(player[addr_]['sweapon'])) + WriteByte(player[addr_]['sammo'])) + WriteByte(round))) 
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
            dir = ReadByte(data)
            if not checkid(addr, id_):
                log4 = log4 + 'Hack : Dir'
            else:
                player[addr]['dir'] = dir
                sendall(((WriteByte(16)+ WriteByte(id_))+ WriteByte(dir))) 
        elif byte == 20: 
            id_ = ReadByte(data)
            xdif = ReadByte(data)
            ydif = ReadByte(data)
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
            dir = ReadByte(data)
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
                        sendall(((((WriteByte(22) + WriteByte(id_)) + WriteByte(xdif)) +WriteByte(ydif))+WriteByte(dir)), ids_ = [id_])
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
            dir = ReadByte(data)
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
                        sendall(((((WriteByte(23) + WriteByte(id_)) + WriteByte(xdif)) +WriteByte(ydif))+WriteByte(dir)), ids_ = [id_])
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
        elif byte == 91:
            mode = ReadByte(data)
            id_ = ReadByte(data)
            message = ReadLine(data)
            if message == "restart":
                startround(0)
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
