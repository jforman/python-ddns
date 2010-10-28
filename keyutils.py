#!/usr/bin/env python

import sys
import re

def read_tsigkey(tsigkeyfile,keyname):
    try:
        keyfile = open(tsigkeyfile)
        keystruct = keyfile.read()
        keyfile.close()
    except IOError:
        print "A problem was encountered opening your keyfile, %s." % tsigkeyfile
        sys.exit(1)

    try:
        keydata = re.search(r"key \"%s\" \{(.*?)\}\;" % keyname, keystruct, re.DOTALL).group(1)
        
    except AttributeError:
        print "No key %s found." % keyname
        sys.exit(1)

    algorithm = re.search(r"algorithm ([a-zA-Z0-9_-]+?)\;", keydata, re.DOTALL).group(1)
    tsigsecret = re.search(r"secret \"(.*?)\"", keydata, re.DOTALL).group(1)
    return (algorithm, tsigsecret)
