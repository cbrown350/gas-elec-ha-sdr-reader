FROM alpine:3.18.4 AS builder

RUN apk add --no-cache build-base cmake git libevent-dev gengetopt bsd-compat-headers

WORKDIR /root
RUN git clone https://github.com/slepp/rtlmux && cd rtlmux && make


FROM alpine:3.18.4

WORKDIR /root/rtlmux
COPY --from=builder /root/rtlmux /root/rtlmux
RUN install rtlmux /usr/local/bin && rm -rf /root/rtlmux

RUN apk add --no-cache python3 rtl-sdr libevent curl go git && \
    export GO111MODULE=on && \
    go mod init rtlamr && \
    go get github.com/bemasher/rtlamr@latest && \
    go install github.com/bemasher/rtlamr && \
    mv ~/go/bin/rtlamr /usr/local/bin/rtlamr && \
    rm -rf ~/go && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
  apk del go curl

RUN python3 -m pip install --upgrade pip setuptools pbr

WORKDIR /app

COPY . ./

RUN PBR_VERSION=1.2.3 python3 -m pip install .

RUN chmod +x startup.sh healthcheck.sh

CMD [ "/app/startup.sh" ]