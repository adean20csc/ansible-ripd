FROM jcpowermac/alpine-ansible-ssh 

RUN pip install butterfly   

USER ansible
ENTRYPOINT ["/bin/ash"]
CMD ["-c", "/usr/bin/butterfly.server.py --unsecure --host=0.0.0.0"]
