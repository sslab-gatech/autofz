ARG PREFIX
FROM $PREFIX/base

WORKDIR /fuzzer

RUN git clone https://github.com/AngoraFuzzer/Angora /fuzzer/angora \
    && cd /fuzzer/angora \
    && git checkout 3cedcac8e65595cd2cdd950b60f654c93cf8cc2e


ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PIN_ROOT=/pin-3.7-97619-g0d0c92f4f-gcc-linux \
    GOPATH=/go \
    PATH=/fuzzer/angora/clang+llvm/bin:/usr/local/cargo/bin:/fuzzer/angora/bin/:/go/bin:$PATH \
    LD_LIBRARY_PATH=/fuzzer/angora/clang+llvm/lib:$LD_LIBRARY_PATH

WORKDIR /fuzzer/angora

RUN ./build/install_rust.sh
RUN PREFIX=/fuzzer/angora ./build/install_llvm.sh

# FIXME: go get cannot specify version in ubuntu 16.04 ...
RUN sed -i 's/go get/#go get/g' /fuzzer/angora/build/install_tools.sh
RUN ./build/install_tools.sh

# no15k
# https://github.com/unifuzz/dockerized_fuzzing/blob/master/angora/Dockerfile.no15k
RUN sed -i 's/15000/1048576/g' /fuzzer/angora/common/src/config.rs
RUN ./build/build.sh
RUN ./build/install_pin_mode.sh

ENV CC=/fuzzer/angora/bin/angora-clang CXX=/fuzzer/angora/bin/angora-clang++
