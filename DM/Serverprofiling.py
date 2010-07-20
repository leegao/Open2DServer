import profile
import DMServer
from DMServer import *

#Uncomment to run test.
#profile.run("DMServer.loadserver()", "DMProfile.txt")

import pstats
p = pstats.Stats('DMProfile.txt')
p.sort_stats('cumulative')
p.print_stats()
raw_input('')