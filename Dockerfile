FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt install --no-install-recommends -y \
    build-essential \
    cmake \
    make \
    libevent-dev \
    gengetopt \
    gcc \
    git \
    pkg-config \
    libusb-1.0-0-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    golang \
    wget \
    gnuradio \
    rtl-433 \
    rtl-sdr \
    mosquitto-clients \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install paho-mqtt pytz

RUN git clone https://github.com/slepp/rtlmux && cd rtlmux && make && install rtlmux /usr/local/bin

RUN go install github.com/bemasher/rtlamr@latest && cp ~/go/bin/rtlamr /usr/local/bin/rtlamr

WORKDIR /app

COPY . ./

RUN chmod +x startup.sh

CMD ["/app/startup.sh"]