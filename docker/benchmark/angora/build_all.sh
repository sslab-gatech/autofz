#!/bin/bash -e

mkdir -p /d/p/angora/taint /d/p/angora/fast

unibench_targets=(
    exiv2
    gdk-pixbuf-pixdata
    imginfo
    jhead
    tiffsplit
    lame
    mp3gain
    wav2swf
    ffmpeg
    flvmeta
    mp42aac
    cflow
    infotocap
    jq
    mujs
    pdftotext
    sqlite3
    nm
    objdump
    tcpdump
)


for target in "${unibench_targets[@]}";
do
    mkdir -p /d/p/angora/taint/unibench/$target
    mkdir -p /d/p/angora/fast/unibench/$target
done

export ANGORA_TAINT_RULE_LIST=/tmp/abilist.txt

ldd /d/p/normal/*/*/*|grep .so|awk '{print $3}'|grep .so|sort|uniq|sed 's#^/lib#/usr/lib#g'|sed 's#\.so.*$#.so#g'|grep -v libgcc_s.so|grep -v libstdc++.so|grep -v libc.so|grep -v libm.so|grep -v libpthread.so|xargs -i /fuzzer/angora/tools/gen_library_abilist.sh '{}' discard >> $ANGORA_TAINT_RULE_LIST

LIBS=(
    /usr/lib/x86_64-linux-gnu/libpng.so
    /usr/lib/x86_64-linux-gnu/libfreetype.so.6
)

for lib in "${LIBS[@]}";
do
    /fuzzer/angora/tools/gen_library_abilist.sh $lib discard >> $ANGORA_TAINT_RULE_LIST
done


cd /autofz_bench/unibench && \
    mkdir mp3gain-1.5.2 && cd mp3gain-1.5.2 && mv ../mp3gain-1.5.2.zip ./ && unzip -q mp3gain-1.5.2.zip && rm mp3gain-1.5.2.zip && cd .. &&\
    ls *.zip|xargs -i unzip -q '{}' &&\
    ls *.tar.gz|xargs -i tar xf '{}' &&\
    rm -r *.tar.gz *.zip &&\
    mv SQLite-8a8ffc86 SQLite-3.8.9 && mv binutils_5279478 binutils-5279478 && mv libtiff-Release-v3-9-7 libtiff-3.9.7 &&\
    ls -alh

{
 cd /autofz_bench/unibench/exiv2-0.26 && cmake -DEXIV2_ENABLE_SHARED=OFF . && \
     make clean && \
     make -j && cp bin/exiv2 /d/p/angora/fast/unibench/exiv2/exiv2 &&\
     make clean && USE_TRACK=1 make -j && cp bin/exiv2 /d/p/angora/taint/unibench/exiv2/exiv2 &&\
     make clean
} &

{
cd /autofz_bench/unibench/gdk-pixbuf-2.31.1 &&\
    ./autogen.sh --enable-static=yes --enable-shared=no --with-included-loaders=yes && \
    make clean && \
    make -j &&\
    cp gdk-pixbuf/gdk-pixbuf-pixdata /d/p/angora/fast/unibench/gdk-pixbuf-pixdata &&\
    make clean && USE_TRACK=1 make -j &&\
    cp gdk-pixbuf/gdk-pixbuf-pixdata /d/p/angora/taint/unibench/gdk-pixbuf-pixdata &&\
    make clean
} &

{
cd /autofz_bench/unibench/jasper-2.0.12 && cmake -DJAS_ENABLE_SHARED=OFF -DALLOW_IN_SOURCE_BUILD=ON . &&\
    make clean && \
    make -j &&\
    cp src/appl/imginfo /d/p/angora/fast/unibench/imginfo &&\
    make clean && USE_TRACK=1 make -j &&\
    cp src/appl/imginfo /d/p/angora/taint/unibench/imginfo &&\
    make clean
} &

