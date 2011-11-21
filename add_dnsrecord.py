#!/usr/bin/env python

# Example: add_dnsrecord.py --fqdn host101.testzone.example.com --ip 10.30.0.101 --keyfile ddns.key --keyname ddns-key --server mydnsserver --reverse

import dns.query
import dns.reversename
import dns.tsigkeyring
import dns.update
import re
import sys

import keyutils

from optparse import OptionParser

def parse_arguments():
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
    parser.add_option("--reverse", action="store_true", default=False,
                      help="Enable if you want to create a reverse PTR record.")
    parser.add_option("--server", dest="dns_server",
                      help="DNS server to query.",
                      type="string")
    parser.add_option("--ttl",dest="ttl",
                      help="Time to Live (in Seconds). Default: 86400",
                      type="int",default=86400)
    
    (options, args) = parser.parse_args()
    return options

def add_forward_record(hostname, domain, ip_address, ttl, dns_server, key_file, key_name):
    """Add an A record to the specific DNS server
    with the provided hostname/IP/key information."""

    (algorithm, tsigsecret) = keyutils.read_tsigkey(key_file, key_name)

    keyring = dns.tsigkeyring.from_text({
            key_name : tsigsecret
    })

    update = dns.update.Update(domain, keyring = keyring)
    update.replace(hostname, ttl, 'A', ip_address)
    try:
        response = dns.query.tcp(update, dns_server)
        print "Output: %s" % response
    except dns.tsig.PeerBadKey:
        print "The remote DNS server %s did not accept the key passed." % dns_server
        raise
    except Exception, err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print "type: %s, obj: %s, tb: %s" % (exc_type, exc_obj, exc_tb)
        print "Unhandled exception in add_forward_record: %s" % err
        raise

    return


def add_reverse_record(fqdn, domain, ip_address, ttl, dns_server, key_file, key_name):
    print "in add_reverse_record"
    reverse_fqdn = str(dns.reversename.from_address(ip_address))
    print "Reverse fqdn: %s" % reverse_fqdn
    reverse_ip = re.search(r"([0-9]+).(.*).$", reverse_fqdn).group(1)
    reverse_domain = re.search(r"([0-9]+).(.*).$", reverse_fqdn).group(2)

    print "reverse ip: %s, domain: %s" % (reverse_ip, reverse_domain)

    (algorithm, tsigsecret) = keyutils.read_tsigkey(key_file, key_name)

    keyring = dns.tsigkeyring.from_text({
            key_name : tsigsecret
    })

    print "in reverse, hostname: %s" % fqdn
    update = dns.update.Update(reverse_domain, keyring = keyring)
    update.replace(reverse_ip, ttl, 'PTR', fqdn)
    response = dns.query.tcp(update, dns_server)

    print "reverse response: %s" % response

def main():
    options = parse_arguments()
    hostname = re.search(r"(\w+).(.*)", options.fqdn).group(1)
    domain = re.search(r"(\w+).(.*)", options.fqdn).group(2)
    print "Host to be added/updated: %s, IP Address: %s, DNS Server: %s" % (options.fqdn, options.ip_address, options.dns_server)
    try:
        add_forward_record(hostname, domain, options.ip_address, options.ttl, options.dns_server, options.key_file, options.key_name)
    except:
        print "Exception in add_forward_record. Exiting."
        sys.exit(1)

    add_reverse_record(options.fqdn, domain, options.ip_address, options.ttl, options.dns_server, options.key_file, options.key_name)


if __name__ == "__main__":
    main()
