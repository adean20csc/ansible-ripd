
#### alpine-ansible-ssh

A Docker image with Ansible is already available in the Docker Hub so that is our starting point for this image.
```
FROM williamyeh/ansible:alpine3
```
The Ansible playbook `init.yml` and the OpenSSH server configuration file is copied to `/tmp`.
```
COPY . /tmp/
```
Since Ansible is already available it will be used to configure the rest of the image.  Which includes:
- Installing and configuring OpenSSH
- Creating the Ansible user account
- Generating the host's SSH Keys
- Installing additional python requirements for AWS and Windows

```
RUN ansible-playbook /tmp/init.yml -c local -i localhost,
```
The ash shell is the ENTRYPOINT with the CMD defaulted to run sshd.
```
ENTRYPOINT ["/bin/ash"]
CMD ["-c", "/usr/sbin/sshd -D -e"]
```
