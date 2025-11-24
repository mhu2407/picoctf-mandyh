FROM golang:latest AS challenge

RUN apt-get update && apt-get install -y python3 socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Build the Go binary -> /app/server
RUN make

RUN mkdir /challenge && chmod 700 /challenge

# Bundle artifacts for players
RUN tar czvf /challenge/artifacts.tar.gz ciphertext.bin starting-board.txt

ARG FLAG
RUN /app/setup-challenge.py

# Let cmgr know this is an nc port named "nc" on 3000
# PUBLISH 3000 AS nc
EXPOSE 3000

# Copy the correct start script
COPY start.sh /opt/start.sh
RUN chmod +x /opt/start.sh

CMD ["/opt/start.sh"]
