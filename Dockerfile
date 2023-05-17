##
## Copyright 2023 Ocean Protocol Foundation
## SPDX-License-Identifier: Apache-2.0
##
FROM ubuntu:20.04
LABEL maintainer="Ocean Protocol <devops@oceanprotocol.com>"

ARG VERSION

RUN apt-get update && \
   apt-get install --no-install-recommends -y \
   python3.8 \
   python3-pip \
   python3.8-dev \
   gettext-base

COPY . /pdr-predictoor
WORKDIR /pdr-predictoor

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

ENV ADDRESS_FILE="${HOME}/.ocean/ocean-contracts/artifacts/address.json"
ENV RPC_URL="http://127.0.0.1:8545"
ENV SUBGRAPH_URL="http://172.15.0.15:8000/subgraphs/name/oceanprotocol/ocean-subgraph"
ENV PRIVATE_KEY="0xef4b441145c1d0f3b4bc6d61d29f5c6e502359481152f869247c7a4244d45209"

ENTRYPOINT ["python3","main.py"]
