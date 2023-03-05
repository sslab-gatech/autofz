ARG BENCHMARK_PREFIX
ARG FUZZER_PREFIX
FROM $BENCHMARK_PREFIX/fuzzer-test-suite-libfuzzer as bench_fts
FROM $FUZZER_PREFIX/libfuzzer

COPY --from=bench_fts /d/p /d/p
COPY seeds/ /seeds
