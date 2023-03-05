ARG FUZZER_PREFIX
ARG BENCHMARK_PREFIX
FROM $BENCHMARK_PREFIX/aflplusplus as bench_aflplusplus
FROM $BENCHMARK_PREFIX/fuzzer-test-suite-aflplusplus as bench_fts_aflplusplus
FROM $FUZZER_PREFIX/redqueen

RUN mkdir /d

COPY --from=bench_aflplusplus /d/p/ /d/p/
COPY --from=bench_fts_aflplusplus /d/p/ /d/p/
COPY seeds/ /seeds
