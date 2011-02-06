#!/usr/bin/env python

# Example: ./add_cname.py --keyfile ddns.key --keyname ddns-key --orig puppet.test.jeffreyforman.net --dest www.example.com --server dns1

import dns.query
import dns.reversename
import dns.tsigkeyring
import dns.update
import re
import sys

import keyutils

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--dest", dest="dest",
                  help="Destination of the CNAME.",
                  type="string")
parser.add_option("--orig", dest="orig",
                  help="Name of the CNAME.",
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
parser.add_option("--ttl",dest="ttl",
                  help="Time to Live (in Seconds). Default: 86400",
                  type="int",default=86400)

(options, args) = parser.parse_args()

orig_hostname = re.search(r"(\w+).(.*)", options.orig).group(1)
orig_domain = re.search(r"(\w+).(.*)", options.orig).group(2)

print "CNAME record to be added: %s, CNAME points to: %s, DNS Server: %s" % (options.orig, options.dest, options.dns_server)

(algorithm, tsigsecret) = keyutils.read_tsigkey(options.key_file,options.key_name)

keyring = dns.tsigkeyring.from_text({
     'ddns-key' : tsigsecret
})

update = dns.update.Update(orig_domain, keyring = keyring)
update.replace(orig_hostname, options.ttl, 'CNAME', "%s." % options.dest)

print "--- Updating CNAME Record"
response = dns.query.tcp(update,options.dns_server)

print "Output: %s" % response
