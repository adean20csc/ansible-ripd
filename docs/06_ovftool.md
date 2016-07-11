#### Deploy with ovftool

In the example below the ovftool used is the one included with VMware Fusion.  This path would need to be replaced based on your installation location.  The arguments that should be modified for your environment.

- `-ds`
- `--net` after the `=` 
- destination  
  In the example this is being deployed to ESXi 5.5 


```bash
$ /Applications/VMware\ Fusion.app/Contents/Library/VMware\ OVF\ Tool/ovftool -ds=datastore1 --skipManifestCheck "--net:eth0=VM Network" ~/Downloads/rancher-ovf/rancher.ovf "vi://root:trustn01@10.53.252.71"
Opening OVF source: /Users/jcallen/Downloads/rancher-ovf/rancher.ovf
Opening VI target: vi://root@10.53.252.71:443/
Deploying to VI: vi://root@10.53.252.71:443/
Transfer Completed
Completed successfully
```

Connect to the Docker container and run a few Ansible commands.
```bash
$ ssh -p2222 ansible@10.53.252.97

Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <http://wiki.alpinelinux.org>.

You can setup the system with the command: setup-alpine

You may change this message by editing /etc/motd.

9989840a0322:~$ ansible localhost -m setup -c local -i localhost,
localhost | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [],
        "ansible_all_ipv6_addresses": [],
        "ansible_architecture": "x86_64",
        "ansible_bios_date": "04/14/2014",
        "ansible_bios_version": "6.00",
        "ansible_cmdline": {
            "BOOT_IMAGE": "/boot/vmlinuz-v0.5.0-rancheros",
            "console": "tty0"
        },
        "ansible_date_time": {
...

9989840a0322:~$ ansible-playbook --version
ansible-playbook 2.1.0.0
  config file =
  configured module search path = Default w/o overrides
```

##### YouTube video

[![youtube - deploy via ovftool](http://img.youtube.com/vi/ALbAoD_63fY/0.jpg)](http://www.youtube.com/watch?v=ALbAoD_63fY)
