#!/usr/bin/env python

try:
    import json
except ImportError:
    import simplejson as json

try:
    from typing import Dict
except:
    pass


import dns.resolver as r
import os
import sys

username_env_var = "LINUXACADEMY_USERNAME"


def get_config(env_var):
    result = os.getenv(env_var)
    if not result:
        sys.exit("failed=True, msg='missing %s environment variable'" % env_var)
    return result


def hostname(user, i, suffix):
    return "%s%s%s" % (username, i, linuxacademy_host_suffix)

username = get_config(username_env_var)
result = {}  # type: Dict[str, Dict]
linuxacademy_host_suffix = ".mylabserver.com"

resolver = r.Resolver(configure="False")
resolver.nameservers = [
    '1.1.1.1',
    '1.0.0.1',
    '8.8.8.8',
    '8.8.4.4']


def facts_for_host(host):
    try:
        result = {}
        resp = resolver.query(host)
        result[host] = {
            "ansible_user": "user",
            "ansible_host": resp[0].to_text()
        }
        return result
    except r.NXDOMAIN:
        pass
    return {}


def facts_for_group():
    group = []
    for i in range(1, 6):
        host = hostname(username, i, linuxacademy_host_suffix)
        facts = facts_for_host(host)
        if facts:
            group.append(facts)
    return group


if len(sys.argv) == 2 and sys.argv[1] == '--list':
    print(json.dumps(facts_for_group()))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    host_facts = facts_for_host(sys.argv[2])
    print(json.dumps(host_facts))
else:
    print("Need an argument, either --list or --host <host>")