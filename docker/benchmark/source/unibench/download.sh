#!/bin/bash
d(){
    wget -nc "$1" -O "$2";
}
d https://github.com/Exiv2/exiv2/archive/v0.26.zip exiv2-0.26.zip
d https://gitlab.gnome.org/GNOME/gdk-pixbuf/-/archive/2.31.1/gdk-pixbuf-2.31.1.zip gdk-pixbuf-2.31.1.zip
d https://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.12.tar.gz jasper-2.0.12.tar.gz
d https://www.sentex.ca/~mwandel/jhead/jhead-3.00.tar.gz jhead-3.00.tar.gz
d https://gitlab.com/libtiff/libtiff/-/archive/Release-v3-9-7/libtiff-Release-v3-9-7.zip libtiff-3.9.7.zip
d https://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz/download lame-3.99.5.tar.gz
d https://sourceforge.net/projects/mp3gain/files/mp3gain/1.5.2/mp3gain-1_5_2-src.zip/download mp3gain-1.5.2.zip
d http://www.swftools.org/swftools-0.9.2.tar.gz swftools-0.9.2.tar.gz
d https://www.ffmpeg.org/releases/ffmpeg-4.0.1.tar.gz ffmpeg-4.0.1.tar.gz
d https://flvmeta.com/files/flvmeta-1.2.1.tar.gz flvmeta-1.2.1.tar.gz
d https://github.com/axiomatic-systems/Bento4/archive/v1.5.1-628.zip Bento4-1.5.1-628.zip
d ftp://download.gnu.org.ua/pub/release/cflow/cflow-1.6.tar.gz cflow-1.6.tar.gz
d http://invisible-mirror.net/archives/ncurses/ncurses-6.1.tar.gz ncurses-6.1.tar.gz
d https://github.com/stedolan/jq/releases/download/jq-1.5/jq-1.5.zip jq-1.5.zip
d https://mujs.com/downloads/mujs-1.0.2.zip mujs-1.0.2.zip
d https://xpdfreader-dl.s3.amazonaws.com/old/xpdf-4.00.tar.gz xpdf-4.00.tar.gz 
d https://www.sqlite.org/cgi/src/zip/8a8ffc86/SQLite-8a8ffc86.zip SQLite-3.8.9.zip

if [ ! -f "binutils-5279478.zip" ]; then
    git clone -n git://sourceware.org/git/binutils-gdb.git
    cd binutils-gdb
    git checkout 5279478
    rm -r .git
    cd ..
    mv binutils-gdb binutils_5279478
    zip -r binutils-5279478.zip binutils_5279478/
    rm -r binutils_5279478/
fi

d ftp://sourceware.org/pub/binutils/releases/binutils-2.28.tar.gz binutils-2.28.tar.gz
d https://www.tcpdump.org/release/tcpdump-4.8.1.tar.gz tcpdump-4.8.1.tar.gz
d https://www.tcpdump.org/release/libpcap-1.8.1.tar.gz libpcap-1.8.1.tar.gz