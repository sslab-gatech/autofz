ARG PREFIX
FROM $PREFIX/base

WORKDIR /fuzzer

RUN git clone https://github.com/carolemieux/afl-rb.git && \
  cd afl-rb && \
  git checkout e529c1f1b366 && \
  make -j && make install

ENV CC=afl-gcc \
    CXX=afl-g++
