FROM alpine:3.14

USER root

RUN apk add bash

RUN addgroup -g 1002 ctf
RUN adduser -h /home/ctfuser -s /bin/bash -D ctfuser

RUN mkdir /home/ctfuser/challenge
RUN chown ctfuser:ctf /home/ctfuser/challenge

COPY Auth /home/ctfuser/challenge/
RUN chmod +x /home/ctfuser/challenge/Auth
RUN chown ctfuser:ctf /home/ctfuser/challenge/Auth

RUN echo "blackhatbureau{P4ssw0rd_1s_Cyph3r}" > /home/ctfuser/challenge/flag
RUN chown ctfuser:ctf /home/ctfuser/challenge/flag

EXPOSE 666/tcp

RUN bash && rm sbin/apk  bin/busybox 

WORKDIR /home/ctfuser/challenge

ENV PATH = ''

USER ctfuser

CMD ["/bin/bash", "-c", "/home/ctfuser/challenge/Auth && /bin/bash "]
