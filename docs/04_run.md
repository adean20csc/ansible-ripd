#### Running the image with docker-compose

To make the execution of the container easier a `docker-compose.yml` has been supplied.  There are a number of options required since we are running a QEMU/KVM virtual machine in this container.  This includes privileged and the mounted devices.  Our image ENTRYPOINT is packer so the command is the arguments required for packer to run.

```yaml
---
version: '2'
services:
    packer-rancheros:
        image: jcpowermac/packer-rancheros
        privileged: true
        ports:
            - "0.0.0.0:5900:5900"
        command: build -only rancher-scsi-e1000 -var 'device=/dev/sda' /opt/hashicorp/etc/packer/rancheros.json
        #environment:
        #    PACKER_LOG: 1
        volumes:
            - build:/build
            - /dev/kvm:/dev/kvm:rw
            - /dev/net/tun:/dev/net/tun:rw

volumes:
  build:

```
For the most current revision see the [docker-compose.yml](../rancheros/docker-compose.yml).



To build the image simple run the command below.
```bash
> $ docker-compose up
```

The output is extensive so only the partial results from the command is listed.
```bash
Creating network "rancheros_default" with the default driver
Creating volume "rancheros_build" with default driver
Creating rancheros_packer-rancheros_1
Attaching to rancheros_packer-rancheros_1
packer-rancheros_1  | rancher-scsi-e1000 output will be in this color.
packer-rancheros_1  |
packer-rancheros_1  | ==> rancher-scsi-e1000: Downloading or copying ISO
packer-rancheros_1  |     rancher-scsi-e1000: Downloading or copying: https://github.com/rancher/os/releases/download/v0.5.0/rancheros.iso
packer-rancheros_1  |     rancher-scsi-e1000: Download progress: 18%
packer-rancheros_1  |     rancher-scsi-e1000: Download progress: 40%
packer-rancheros_1  |     rancher-scsi-e1000: Download progress: 48%
packer-rancheros_1  |     rancher-scsi-e1000: Download progress: 70%
packer-rancheros_1  |     rancher-scsi-e1000: Download progress: 90%
packer-rancheros_1  | ==> rancher-scsi-e1000: Creating hard drive...
packer-rancheros_1  | ==> rancher-scsi-e1000: Found port for communicator (SSH, WinRM, etc): 2222.
packer-rancheros_1  | ==> rancher-scsi-e1000: Looking for available port between 5900 and 5900
packer-rancheros_1  | ==> rancher-scsi-e1000: Found available VNC port: 5900
packer-rancheros_1  | ==> rancher-scsi-e1000: Starting VM, booting from CD-ROM
packer-rancheros_1  |     rancher-scsi-e1000: WARNING: The VM will be started in headless mode, as configured.
packer-rancheros_1  |     rancher-scsi-e1000: In headless mode, errors during the boot sequence or OS setup
packer-rancheros_1  |     rancher-scsi-e1000: won't be easily visible. Use at your own discretion.
packer-rancheros_1  | ==> rancher-scsi-e1000: Overriding defaults Qemu arguments with QemuArgs...
packer-rancheros_1  | ==> rancher-scsi-e1000: Waiting 10s for boot...
packer-rancheros_1  | ==> rancher-scsi-e1000: Connecting to VM via VNC
packer-rancheros_1  | ==> rancher-scsi-e1000: Typing the boot command over VNC...
packer-rancheros_1  | ==> rancher-scsi-e1000: Waiting for SSH to become available...
packer-rancheros_1  | ==> rancher-scsi-e1000: Connected to SSH!
packer-rancheros_1  | ==> rancher-scsi-e1000: Uploading /opt/hashicorp/etc/packer/cloud-config.yml => /tmp/cloud-config.yml
packer-rancheros_1  | ==> rancher-scsi-e1000: Provisioning with shell script: /tmp/packer-shell588498308
packer-rancheros_1  |     rancher-scsi-e1000: Installing from rancher/os:v0.5.0
packer-rancheros_1  |     rancher-scsi-e1000: Unable to find image 'rancher/os:v0.5.0' locally
packer-rancheros_1  |     rancher-scsi-e1000: v0.5.0: Pulling from rancher/os
...
packer-rancheros_1  |     rancher-scsi-e1000 (shell-local):     INFO: Added new harddisk under None, instance is 5
packer-rancheros_1  |     rancher-scsi-e1000 (shell-local):     INFO: Calling 'qemu-img info /tmp/cot7tqdMb/rancher.vmdk' and capturing its output...
packer-rancheros_1  |     rancher-scsi-e1000 (shell-local):     INFO: ...done
packer-rancheros_1  |     rancher-scsi-e1000 (shell-local):     INFO: Writing out to file /build/output/rancher.ovf
packer-rancheros_1  |     rancher-scsi-e1000 (shell-local):     INFO: Copying /tmp/cot7tqdMb/rancher.vmdk to /build/output
packer-rancheros_1  | Build 'rancher-scsi-e1000' finished.
packer-rancheros_1  |
packer-rancheros_1  | ==> Builds finished. The artifacts of successful builds are:
packer-rancheros_1  | --> rancher-scsi-e1000: VM files in directory: /build/output
packer-rancheros_1  | --> rancher-scsi-e1000:
packer-rancheros_1  | --> rancher-scsi-e1000:
packer-rancheros_1  | --> rancher-scsi-e1000:
packer-rancheros_1  | --> rancher-scsi-e1000:
rancheros_packer-rancheros_1 exited with code 0
```

In the current configuration named volumes are used.  The outputted files are available: `/var/lib/docker/volumes/rancheros_build/_data/output`
```
> $ ls -alh
total 101M
drwxr-xr-x. 2 root root 4.0K Jul  7 21:19 .
drwxr-xr-x. 4 root root 4.0K Jul  7 21:18 ..
-rwxr-xr-x. 1 root root  58M Jul  7 21:19 packer-rancher-scsi-e1000
-rw-r--r--. 1 root root  121 Jul  7 21:20 rancher.mf
-rw-r--r--. 1 root root 3.0K Jul  7 21:20 rancher.ovf
-rw-r--r--. 1 root root  44M Jul  7 21:20 rancher.vmdk
```
#### YouTube Video
[![youtube - docker-compose up](http://img.youtube.com/vi/StYlU6Xy_JQ/0.jpg)](http://www.youtube.com/watch?v=StYlU6Xy_JQ)

