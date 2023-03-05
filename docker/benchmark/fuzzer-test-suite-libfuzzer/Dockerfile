ARG FUZZER_PREFIX
FROM $FUZZER_PREFIX/libfuzzer

RUN mkdir /d

COPY source/ /autofz_bench

COPY fuzzer-test-suite-libfuzzer/build_all.sh /

RUN cd /autofz_bench/fuzzer-test-suite

RUN /build_all.sh
