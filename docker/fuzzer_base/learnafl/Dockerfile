ARG PREFIX
FROM $PREFIX/base

WORKDIR /fuzzer

COPY fuzzer_source/LearnAFL/ /fuzzer/LearnAFL
RUN cd LearnAFL && \
    make && make install

ENV CC=afl-gcc \
    CXX=afl-g++
