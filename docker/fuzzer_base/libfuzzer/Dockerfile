ARG PREFIX
FROM $PREFIX/base

WORKDIR /fuzzer

RUN mkdir -p /fuzzer/libfuzzer /fuzzer/libfuzzer/build

WORKDIR /fuzzer/libfuzzer/

RUN apt install -y ninja-build

RUN git clone --depth=1 --single-branch --branch fuzzer_sync https://github.com/phi-go/llvm-project.git

# RUN cd llvm-project && mkdir build && cd build &&\
#   cmake -G Ninja -DLLVM_TARGETS_TO_BUILD=Native -DCMAKE_BUILD_TYPE=Release \
#   -DLLVM_ENABLE_PROJECTS='clang;compiler-rt' -DCMAKE_INSTALL_PREFIX=/fuzzer/libfuzzer ../llvm &&\
#   ninja && ninja install

RUN cd /fuzzer/libfuzzer/llvm-project/compiler-rt/lib/fuzzer && ./build.sh
