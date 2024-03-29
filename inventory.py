#!/usr/bin/env python3
# https://github.com/ansible/ansible/blob/stable-2.1/contrib/inventory/vagrant.py
# License: GNU General Public License, Version 3 <http://www.gnu.org/licenses/>
"""
Vagrant external inventory script. Automatically finds the IP of the booted vagrant vm(s), and
returns it under the host group 'vagrant'
Example Vagrant configuration using this script:
    config.vm.provision :ansible do |ansible|
      ansible.playbook = "./provision/your_playbook.yml"
      ansible.inventory_file = "./provision/inventory/vagrant.py"
      ansible.verbose = true
    end
"""

# Copyright (C) 2013  Mark Mandel <mark@compoundtheory.com>
#               2015  Igor Khomyakov <homyakov@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# Thanks to the spacewalk.py inventory script for giving me the basic structure
# of this.
#
import sys
import os.path
import subprocess
import re
from paramiko import SSHConfig
from io import StringIO
from optparse import OptionParser
from collections import defaultdict
import json

_group = 'vagrant'  # a default group
_ssh_to_ansible = [('user', 'ansible_ssh_user'),
                   ('hostname', 'ansible_ssh_host'),
                   ('identityfile', 'ansible_ssh_private_key_file'),
                   ('port', 'ansible_ssh_port')]

# Options
# ------------------------------

parser = OptionParser(usage="%prog [options] --list | --host <machine>")
parser.add_option('--list', default=False, dest="list", action="store_true",
                  help="Produce a JSON consumable grouping of Vagrant servers for Ansible")
parser.add_option('--host', default=None, dest="host",
                  help="Generate additional host specific details for given host for Ansible")
(options, args) = parser.parse_args()

#
# helper functions
#


# get all the ssh configs for all boxes in an array of dictionaries.
def get_ssh_config():
    return {k: get_a_ssh_config(k) for k in list_running_boxes()}


# list all the running boxes
def list_running_boxes():
    output = subprocess.check_output(["vagrant", "status"]).decode().split('\n')

    boxes = []

    for line in output:
        matcher = re.search("([^\s]+)[\s]+running \(.+", line)
        if matcher:
            boxes.append(matcher.group(1))

    return boxes


# get the ssh config for a single box
def get_a_ssh_config(box_name):
    """Gives back a map of all the machine's ssh configurations"""

    try:
        output = subprocess.check_output(["vagrant", "ssh-config", box_name])
        config = SSHConfig()
        config.parse(StringIO(output.decode()))
        host_config = config.lookup(box_name)

        # man 5 ssh_config:
        # > It is possible to have multiple identity files ...
        # > all these identities will be tried in sequence.
        for id in host_config['identityfile']:
            if os.path.isfile(id):
                host_config['identityfile'] = id

        return {v: host_config[k] for k, v in _ssh_to_ansible}
    except Exception:
        return {}

def add_to_group(data, host):
    group = 'ungrouped'
    if 'worker' in host:
        group = 'workers'
    elif 'controlplane' in host:
        group = 'controlplane'
    elif 'storage' in host:
        group = 'storage'
    
    if group not in data:
        data[group] = defaultdict(dict)
        data[group]['hosts'] = []

    data[group]['hosts'].append(host)


# List out servers that vagrant has running
# ------------------------------
if options.list:
    ssh_config = get_ssh_config()
    meta = defaultdict(dict)
    data = defaultdict(dict)
    data['_meta'] = meta
    data['all'] = {'children': ['ungrouped', 'controlplane', 'workers', 'storage']}

    for host in ssh_config:
        meta['hostvars'][host] = ssh_config[host]
        add_to_group(data, host)

    print(json.dumps(data))
    sys.exit(0)

# Get out the host details
# ------------------------------
elif options.host:
    print(json.dumps(get_a_ssh_config(options.host)))
    sys.exit(0)

# Print out help
# ------------------------------
else:
    parser.print_help()
    sys.exit(0)