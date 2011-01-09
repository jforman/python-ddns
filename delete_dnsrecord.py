#!/usr/bin/env python

# Example: delete_dnsrecord.py --fqdn test53.test.mydomain.net --keyfile ddns.key --keyname ddns-key --server mydnsserver

import dns.query
import dns.tsigkeyring
import dns.update
import dns.reversename
import re
import socket
import sys

import keyutils

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--fqdn", dest="fqdn",
                  help="FQDN of the host you wish to delete.",
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

print "Host to be deleted: %s, DNS Server: %s" % (options.fqdn, options.dns_server)

try:
    fqdn_ip = socket.gethostbyaddr(options.fqdn)[2][0]
except socket.gaierror, e:
    print "There was an error resolving the hostname to its IP: %s. Exiting.\n" % e
    sys.exit(1)

print "DNS record resolves to: %s" % fqdn_ip

# Compute Reverse Record Information
reverse_record = dns.reversename.from_address(fqdn_ip)
reverse_last_octet_ip = re.search(r"([0-9]+).(.*).$", str(reverse_record)).group(1)
reverse_ptr_domain = re.search(r"([0-9]+).(.*).$", str(reverse_record)).group(2)
print "Reverse Record: %s, Last Octet IP: %s, PTR Domain: %s" % (reverse_record, reverse_last_octet_ip, reverse_ptr_domain)

# Process: Read Shared Key
(algorithm, tsigsecret) = keyutils.read_tsigkey(options.key_file,options.key_name)

keyring = dns.tsigkeyring.from_text({
     'ddns-key' : tsigsecret
})

# Process: Delete Forward Record
update = dns.update.Update(domain, keyring = keyring)
update.delete(hostname)
response = dns.query.tcp(update,options.dns_server)
print "Forward Zone Deletion Output: %s\n" % response

# Process: Delete Reverse (PTR) Record
update = dns.update.Update(reverse_ptr_domain, keyring = keyring)
update.delete(reverse_last_octet_ip)
response = dns.query.tcp(update,options.dns_server)
print "Reverse Zone Deletion Output: %s\n" % response
