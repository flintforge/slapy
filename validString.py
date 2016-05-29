#
# regex validation rules
#

import re

class StringValidation():
    @staticmethod
    def validate(string):
        pass

class IPvalidation(StringValidation):
    validIpRgx = "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    validIpRgxLine = "^"+validIpRgx+"$"

    @staticmethod
    def validate(string):
           if( not re.match( IPvalidation.validIpRgx, string )):
            raise Exception("invalid IP %s"% string)
