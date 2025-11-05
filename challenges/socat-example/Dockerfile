FROM golang:latest AS challenge

RUN apt-get update && apt-get install -y python3 socat

WORKDIR /app
COPY . . 
COPY start.sh /opt/
RUN chmod +x /opt/start.sh
RUN make

RUN mkdir /challenge && chmod 700 /challenge
COPY start.sh /opt/
RUN chmod +x /opt/start.sh
RUN tar czvf /challenge/artifacts.tar.gz yolosign.go

ARG FLAG

RUN /app/setup-challenge.py

# PUBLISH 5555 AS nc
EXPOSE 5555
CMD ["/opt/start.sh"]
