ARG FUZZER_PREFIX
ARG BENCHMARK_PREFIX
FROM $BENCHMARK_PREFIX/fuzzer-test-suite-aflplusplus as bench_fts_aflpp
FROM $FUZZER_PREFIX/aflplusplus

RUN mkdir /d

COPY source/ /autofz_bench

COPY aflplusplus/build_all.sh /

RUN /build_all.sh > /dev/null

COPY seeds/ /seeds

COPY --from=bench_fts_aflpp /d/p/ /d/p/

RUN find /autofz_bench -type d -name ".git" | xargs rm -rf
