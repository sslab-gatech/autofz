ARG PREFIX
FROM $PREFIX/base

WORKDIR /fuzzer

RUN git clone https://github.com/google/AFL.git afl && \
    cd /fuzzer/afl && \
    git checkout 82b5e359463238d790cadbe2dd494d6a4928bff3 && \
    make && make install

WORKDIR /
# https://github.com/google/fuzzbench/blob/master/fuzzers/afl/builder.Dockerfile
RUN apt-get update && \
  apt-get install wget -y && \
  wget https://raw.githubusercontent.com/llvm/llvm-project/5feb80e748924606531ba28c97fe65145c65372e/compiler-rt/lib/fuzzer/afl/afl_driver.cpp -O /fuzzer/afl/afl_driver.cpp && \
  clang -Wno-pointer-sign -c /fuzzer/afl/llvm_mode/afl-llvm-rt.o.c -I/fuzzer/afl && \
  clang++ -stdlib=libc++ -std=c++11 -O2 -c /fuzzer/afl/afl_driver.cpp && \
  ar r /fuzzer/afl/libAFL.a *.o

ENV CC=afl-gcc \
    CXX=afl-g++
