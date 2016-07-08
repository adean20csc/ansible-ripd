#### Docker Image for Packer

The current base image is Alpine.  It was a perfect choice as a base because of its size at only 4.8 MB.
```
FROM alpine:latest
MAINTAINER Joseph Callen <jcpowermac@gmail.com>
```
In order to use [Hashicorp Packer](http://packer.io) some prerequisites are required which is installed in the image.

```
RUN apk update && \
    apk add qemu-system-x86_64 qemu-img wget unzip py-requests py-pip && \
    pip install cot
```
When the image is built the most current is downloaded.  The GitHub REST API is used via Python Requests to retrieve the latest tagged release.  The version is used to download the packer binary for Linux x86-64.

```
RUN mkdir -p ${packer_bin_dir} \
  && cd ${packer_bin_dir} \
  && wget -nv $(python -c 'import requests;version = requests.get("https://api.github.com/repos/mitchellh/packer/tags").json()[0]["name"].replace("v","");print "https://releases.hashicorp.com/packer/%s/packer_%s_linux_amd64.zip" % (version,version)') -O /tmp/packer.zip \
  && unzip /tmp/packer.zip -d ${packer_bin_dir}
```
The files required for the packer build process is copied into the image.
```
COPY . /opt/hashicorp/etc/packer/
```
Since our image's purpose is to run packer the ENTRYPOINT is configured to the executable path.  By default when the container is ran without any command help will be displayed.
```
ENTRYPOINT ["/opt/hashicorp/bin/packer"]
CMD ["--help"]
```

Port 5900 is exposed in case the VNC console needs to be viewed during the boot and installation process of RancherOS.
```
EXPOSE 5900
```
For the most current revision see the [Dockerfile](../rancheros/Dockerfile).

#### Docker Compose build

If an image needs to built locally for testing or modification the `docker-compose.build.yml` can be used.
The `docker-compose` command below will build the image that `docker-compose.yml` will use to run the container.
```bash
> $ docker-compose -f docker-compose.build.yml build                                                                                                                                                                              ```
Results from executing `docker-compose`
```bash
Building packer-rancheros
Step 1 : FROM alpine:latest
 ---> 4e38e38c8ce0
Step 2 : MAINTAINER Joseph Callen <jcpowermac@gmail.com>
 ---> Using cache
 ---> 164191b261c6
Step 3 : ENV packer_bin_dir /opt/hashicorp/bin
 ---> Using cache
 ---> c1069d070ab6
Step 4 : ENV packer_path ${packer_bin_dir}/packer
 ---> Using cache
 ---> 6e03d4694274
Step 5 : RUN apk update &&     apk add qemu-system-x86_64 qemu-img wget unzip py-requests py-pip &&     pip install cot
 ---> Using cache
 ---> 378754cbb54e
Step 6 : RUN mkdir -p ${packer_bin_dir}   && cd ${packer_bin_dir}   && wget -nv $(python -c 'import requests;version = requests.get("https://api.github.com/repos/mitchellh/packer/tags").json()[0]["name"].replace("v","");print "https://releases.hashicorp.com/packer/%s/packer_%s_linux_amd64.zip" % (version,version)') -O /tmp/packer.zip   && unzip /tmp/packer.zip -d ${packer_bin_dir}
 ---> Using cache
 ---> 3f4d2ddd2f02
Step 7 : COPY . /opt/hashicorp/etc/packer/
 ---> df3585030a84
Removing intermediate container 56e7624e1651
Step 8 : VOLUME /build
 ---> Running in 4918b687f90e
 ---> a7d8369c6f25
Removing intermediate container 4918b687f90e
Step 9 : WORKDIR /build
 ---> Running in 60d2d7f5ec3f
 ---> 01e402bee9fb
Removing intermediate container 60d2d7f5ec3f
Step 10 : ENTRYPOINT /opt/hashicorp/bin/packer
 ---> Running in 1e3996029363
 ---> f39d5a9bdb48
Removing intermediate container 1e3996029363
Step 11 : CMD --help
 ---> Running in c31017cd3df0
 ---> 3103a3f13fc9
Removing intermediate container c31017cd3df0
Step 12 : EXPOSE 5900
 ---> Running in 3ac2ae9806b1
 ---> a51258ee2cf0
Removing intermediate container 3ac2ae9806b1
Successfully built a51258ee2cf0
```

For the most current revision see the [docker-compose.build.yml](../rancheros/docker-compose.build.yml).

[Next](03_packer_config.md)
