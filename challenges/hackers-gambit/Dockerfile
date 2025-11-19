FROM golang:latest AS challenge

RUN apt-get update && apt-get install -y python3 socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

COPY start.sh /opt/
RUN chmod +x /opt/start.sh

RUN make

RUN mkdir /challenge && chmod 700 /challenge

COPY start.sh /opt/
RUN chmod +x /opt/start.sh


RUN tar czvf /challenge/artifacts.tar.gz ciphertext.bin

ARG FLAG

RUN /app/setup-challenge.py

EXPOSE 3000

CMD ["/opt/start.sh"]
