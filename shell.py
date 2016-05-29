# Date:<2016/05/12 03:55:59>
# author : phil estival <infos@caern.net>
# This script is distributed under the terms of the GPL v2 license.

# shell command called as subprocess

from subprocess import Popen, PIPE

class ShellCommand:
    def __init__(self,cmd=''):
        self.cmd=cmd
        self.out=''
        self.returncode=-7
        self.errors=0

    def run(self,cmd='', args=[]):
        if not cmd:
            if not self.cmd:
                print 'empty command'
                return
            else : cmd=self.cmd

        self.cmd = cmd + " " + ' '.join(args)
        p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
        self.out, self.errors = p.communicate()
        self.returncode = p.returncode
        return (self.returncode, self.out, self.errors)

    @staticmethod
    def call(cmd='', args=[]):
        if not cmd:
            print 'empty command'
            return

        cmd + " " + ' '.join(args)
        p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
        out, errors = p.communicate()
        return (p.returncode, out, errors)

