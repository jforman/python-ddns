#!/usr/bin/env python

import dns.query
import dns.zone
import sys

print "args: %s %s" % (sys.argv[1], sys.argv[2])
try:
    z = dns.zone.from_xfr(dns.query.xfr(sys.argv[1], sys.argv[2]))
    print "after transfer"
    names = z.nodes.keys()
    names.sort()
    for n in names:
        print z[n].to_text(n)
except dns.exception.FormError:
    print "The transfer encountered a problem."
