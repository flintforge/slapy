#!/env/bin/python
# Date:<2016/05/12 02:02:22>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

# grep on a piped output.
# returns when the pattern is found
# or timeout occured

import time,subprocess,select,sys,getopt,re

class grepipe :
    def __init__ (self,file,pattern,t):

        start_t = time.time()
        if pattern is "":
            raise Exception("empty pattern")

        f = subprocess.Popen(['tail','-F',filename, '-n1'],\
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)
        found=False

        pat = "^.*"+pattern+".*$"
        while True :
            elapsed = time.time() - start_t
            if elapsed > t:
                exit(1)

            if p.poll(1):
                line=f.stdout.readline()
                if re.match("^.*"+pattern+".*$", line):
                   exit (0)


#    main   
if __name__ == '__main__':

     def usage(prog):
         print "usage: %s [-f file] [-p pattern] [-t timeout]" % prog
         print " argument order matters"

     prog = sys.argv[0]
     args = sys.argv[1:]
     filename=""
     pattern=""
     t=0
     validation=None
     if len(args) > 0:
        try:
            opt, args = getopt.getopt(args,"f:p:t:")
        except Exception,e:
            usage(prog)
            sys.exit(0)

        for opt, optarg in opt:

             if opt in ('-f', '--file'):
                 filename = optarg
             elif opt in ('-p'):
                 pattern = optarg
             elif opt in ('-t','--time'):
                 t=float(optarg)
             else:
                 usage(prog)
                 sys.exit(0)

        grepipe(filename,pattern,t)

     else:
         usage(prog)


