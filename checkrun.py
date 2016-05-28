# encoding: utf-8
# Date:<2016/05/28 23:15:48>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

# run shell commands, output [ OK ] or [ FAILED ] in colors
# and display a spinning animation while waiting for termination

import sys,signal,time,traceback
from shell import ShellCommand as sh
from tput import OK,FAIL

from threading import Thread

def signal_handler(signal, frame):
    CheckRun.endPatience=True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def linemessage(msg):
    sys.stdout.write( '%-35s %1s'% (msg,""))

class CheckRun :
    """
    let's have some fun : characters to display while waiting
    """
    #chars = ['/','-','\\']
    #pyramid=u'▁▂▃▄▅▆▇██▇▆▅▄▃▂▁'
    #boldcorners = u'▙▛▜▟'
    cornerCursor =u'⎾⌜⌝⌟⌞'
    chars = cornerCursor
    #chars = '\\|/-'
    endPatience=False
    quiet=False

    def patience(self,msg, cmd=None):
        if self.debug:
            sys.stdout.write( '%-34s %-49s %2s'% (msg,cmd, ""))
        else:
            #linemessage(msg) #if the terminal can't display carriage return
            sys.stdout.write( '%-35s %2s'% (msg,""))

        n=0
        L=len(self.chars)

        if CheckRun.quiet:
            while not self.endPatience:
                time.sleep(1)
        else:
            while not self.endPatience:
                n+=1
                #for horizontal scrolling
                #rotated = ''.join([chars[i-offset] for i in range(len(chars))])
                #rotated = chars[n:] + chars[:n]
                #sys.stdout.write( '\b'*len(rotated) + rotated)
                sys.stdout.write( '\b'+ self.chars[n%L])
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\b')

    def __init__(self,msg,cmd,output=False,debug=False):
        endPatience=False
        self.debug=debug
        t=Thread(target=self.patience,args=[msg,cmd])
        t.start()

        ret = sh.call(cmd)
        self.endPatience=True
        t.join(10) # wait 10 sec max for thread to finish
        #sys.stdout.write ('\b')

        if ret[0]:
            print FAIL
            if ret[1] : print ret[1]
            if ret[2] : print ret[2]
            sys.exit(2)
        else :
            print OK
            if output:
                print ret[1]
                print ret[2]


def printFailed(e,debug=False):
    print FAIL
    if debug: print traceback.format_exc(e)
    else: print e
    sys.exit(2)


