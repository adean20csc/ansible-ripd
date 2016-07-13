FROM williamyeh/ansible:alpine3

COPY . /tmp/
RUN ansible-playbook /tmp/init.yml -c local -i localhost,

ENTRYPOINT ["/bin/ash"]
CMD ["-c", "/usr/sbin/sshd -D -e"]
