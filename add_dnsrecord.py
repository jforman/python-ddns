#!/usr/bin/env python

# Example: add_dnsrecord.py --fqdn host101.testzone.example.com --ip 10.30.0.101 --keyfile ddns.key --keyname ddns-key --server mydnsserver

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
parser.add_option("--fqdn", dest="fqdn",
                  help="FQDN of the host you wish to add.",
                  type="string")
parser.add_option("--ip", dest="ip_address",
                  help="IP address of host you wish to add.",
                  type="string")
parser.add_option("--keyfile", dest="key_file",
                  help="File containing the TSIG key.",
                  type="string")
parser.add_option("--keyname", dest="key_name",
                  help="TSIG key name to use for the DDNS update.",
                  type="string")
parser.add_option("--server", dest="dns_server",
                  help="DNS server to query.",
                  type="string")


(options, args) = parser.parse_args()

hostname = re.search(r"(\w+).(.*)", options.fqdn).group(1)
domain = re.search(r"(\w+).(.*)", options.fqdn).group(2)

print "Host to be updated: %s, IP: %s, DNS Server: %s" % (options.fqdn, options.ip_address, options.dns_server)

(algorithm, tsigsecret) = keyutils.read_tsigkey(options.key_file,options.key_name)

keyring = dns.tsigkeyring.from_text({
     'ddns-key' : tsigsecret
})

update = dns.update.Update(domain, keyring = keyring)
update.replace(hostname, 300, 'A', options.ip_address)

response = dns.query.tcp(update,options.dns_server)

print "Output: %s" % response
