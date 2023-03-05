ARG FUZZER_PREFIX
FROM $FUZZER_PREFIX/afl

RUN mkdir /d

COPY source/ /autofz_bench

RUN cd /autofz_bench/fuzzer-test-suite

COPY fuzzer-test-suite/build_all.sh /

RUN /build_all.sh
