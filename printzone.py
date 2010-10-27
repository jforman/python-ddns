#!/usr/bin/env python

import dns.query
import dns.zone
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--server", dest="dns_server",
                  help="DNS server to query.",
                  type="string")
parser.add_option("--zone", dest="dns_zone",
                  help="Zone to print.",
                  type="string")

(options, args) = parser.parse_args()

print "Server: %s Zone: %s" % (options.dns_server, options.dns_zone)
try:
    z = dns.zone.from_xfr(dns.query.xfr(options.dns_server, options.dns_zone))
    names = z.nodes.keys()
    names.sort()
    for n in names:
        print z[n].to_text(n)
except dns.exception.FormError:
    print "The transfer encountered a problem."
