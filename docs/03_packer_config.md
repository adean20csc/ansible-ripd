#### RancherOS Packer JSON Configuration

##### Provisioners
The first section is the provisioners.  These actions are executed after SSH is available.
First highlighted section is the regarding the `cloud-config.yml`.  This file is used in a RancherOS install to configure the instance.
```json
{
  "type": "file",
  "source": "/opt/hashicorp/etc/packer/cloud-config.yml",
  "destination": "/tmp/cloud-config.yml"
}
```

The `cloud-config.yml` is configured to start the `jcpowermac/alpine-ansible-ssh` container always when the virtual machine instance is running.  Details regarding this image are available in the [README.md](../alpine-ansible-ssh/README.md).
```yml
#cloud-config
ssh_authorized_keys:
  - ssh-rsa
rancher:
    services:
        alpine-ansible-ssh:
            image: jcpowermac/alpine-ansible-ssh
            ports:
                - 2222:22
            restart: always
```

After the `cloud-config.yml` is available the `ros install` command is executed with the appropriate options.  One variable is included `device` based on the variability between using virtio and traditional scsi disk e.g. `/dev/vda` vs `/dev/sda`.
```json
{
  "type": "shell",
  "inline": ["sudo ros install -c /tmp/cloud-config.yml -d {{user `device`}} -f -t generic --no-reboot"]
}
```

##### Builders

The `rancher-scsi-e1000` builder can be used for both KVM and VMware hypervisors.  In the current configuration the rancher iso is downloaded from GitHub and executed in KVM.  Please note `qemuargs` is set to `-m 1024M`.  In order for RancherOS to install it needs enough memory to download the RancherOS container.  

```json
{
  "name": "rancher-scsi-e1000",
  "type": "qemu",
  "iso_checksum_type": "sha256",
  "iso_checksum": "58ca14b497178097d716ecd5d06332c4c2f6b9c5a127cf88453a5d22742835d4",
  "iso_url": "https://github.com/rancher/os/releases/download/v0.5.0/rancheros.iso",
  "output_directory": "/build/output",
  "ssh_wait_timeout": "30s",
  "shutdown_command": "sudo poweroff",
  "disk_size": 8192,
  "format": "qcow2",
  "headless": true,
  "accelerator": "kvm",
  "ssh_host_port_min": 2222,
  "ssh_host_port_max": 2229,
  "ssh_username": "rancher",
  "ssh_password": "rancher",
  "ssh_port": 22,
  "ssh_wait_timeout": "90m",
  "net_device": "e1000",
  "disk_interface": "scsi",
  "vnc_port_min": 5900,
  "vnc_port_max": 5900,
  "qemuargs": [
      [ "-m", "1024M" ]
    ]
}
```

##### Post Processors

After the builder has finished there are a few more steps before our VMware-based appliance is ready.  Packer outputs the image as qcow2.  For VMware a VMDK based disk file is needed.  Using `qemu-img` the existing qcow2 image is converted to vmdk and stored as `rancher.vmdk`.
```json
{
    "type": "shell-local",
    "inline": "qemu-img convert -f qcow2 -O vmdk /build/output/packer-rancher-scsi-e1000 /build/output/rancher.vmdk",
    "only": ["rancher-scsi-e1000"]
}
```
To build an OVF the follow commands are executed.  This provides the necessary configuration including CPU, memory, network devices and disks.
```json
{
    "type": "shell-local",
    "inline": "cot -f edit-product /opt/hashicorp/etc/packer/minimal.ovf -o /build/output/rancher.ovf -p RancherOS -n Rancher -v 0.5.0",
    "only": ["rancher-scsi-e1000"]
},
{
    "type": "shell-local",
    "inline": "cot -f edit-hardware /build/output/rancher.ovf -v vmx-8 -c 1 -m 1G -n 1 --nic-types e1000 --nic-names eth0 --nic-networks eth0 --network-descriptions \"Management Network\"",
    "only": ["rancher-scsi-e1000"]
},
{
    "type": "shell-local",
    "inline": "cot -f add-disk /build/output/rancher.vmdk /build/output/rancher.ovf -t harddisk -c scsi",
    "only": ["rancher-scsi-e1000"]
}
```

For the most current revision see the [rancheros.json](../rancheros/rancheros.json).



[Next](04_run.md)
