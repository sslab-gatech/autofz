ARG FUZZER_PREFIX
FROM $FUZZER_PREFIX/lafintel

RUN mkdir /d

COPY source/ /autofz_bench

COPY fuzzer-test-suite-lafintel/build_all.sh /

RUN cd /autofz_bench/fuzzer-test-suite-aflplusplus

RUN /build_all.sh
