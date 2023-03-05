ARG FUZZER_PREFIX
ARG BENCHMARK_PREFIX
FROM $BENCHMARK_PREFIX/fuzzer-test-suite as bench_fts
FROM $FUZZER_PREFIX/angora

RUN mkdir -p /d/p/angora

COPY --from=bench_fts /d/p/normal /d/p/normal

COPY source/ /autofz_bench

RUN cd /autofz_bench/fuzzer-test-suite


COPY fuzzer-test-suite-angora/build_all.sh /

RUN /build_all.sh
