ARG FUZZER_PREFIX
ARG BENCHMARK_PREFIX
FROM $BENCHMARK_PREFIX/fuzzer-test-suite-lafintel as bench_fts_lafintel
FROM $FUZZER_PREFIX/lafintel

RUN mkdir /d

COPY source/ /autofz_bench

COPY lafintel/build_all.sh /

RUN /build_all.sh > /dev/null

COPY seeds/ /seeds

COPY --from=bench_fts_lafintel /d/p/ /d/p/
