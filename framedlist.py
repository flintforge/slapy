#!/env/bin/python

# Date:<2016/05/28 23:53:19>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

# frame strings in a list with prefix, suffix
# todo : option to activate validation rule for the inner string

import sys,re,getopt


defaultfile="servers.d"

# unused
validIpRgx = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
def validIp(ip):
    if( not re.match( validIpRgx, ip )):
        raise Exception("not a valid hostname %s"% ip)


#todo left and right sep + iterator
def framedList(prefix,suffix,slist,validationRule=None,separator="" ):

    n=0
    framedlist=[]
    for string in slist:
        if validationRule:
            validationRule.valid(string)
        n+=1
        framedlist.append("%s%i %s%s%s%s" #fixme
            %(prefix,n,separator,string.strip(),separator,suffix))

    return ("\n".join(framedlist))

if __name__ == '__main__':
        args = sys.argv[1:]
        if len(args) > 0:
                file = defaultfile
                suffix=prefix=""
                try:
                    opt, args = getopt.getopt(args,"p:s:f:")
                except:
                    print ("build -p prefix -s suffix -f file")
                    sys.exit(0)

                for opt, optarg in opt:
                        if opt in ('-s','--suffix'):
                                suffix = optarg

                        elif opt in ('-p','--prefix'):
                                prefix = optarg

                        elif opt in ('-f'):
                                file = optarg
                        else:
                            print ("build -p predix -s suffix -f file")
                            sys.exit(0)

                with open(file,'r') as f:
                    slist = f.read().strip().split('\n')

                print framedList(prefix,suffix,slist)

        else:
            print ("build -p prefix -s suffix -f file")
            sys.exit(0)




