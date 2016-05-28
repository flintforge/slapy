#!/env/bin/python

# Date:<2016/05/12 02:21:08>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

# This small script manage unique entries inside a file
# with optional validation of ip adresses entries


import sys,getopt

class Listf:

    def __init__(self, file=None, validation=None, unique=True):
        self.file = file
        self.validation=validation
        self.unique=unique

    def show(self):
        with open(self.file, "ra") as F:
            for line in F:
                print line.strip()

    def exists(self,entry):
        with open(self.file, "r") as F:
            L = list(F)
            L = map(str.strip, L)
            return entry in L

    def remove(self,entry):
        if self.exists(entry):
            lines = filter(lambda x:x.strip()!=entry, open(self.file, "r"))
            lines = map(str.strip, lines)
            #print lines
            open(self.file, "w").write("\n".join(lines))
        else:
            sys.exit(1)

    def add(self,entry):

        if self.validation:
            self.validation.validate(entry)
        if self.unique and self.exists(entry) :
            print "%s already in %s"%(entry,self.file)
            sys.exit(1)
        else:
            with open(self.file, "a+") as F : F.write("%s\n"%entry)


#    main
if __name__ == '__main__':

    def usage(prog):
        print "usage: %s [-i ipcheck] [-f file] [-a entry | -r entry | -l]" % prog
        print " argument order matters"
    prog = sys.argv[0]
    args = sys.argv[1:]

    validation=None
    if len(args) > 0:
        try:
            opt, args = getopt.getopt(args, "if:a:r:l")
        except:
            usage(prog)
            sys.exit(0)

        listf = Listf()
        for opt, optarg in opt:
            if opt in ('-i','--ip'):
                from ValidString import *
                listf.validation = IPvalidation

            elif opt in ('-f', '--file'):
                listf.file = optarg
            elif opt in ('-a', '--add'):
                listf.add(optarg)
                sys.exit()
            elif opt in ('-r'):
                listf.remove(optarg)
                sys.exit()
            elif opt in ('-l','--list'):
                listf.show()
                sys.exit()
            else:
                usage(prog)
                sys.exit(0)
    else:
        usage(prog)
