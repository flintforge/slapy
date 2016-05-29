#!/env/bin/python

# concat haproxy global config
# with backends configs and the associated servers ip

import os,sys,getopt
from framedlist import framedList

haproxyd="haproxy/haproxy.d"
haproxybasecfg="haproxy/haproxy.conf"
hacfg="haproxy/haproxy.cfg"
hosts="haproxy/hosts"

class HAconfig:
    def __init__(self,
            haproxyd = "haproxy/haproxy.d",
            haproxybasecfg="haproxy/haproxy.conf",
            hacfg="haproxy/haproxy.cfg",
            hosts="haproxy/hosts",
            prefix="     server ",
            sufix=":8080 check maxconn 350") :

        self.haproxyd=haproxyd
        self.haproxybasecfg=haproxybasecfg
        self.hacfg=hacfg
        self.hosts=hosts
        self.prefix = prefix
        self.sufix = sufix

    def generate(self) :

        with open(self.haproxybasecfg,'r') as f:
            habasecfg = f.read()

        backends = os.listdir(self.haproxyd)
        print backends
        #bkcfg=[]
        bkcfg=""

        for b in backends :
            be = b.split('.')
            backend_name = be[0]
            pool = be[1]

            with open("%s/%s"%(self.haproxyd,b),'r') as f:
                backcfg = f.read()
            with open("%s/%s.ips"%(hosts,pool)) as f:
                serverlist = f.read().strip().split('\n')
                slist=framedList(self.prefix + pool,self.sufix,serverlist)
            bkcfg+=backcfg + slist +'\n'

        open(hacfg, "w").write(habasecfg+bkcfg)
        print "written"
        return habasecfg+bkcfg


"""   main   """
if __name__ == '__main__':
    HAconfig().generate()


