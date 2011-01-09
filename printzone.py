#!/usr/bin/env python

from optparse import OptionParser

import dns.query
import dns.zone
import socket
import sys

parser = OptionParser()
parser.add_option("--server", dest="dns_server",
                  help="DNS server to query.",
                  default = "foo",
                  type="string")
parser.add_option("--zone", dest="dns_zone",
                  help="Zone to print.",
                  default = False,
                  type="string")

(options, args) = parser.parse_args()

print "Server: %s Zone: %s" % (options.dns_server, options.dns_zone)
try:
    try:
        z = dns.zone.from_xfr(dns.query.xfr(options.dns_server, options.dns_zone))
    except socket.gaierror, e:
        print "Problems querying DNS server %s: %s\n" % (options.dns_server, e)
        sys.exit(1)

    names = z.nodes.keys()
    names.sort() # Sort the array alphabetically
    zone_xfr_array = []
    for n in names:
        current_record = z[n].to_text(n)
        for split_record in current_record.split("\n"): # Split the records on the newline
            zone_xfr_array.append([split_record]) # Add each record to our array
except dns.exception.FormError:
    print "The transfer encountered a problem. Check your zone records.\n"
    sys.exit(1)

for current_record in zone_xfr_array: # Iterate and print our DNS records array
    print current_record

