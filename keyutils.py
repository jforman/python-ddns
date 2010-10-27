#!/usr/bin/env python

def read_tsigkey(tsigkeyfile,keyname):
    try:
        keyfile = open(tsigkeyfile)
        keystruct = keyfile.read()
        keyfile.close()
    except IOError:
        print "A problem was encountered opening your keyfile."
        return 1

    import re
    import sys
    
    try:
        keydata = re.search(r"key \"%s\" \{(.*?)\}\;" % keyname, keystruct, re.DOTALL).group(1)
    except AttributeError:
        print "no key found"
        return 1
        
    algorithm = re.search(r"algorithm ([a-zA-Z0-9_-]+?)\;", keydata, re.DOTALL).group(1)
    tsigsecret = re.search(r"secret \"(.*?)\"", keydata, re.DOTALL).group(1)
        
    print "algo: %s" % algorithm
    print "tsigsecret: %s" % tsigsecret
    
    return (algorithm, tsigsecret)
