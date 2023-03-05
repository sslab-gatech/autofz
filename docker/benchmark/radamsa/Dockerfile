ARG BENCHMARK_PREFIX
ARG FUZZER_PREFIX
FROM $BENCHMARK_PREFIX/afl as bench_afl
FROM $BENCHMARK_PREFIX/aflplusplus as bench_aflplusplus
FROM $FUZZER_PREFIX/radamsa
COPY --from=bench_afl /d/p/ /d/p/
COPY --from=bench_aflplusplus /d/p/ /d/p/
COPY seeds/ /seeds
