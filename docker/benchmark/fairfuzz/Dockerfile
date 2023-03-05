ARG BENCHMARK_PREFIX
ARG FUZZER_PREFIX
FROM $BENCHMARK_PREFIX/afl as bench_afl
FROM $FUZZER_PREFIX/fairfuzz
COPY --from=bench_afl /d/p/justafl /d/p/justafl
COPY seeds/ /seeds
