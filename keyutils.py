#!/usr/bin/env python

import dns.tsigkeyring
import re
import sys

def read_tsigkey(tsig_key_file, key_name):
    """Accept a TSIG keyfile and a key name to retrieve.
    Return a keyring object with the key name and TSIG secret."""

    try:
        key_file = open(tsig_key_file)
        key_struct = key_file.read()
        key_file.close()
    except IOError:
        print "A problem was encountered opening your keyfile, %s." % tsig_key_file
        raise

    try:
        key_data = re.search(r"key \"%s\" \{(.*?)\}\;" % key_name, key_struct, re.DOTALL).group(1)
        algorithm = re.search(r"algorithm ([a-zA-Z0-9_-]+?)\;", key_data, re.DOTALL).group(1)
        tsig_secret = re.search(r"secret \"(.*?)\"", key_data, re.DOTALL).group(1)
    except AttributeError:
        print "Unable to decipher the keyname and secret from your key file."
        raise


    keyring = dns.tsigkeyring.from_text({
            key_name : tsig_secret
    })

    return keyring
