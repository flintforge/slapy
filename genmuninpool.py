#!/env/bin/python
#!/bin/bash
# Date:<2016/05/28 23:55:09>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

# given a file with a list of couple (ip hosts)
# generate a munin.d/config

# [pool;poolX]
#    address 10.0.0.1
#    use_node_name yes
#

import sys,re,getopt,traceback
from validString import IPvalidation

def genmuninpool(group,file) :
    if not group:
       sys.exit("missing group!")
    elif not file:
       sys.exit("missing file!")
    else:
            with open(file,"r") as F:
                hosts=[]
                matched=False
                #validate the file
                for line in F:
                    line = line.rstrip()
                    m = re.search('\s*((\d|\.)+)\s*(\w+)\s*',line)
                    if m :
                        matched=True
                        ip = m.group(1)
                        host = m.group(3)
                        IPvalidation.validate(ip)
                        hosts.append((host,ip))
                # the config
                if len(hosts) is 0 :
                    raise Exception("Empty hosts list !")
                config=''
                for h in hosts :
                    config+='[%s;%s]\n'%(group,h[0])\
                        + "\taddress %s\n"%h[1]\
                        + "\tuse_node_name yes\n"
                return config
                if not matched:
                    sys.exit("no match. no ip/host pairs found")


def usage() :
    print " -g groupname -f file"
    sys.exit(1)

if __name__ == '__main__':
    args = sys.argv[1:]
    file = None
    group = None
    if len(args)>0 :
        try:
            opt,args = getopt.getopt(args, "g:f:")
        except:
            usage()
            sys.exit(1)

        for opt,optarg in opt:
            if opt in ('-g','--group'):
                group=optarg
            if opt in ('-f','--file'):
                file=optarg

        print genmuninpool(group,file)

    else:
        usage()

