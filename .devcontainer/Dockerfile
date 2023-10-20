FROM ubuntu:22.04

# Install build dependencies and other tools for development/debugging
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt install software-properties-common curl -y
RUN ln -snf /usr/share/zoneinfo/$(curl https://ipapi.co/timezone) /etc/localtime || true
RUN echo $(curl https://ipapi.co/timezone) > /etc/timezone || true
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    build-essential \
    cmake \
    make \
    libevent-dev \
    gengetopt \
    gcc \
    net-tools \
    git \
    openssh-client \
    nano \
    pkg-config \
    libusb-1.0-0-dev \
    python3.11-dev \
    golang \
    wget \
    gnuradio \
    rtl-433 \
    rtl-sdr \
    mosquitto-clients \
    docker.io \
    docker-buildx

RUN git clone https://github.com/slepp/rtlmux && cd rtlmux && make && install rtlmux /usr/local/bin

# RUN go install github.com/bemasher/rtlamr@latest && mv ~/go/bin/rtlamr /usr/local/bin/rtlamr
WORKDIR /root
RUN export GO111MODULE=on
RUN go mod init rtlamr
RUN go get github.com/bemasher/rtlamr@latest && go install github.com/bemasher/rtlamr && mv ~/go/bin/rtlamr /usr/local/bin/rtlamr && rm -rf ~/go

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.11 /usr/bin/python3

RUN python3 -m pip install --upgrade pip setuptools wheel pigar pbr

# https://github.com/nektos/act -> run github actions locally
RUN curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | bash && install ./bin/act /usr/local/bin/act && rm -rf ./bin
# use: act --secret-file .secrets
# issues:
# https://github.com/nektos/act/issues/1166 -> (manually pull image and add --pull=false to ~./actrc)

ENV EDITOR=nano  

WORKDIR /app

COPY requirements.txt ./

# generate requirements.txt with 'pigar generate'
RUN python3 -m pip install -r requirements.txt
