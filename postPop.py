#!/env/bin/python

# Date:<2016/05/29 03:04:13>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

from gridoperations import *
from config import *

if __name__ == '__main__':
    def usage(prog):
        print " usage : postpop.py pool"
        exit (1)
    prog = sys.argv[0]
    args = sys.argv[1:]
    if len(args) < 1:
        usage(prog)
    else:
        pool = args[0]
        GridOp = Operations (pool,HOSTS,MUNINCONFD,ANSIBLE_REALM,HaProxyHost,HaProxyPath)
        GridOp.pushMuninPool()
        GridOp.updateAnsiblePool()
        GridOp.uptime()
        GridOp.updateHA()



