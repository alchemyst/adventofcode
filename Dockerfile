FROM python:3.10.1-bullseye

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran 

RUN pip install \
    numpy \
    scipy \
    pandas \
    rich \
    networkx

RUN ["mkdir", "adventofcode"]

WORKDIR /adventofcode

ENTRYPOINT [ "/bin/bash" ]