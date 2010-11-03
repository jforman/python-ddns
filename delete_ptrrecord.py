#!/usr/bin/env python

# Example: delete_ptrrecord.py --ip 10.30.0.54 --keyfile ddns.key --keyname ddns-key --server mydnsserver

import dns.query
import dns.tsigkeyring
import dns.update
import dns.reversename
import re
import sys

import keyutils

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--ip", dest="ip_address",
                  help="IP of the host you wish to delete.",
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

print "--- Deleting Reverse DNS Record (PTR)"
domain = dns.reversename.from_address(options.ip_address)
octetip = re.search(r"([0-9]+).(.*).$", str(domain)).group(1)
ptrdomain = re.search(r"([0-9]+).(.*).$", str(domain)).group(2)
print "domain: %s, octetip: %s, ptrdomain: %s" % (domain, octetip, ptrdomain)

print "Host to be deleted: %s, DNS Server: %s" % (domain, options.dns_server)

(algorithm, tsigsecret) = keyutils.read_tsigkey(options.key_file,options.key_name)

keyring = dns.tsigkeyring.from_text({
     'ddns-key' : tsigsecret
})

update = dns.update.Update(ptrdomain, keyring = keyring)
update.delete(octetip)

response = dns.query.tcp(update,options.dns_server)

print "Output: %s" % response