{
    cd /autofz_bench/unibench/jhead-3.00 &&\
        make clean && \
        make -j &&\
        cp jhead /d/p/angora/fast/unibench/jhead &&\
        make clean && USE_TRACK=1 make -j &&\
        cp jhead /d/p/angora/taint/unibench/jhead &&\
        make clean
} &

{
    cd /autofz_bench/unibench/libtiff-3.9.7 && ./autogen.sh && ./configure --disable-shared &&\
        make clean && \
        make -j &&\
        cp tools/tiffsplit /d/p/angora/fast/unibench/tiffsplit &&\
        make clean && USE_TRACK=1 make -j &&\
        cp tools/tiffsplit /d/p/angora/taint/unibench/tiffsplit &&\
        make clean
} &

{
    cd /autofz_bench/unibench/lame-3.99.5 && ./configure --disable-shared &&\
        make clean && \
        make -j &&\
        cp frontend/lame /d/p/angora/fast/unibench/lame &&\
        make clean && USE_TRACK=1 make -j &&\
        cp frontend/lame /d/p/angora/taint/unibench/lame &&\
        make clean
} &

{
    cd /autofz_bench/unibench/mp3gain-1.5.2 && sed -i 's/CC=/CC?=/' Makefile &&\
        make clean && \
        make -j &&\
        cp mp3gain /d/p/angora/fast/unibench/mp3gain &&\
        make clean && USE_TRACK=1 make -j &&\
        cp mp3gain /d/p/angora/taint/unibench/mp3gain &&\
        make clean
} &

{
    cd /autofz_bench/unibench/swftools-0.9.2/ && ./configure &&\
        sed -i 's/int inline ActionTagSize/int ActionTagSize/' ./lib/modules/swfaction.c &&\
        sed -i 's/byte inline PaethPredictor/byte PaethPredictor/' ./src/png2swf.c &&\
        make clean && \
        make -j &&\
        cp src/wav2swf /d/p/angora/fast/unibench/wav2swf &&\
        make clean && USE_TRACK=1 make -j &&\
        cp src/wav2swf /d/p/angora/taint/unibench/wav2swf &&\
        make clean
} &

# Comment out ffmpeg for building under travis-ci
# The memory usage seems to exceed 3GB and may make the whole build job timeout (50 minutes)
{
    # NOTE: build fail, use unibench version isntead
    wget --quiet https://gitlab.com/unifuzz/unibench_build/raw/master/ffmpeg/angora.tar.gz &&\
        tar xf angora.tar.gz -C / &&\
        rm angora.tar.gz &&
        mv /d/p/angora/fast/ffmpeg /d/p/angora/fast/unibench/ffmpeg/ &&
        mv /d/p/angora/taint/ffmpeg /d/p/angora/taint/unibench/ffmpeg/
} &

{
    cd /autofz_bench/unibench/flvmeta-1.2.1 && cmake . &&\
        make clean && \
        make -j &&\
        cp src/flvmeta /d/p/angora/fast/unibench/flvmeta &&\
        make clean && USE_TRACK=1 make -j &&\
        cp src/flvmeta /d/p/angora/taint/unibench/flvmeta &&\
        make clean
} &

{
    cd /autofz_bench/unibench/Bento4-1.5.1-628 && cmake . &&\
        make clean && \
        make -j &&\
        cp mp42aac /d/p/angora/fast/unibench/mp42aac &&\
        make clean && USE_TRACK=1 make -j &&\
        cp mp42aac /d/p/angora/taint/unibench/mp42aac &&\
        make clean
} &

{
    cd /autofz_bench/unibench/cflow-1.6 && ./configure &&\
        make clean && \
        make -j &&\
        cp src/cflow /d/p/angora/fast/unibench/cflow &&\
        make clean && USE_TRACK=1 make -j &&\
        cp src/cflow /d/p/angora/taint/unibench/cflow &&\
        make clean
} &

{
    cd /autofz_bench/unibench/ncurses-6.1 && ./configure --disable-shared &&\
        make clean && \
        make -j &&\
        cp progs/tic /d/p/angora/fast/unibench/infotocap/infotocap &&\
        make clean && USE_TRACK=1 ASAN_OPTIONS="detect_leaks=0" make -j &&\
        cp progs/tic /d/p/angora/taint/unibench/infotocap/infotocap &&\
        make clean
} &

