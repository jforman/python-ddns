#!/usr/bin/env python

# Example: delete_dnsrecord.py --record test53.test.mydomain.net --keyfile ddns.key --keyname ddns-key --server mydnsserver

import dns.query
import dns.resolver
import dns.tsigkeyring
import dns.update
import dns.reversename
import re
import socket
import sys

import keyutils

from optparse import OptionParser

re_IPADDRESS = re.compile(r"\d+.\d+.\d+.\d+")

def parse_arguments():
    parser = OptionParser("Delete DNS Records")
    parser.add_option("--record", dest="record",
                      help="FQDN or IP address of the host you wish to delete.",
                      type="string")
    parser.add_option("--keyfile", dest="key_file",
                      help="File containing the TSIG key.",
                      type="string")
    parser.add_option("--keyname", dest="key_name",
                      help="TSIG key name to use for the DDNS update.",
                      type="string")
    parser.add_option("--server", dest="server",
                      help="DNS server containing the record to delete.",
                      type="string")

    (options, args) = parser.parse_args()

    return options

def determine_if_ip_address(record):
    """Determine if the record passed is an IP address."""
    # For now this will just handle IPv4
    return re_IPADDRESS.search(record)

def delete_record(record, server, key_file, key_name):
    if determine_if_ip_address(record):
        reverse_record = str(dns.reversename.from_address(record))
        re_record = re.search(r"([0-9]+)\.(.*).$", reverse_record)
    else:
        re_record = re.search(r"(\w+)\.(.*)$", record)

    record = re_record.group(1)
    domain = re_record.group(2)

    try:
        key_ring = keyutils.read_tsigkey(key_file, key_name)
    except:
        raise

    update = dns.update.Update(domain, keyring = key_ring)
    update.delete(record)
    response = dns.query.tcp(update, server)
    print "Record Deletion Output: %s\n" % response

def main():
    options = parse_arguments()
    print "options: %s" % options
    delete_record(options.record, options.server, options.key_file, options.key_name)

if __name__ == "__main__":
    main()
