#!/usr/bin/env python

# Example: jforman@monitor:~/python-ddns$ ./add_dnsrecord.py --server formangate --fqdn testhost200.test.jeffreyforman.net --ip 10.30.0.200

# Add functionality to specify the kind of record. A/CNAME/NS.
# Add functionality to specify TTL.
# Add functionality on whether to create a reverse PTR record.

import dns.query
import dns.tsigkeyring
import dns.update
import re
import sys

import keyutils

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--server", dest="dns_server",
                  help="DNS server to query.",
                  type="string")
parser.add_option("--fqdn", dest="fqdn",
                  help="FQDN of the host you wish to add.",
                  type="string")
parser.add_option("--ip", dest="ip_address",
                  help="IP address of host you wish to add.",
                  type="string")

(options, args) = parser.parse_args()

hostname = re.search(r"(\w+).(.*)", options.fqdn).group(1)
domain = re.search(r"(\w+).(.*)", options.fqdn).group(2)

print "Host to be updated: %s, IP: %s, DNS Server: %s" % (options.fqdn, options.ip_address, options.dns_server)

(algorithm, tsigsecret) = keyutils.read_tsigkey("rdns.key","ddns-key")

keyring = dns.tsigkeyring.from_text({
     'ddns-key' : tsigsecret
})

update = dns.update.Update(domain, keyring = keyring)
update.replace(hostname, 300, 'A', options.ip_address)

response = dns.query.tcp(update,options.dns_server)

print "Output: %s" % response
