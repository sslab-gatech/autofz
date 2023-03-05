ARG PREFIX
FROM $PREFIX/base

RUN mkdir -p /fuzzer

ENV LLVM_CONFIG=llvm-config-12
ENV AFL_SKIP_CPUFREQ=1
ENV AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1

WORKDIR /fuzzer
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git -b 3.13c afl++

WORKDIR /fuzzer/afl++

RUN make clean && \
  make -j source-only && make install

RUN cd custom_mutators/radamsa && \
  make -j


ENV CC=afl-clang-fast \
  CXX=afl-clang-fast++
