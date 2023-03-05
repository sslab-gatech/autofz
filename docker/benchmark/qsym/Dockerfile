ARG BENCHMARK_PREFIX
ARG FUZZER_PREFIX
FROM $BENCHMARK_PREFIX/afl as bench_afl
FROM $BENCHMARK_PREFIX/gcc as bench_gcc
FROM $BENCHMARK_PREFIX/fuzzer-test-suite as bench_fts
FROM $FUZZER_PREFIX/qsym

COPY --from=bench_afl /d/p/justafl /d/p/justafl
COPY --from=bench_afl /d/p/aflasan /d/p/aflasan
COPY --from=bench_gcc /d/p/normal /d/p/normal
COPY --from=bench_fts /d/p /d/p
COPY seeds/ /seeds
