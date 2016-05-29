#!/env/bin/python
# Date:<2016/05/30 00:29:44>
# author : phil estival <pestival@wearelearning.com>
# This script is distributed under the terms of the GPL v2 license.

#
# Generate the backends part of the HA configuration
# based on what's under haproxy.d
# You can safely run this manually from one directory above

import os,sys,getopt
from framedlist import framedList

haproxyd="haproxy/haproxy.d"
haproxycfg="haproxy/haproxy.cfg"
hosts="haproxy/hosts"

prefix="     server"
# TODO : this as parameter
sufix=":8080 check maxconn 450"


def regenHaConfig() :

    with open(haproxycfg,'r') as f:
        hacfg = f.read()

    backends = os.listdir(haproxyd)
    print backends

    bkcfg=""

    for b in backends :
        be = b.split('.')
        backend_name = be[0]
        pool = be[1]

        with open("%s/%s"%(haproxyd,b),'r') as f:
            backcfg = f.read()
        with open("%s/%s.ips"%(hosts,pool)) as f:
            p = f.read().strip().split('\n')
            slist=framedList(prefix,sufix,p)
        bkcfg+=backcfg + slist +'\n'

    return bkcfg

"""   main   """
if __name__ == '__main__':
    print regenHaConfig()


