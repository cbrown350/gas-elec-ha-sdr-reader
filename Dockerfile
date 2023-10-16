FROM ubuntu:22.04

# Install dependencies
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
    git \
    openssh-client \
    nano \
    pkg-config \
    libusb-1.0-0-dev \
    python3.12-dev \
    golang \
    wget \
    gnuradio \
    rtl-433 \
    rtl-sdr \
    mosquitto-clients \
  && rm -rf /var/lib/apt/lists/*

ENV EDITOR=nano  

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.12 /usr/bin/python3

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install paho-mqtt pytz

RUN git clone https://github.com/slepp/rtlmux && cd rtlmux && make && install rtlmux /usr/local/bin

# RUN go install github.com/bemasher/rtlamr@latest && cp ~/go/bin/rtlamr /usr/local/bin/rtlamr
WORKDIR /root
RUN export GO111MODULE=on
RUN go mod init rtlamr
RUN go get github.com/bemasher/rtlamr@latest && go install github.com/bemasher/rtlamr && cp ~/go/bin/rtlamr /usr/local/bin/rtlamr

WORKDIR /app

COPY . ./

RUN chmod +x startup.sh

CMD ["/app/startup.sh"]