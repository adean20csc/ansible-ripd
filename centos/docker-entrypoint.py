#!/usr/bin/python


from jinja2 import Environment, FileSystemLoader
from subprocess import call
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('--packer', dest='packer', help='Options required for packer', required=True)
#args = parser.parse_args()

env = Environment(loader=FileSystemLoader('/opt/ansible-template/templates'))
template = env.get_template('ks-packer.cfg.j2')

output = template.render()

with open('/build/kickstart/ks.cfg', 'w') as f:
	f.write(output)

#packer_args = args.packer.split()
#packer_args.insert(0, '/opt/packer/packer')
call("/opt/packer/packer build /opt/ansible-template/centos7.json")

