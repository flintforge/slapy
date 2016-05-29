#!/env/bin/python

# Date:<2016/05/30 00:34:05>
# author : phil estival <pestival@wearelearning.com>
# This script is distributed under the terms of the GPL v2 license.

# This script manage unique entries inside a file
# with optional validation of ip adresses entries

import sys,getopt

ipcheck=False

File=None

def usage(prog):
    print "usage: %s [-f file] [-a entry| -r entry | -l]" % prog

def show():
    with open(File, "ra") as F:
        for line in F:
            print line.strip()

def exists(entry):
    with open(File, "r") as F:
        L = list(F)
        L = map(str.strip, L)
        return entry in L

def remove(entry):
    if exists(entry):
        lines = filter(lambda x:x.strip()!=entry, open(File, "r"))
        lines = map(str.strip, lines)
        #print lines
        open(File, "w").write("\n".join(lines))
    else:
        sys.exit(1)

def add(entry):
    if exists(entry) :
        print "%s already in %s"%(entry,File)
        sys.exit(1)
    else:
        with open(File, "a+") as F : F.write("\n%s"%entry)
   
"""   main   """
if __name__ == '__main__':
    prog = sys.argv[0]
    args = sys.argv[1:]

    if len(args) > 0:
        try:
            opt, args = getopt.getopt(args, "if:a:r:l")
        except:
            usage(prog)
            sys.exit(0)

        for opt, optarg in opt:
            if opt in ('-i','--ip'):
                from validIp import validIp
                ipcheck=True
            elif opt in ('-f', '--file'):
                File = optarg
            elif opt in ('-a', '--add'):
                if ipcheck : validIp(optarg)
                add(optarg)
                sys.exit()
            elif opt in ('-r'):
                remove(optarg)
                sys.exit()
            elif opt in ('-l','--list'):
                show()
                sys.exit()
            else:
                usage(prog)
                sys.exit(0)
    else:
        usage(prog)


