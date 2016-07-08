#!/usr/bin/python

import sys
from subprocess import call
import requests
import re


def parse_checksum(url):
    result = requests.get(url).content
    match = re.match('^sha256:[ ]*([a-z0-9]*)', result)
    return match.group(1)


def current_version(project):

    url = "https://api.github.com/repos/%s/releases" % project
    results = requests.get(url).json()
    for r in results:
        if 'rc' not in r["name"] or 'rc' not in r["tag_name"]:
            return r["url"]


def find_assets(url):

    results = requests.get(url).json()
    for assets in results["assets"]:
        if "iso-checksum" in assets["name"]:
            checksum_url = assets["browser_download_url"]
        elif "rancheros.iso" in assets["name"]:
            iso_url = assets["browser_download_url"]

    return iso_url, checksum_url


def main():
    url = current_version("rancher/os")
    iso_url, checksum_url = find_assets(url)
    checksum = parse_checksum(checksum_url)

    packer_args = sys.argv[1:]
    if 'build' in packer_args:
        packer_args_length = len(packer_args)
        packer_args[packer_args_length - 1:packer_args_length - 1] = ["-var", "iso_checksum=%s" % checksum]
        packer_args[packer_args_length - 1:packer_args_length - 1] = ["-var", "iso_url=%s" % iso_url]

    print packer_args

    packer_args.insert(0, '/opt/hashicorp/bin/packer')
    call(packer_args)

if __name__ == '__main__':
    main()
