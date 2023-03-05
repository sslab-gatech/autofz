ARG FUZZER_PREFIX
ARG BENCHMARK_PREFIX
FROM $BENCHMARK_PREFIX/fuzzer-test-suite as bench_fts
FROM $FUZZER_PREFIX/afl

RUN mkdir /d

COPY source/ /autofz_bench

COPY afl/build_all.sh /

RUN /build_all.sh > /dev/null

COPY --from=bench_fts /d/p/ /d/p/

COPY seeds/ /seeds

RUN find /autofz_bench -type d -name ".git" | xargs rm -rf
