#!/env/bin/python

# Date:<2016/05/30 00:36:54>
# author : phil estival <pestival@wearelearning.com>
# This script is distributed under the terms of the GPL v2 license.

# this is a list of operations conducted on a server pool
# such as :

# with ansible :
# - ask uptime
# - push last version of a payload
# - update munin pool
# - start servers
# - ensure a log line as occured in all the servers

# through ssh :
# - copy haproxy.cfg, check it, run it

# TODO :
# - fixme. generate the ips from the iph
# - argparse

import os,sys,shutil,getopt

from tput import *
from shell import ShellCommand as Shell
sh=Shell()
from checkrun import *
from genmuninpool import genmuninpool
from tput import OK,FAIL
from datetime import datetime
from config import *


def messageline(msg):
    sys.stdout.write( '%-30s'% msg)
    sys.stdout.flush()


class Operations :
    def __init__ (self,pool,hosts,muninconfd,ansible_realm,haproxyhost,haproxypath, debug=False):
        self.pool = pool
        self.HOSTS = hosts
        self.MUNINCONFD = muninconfd
        self.ANSIBLE_REALM = ansible_realm
        self.HaProxyHost = haproxyhost
        self.HaProxyPath = haproxypath
        self.debug=debug

    def pushMuninPool(self):
        messageline("generate muninpool")
        try:
            config=genmuninpool(self.pool, "%s/%s.iph"%(self.HOSTS,self.pool) )

            print "Generated munin pool :"
            print '---\n%s\n---'%config
            muninconf="%s/%s.%s"%(self.HOSTS,self.pool,"munin")
            open(muninconf,"w").write(config)
            shutil.copy2(muninconf,self.MUNINCONFD)
            CheckRun("restart munin","sudo /etc/init.d/munin restart")
            #CheckRun("restart munin","su - munin --shell=/bin/bash -c /usr/share/munin/munin-update")

        except Exception,e:
            printFailed(e,self.debug)

    # need a way to ensure this has occured
    def updateAnsiblePool(self):
        linemessage("copy pools in ansible directory")
        shutil.copy2("%s/%s.ips"%(self.HOSTS,self.pool), self.ANSIBLE_REALM)
        shutil.copy2("%s/%s.new.ips"%(self.HOSTS,self.pool), self.ANSIBLE_REALM)
        print OK

    def uptime(self, pool=None) :
        CheckRun("ansible uptime on new pool",
            ansible+"/ap %s uptime -u ansible" % (pool or self.pool))

    def updateHA(self):
        CheckRun("regen haproxy config", "./haproxy/genHAconfig.py")
        CheckRun("send haconfig to silver",
            "scp haproxy/haproxy.cfg %s:%s"%(self.HaProxyHost,self.HaProxyPath))
        CheckRun("load balancer configuration check",
            "ssh %s /etc/init.d/haproxy.sh checkconf"%(self.HaProxyHost))
        CheckRun("restart load balancer",
            "ssh %s /etc/init.d/haproxy.sh restart"%(self.HaProxyHost))

    def putpayload(self,pool,targetdir,app):
        """
        dispatch a file to to the pool
        start the server
        wait for a message to appear in the logs
        """
        CheckRun("dispatch wal to the pool",
            ansible+"/ap-up %s %s %s -u ansible"%(pool,app,targetdir)
        )
        timestamp = datetime.now().strftime('%Y.%m.%d_%H-%M-%S')
        CheckRun("start servers ", ansible+"/ap %s startserver" %pool)
        CheckRun("ensure app is deployed", ansible+"/ap %s checkAppDeployed" %pool)



if __name__ == '__main__':
    def usage(prog):
        print " usage : gridoperations [-q quiet] op [pool]"
        exit (1)

    prog = sys.argv[0]
    args = sys.argv[1:]
    
    if len(args) < 1:
        usage(prog)
    else: 
        pool=""
        GridOp = Operations (pool,HOSTS,MUNINCONFD,ANSIBLE_REALM,HaProxyHost,HaProxyPath)
        try:
            opt, args = getopt.getopt(args,"p:aw:qt")
        except:
            usage(prog)

        for opt, optarg in opt:
            if opt in ('-q'):
                CheckRun.quiet=True
                continue
            if opt in ('-a'):
                GridOp.updateHA()
            elif opt in ('-p','--prefix'):
                pool = optarg
            elif opt in ('-w','--wal') :
                GridOp.putLastWalRelease(optarg)
            elif opt in ('-t') :
                GridOp.test()
            elif opt in ('-f'):
                file = optarg
            else:
                usage(arg[0])
                sys.exit(0)



