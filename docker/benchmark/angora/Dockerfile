ARG FUZZER_PREFIX
ARG BENCHMARK_PREFIX
FROM $BENCHMARK_PREFIX/gcc as bench_gcc
FROM $BENCHMARK_PREFIX/fuzzer-test-suite-angora as bench_fts_angora
FROM $FUZZER_PREFIX/angora

RUN mkdir -p /d/p/angora

COPY --from=bench_gcc /d/p/normal /d/p/normal
COPY source/ /autofz_bench

COPY angora/abilist.txt /tmp/abilist_ffmpeg.txt

COPY angora/build_all.sh /

RUN /build_all.sh > /dev/null

COPY --from=bench_fts_angora /d/p/ /d/p/

COPY seeds/ /seeds

RUN find /autofz_bench -type d -name ".git" | xargs rm -rf
