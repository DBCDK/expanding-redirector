FROM docker.dbc.dk/dbc-stretch:latest
MAINTAINER DBC <dbc@dbc.dk>

ENV PORT=8888
LABEL PORT="Port to listen for http requests on (default: 8888)"


RUN useradd -u 8888 -d /var/lib/redirector -m -s /bin/bash redirector
RUN apt-install python3-tornado

ADD docker-entrypoint.sh /
ADD expanding-redirector.py index.html /var/lib/redirector/

USER redirector
WORKDIR /var/lib/redirector
EXPOSE 8888
CMD [ "/bin/bash", "/docker-entrypoint.sh" ]
