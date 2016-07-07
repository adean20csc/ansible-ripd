FROM alpine:latest
MAINTAINER Joseph Callen <jcpowermac@gmail.com>

ENV packer_bin_dir /opt/hashicorp/bin
ENV packer_path ${packer_bin_dir}/packer

RUN apk update && \
    apk add qemu-system-x86_64 qemu-img wget unzip py-requests py-pip && \
    pip install cot

RUN mkdir -p ${packer_bin_dir} \
  && cd ${packer_bin_dir} \
  && wget -nv $(python -c 'import requests;version = requests.get("https://api.github.com/repos/mitchellh/packer/tags").json()[0]["name"].replace("v","");print "https://releases.hashicorp.com/packer/%s/packer_%s_linux_amd64.zip" % (version,version)') -O /tmp/packer.zip \
  && unzip /tmp/packer.zip -d ${packer_bin_dir} 

COPY . /opt/hashicorp/etc/packer/

VOLUME /build
WORKDIR /build
ENTRYPOINT ["/opt/hashicorp/bin/packer"]
CMD ["--help"]
EXPOSE 5900