{
    cd /autofz_bench/unibench/jq-1.5 && ./configure --disable-shared &&\
        make clean && \
        make -j &&\
        cp jq /d/p/angora/fast/unibench/jq &&\
        make clean && USE_TRACK=1 make -j &&\
        cp jq /d/p/angora/taint/unibench/jq &&\
        make clean
} &

{
    cd /autofz_bench/unibench/mujs-1.0.2 &&\
        make clean && \
        build=debug make -j &&\
        cp build/debug/mujs /d/p/angora/fast/unibench/mujs &&\
        make clean && USE_TRACK=1 build=debug make -j &&\
        cp build/debug/mujs /d/p/angora/taint/unibench/mujs &&\
        make clean
} &

{
    cd /autofz_bench/unibench/xpdf-4.00 && cmake . &&\
        make clean && \
        make -j &&\
        cp xpdf/pdftotext /d/p/angora/fast/unibench/pdftotext &&\
        make clean && USE_TRACK=1 make -j &&\
        cp xpdf/pdftotext /d/p/angora/taint/unibench/pdftotext &&\
        make clean
} &

#--disable-amalgamation can be used for coverage build
{
    cd /autofz_bench/unibench/SQLite-3.8.9 && ./configure --disable-shared &&\
        make clean && \
        make -j &&\
        cp sqlite3 /d/p/angora/fast/unibench/sqlite3 &&\
        make clean && USE_TRACK=1 ASAN_OPTIONS="detect_leaks=0" make -j &&\
        cp sqlite3 /d/p/angora/taint/unibench/sqlite3 &&\
        make clean
} &

{
    cd /autofz_bench/unibench/binutils-5279478 &&\
        ./configure --disable-shared &&\
        for i in bfd libiberty opcodes libctf; do cd $i; ./configure --disable-shared && make clean && make -j; cd ..; done  &&\
        cd binutils  &&\
        ./configure --disable-shared &&\
        make nm-new &&\
        cp nm-new /d/p/angora/fast/unibench/nm/nm &&\
        cd /autofz_bench/unibench/binutils-5279478 &&\
        for i in bfd libiberty opcodes libctf; do cd $i; make clean && USE_TRACK=1 make -j; cd ..; done  &&\
        cd binutils  && make clean &&\
        USE_TRACK=1 make nm-new &&\
        cp nm-new /d/p/angora/taint/unibench/nm/nm &&\
        cd .. && make distclean
} &

{
    cd /autofz_bench/unibench/binutils-2.28 && ./configure --disable-shared && \
        make clean && \
        make -j && \
        cp binutils/objdump /d/p/angora/fast/unibench/objdump &&\
        make clean && USE_TRACK=1 ASAN_OPTIONS="detect_leaks=0" make -j &&\
        cp binutils/objdump /d/p/angora/taint/unibench/objdump &&\
        make clean
} &

{
    cd /autofz_bench/unibench/libpcap-1.8.1 && ./configure --disable-shared &&\
        make clean && \
        make -j &&\
        cd /autofz_bench/unibench/tcpdump-4.8.1 && ./configure &&\
        make clean && \
        make -j &&\
        cp tcpdump /d/p/angora/fast/unibench/tcpdump &&\
        cd /autofz_bench/unibench/libpcap-1.8.1 &&\
        make clean && USE_TRACK=1 make -j &&\
        cd /autofz_bench/unibench/tcpdump-4.8.1 &&\
        make clean && USE_TRACK=1 make -j &&\
        cp tcpdump /d/p/angora/taint/unibench/tcpdump &&\
        make clean && cd /autofz_bench/unibench/libpcap-1.8.1 && make clean
} &

# ./configure --disable-acl --disable-libcap --without-gmp --without-selinux --disable-xattr v.s gllvm
wait
