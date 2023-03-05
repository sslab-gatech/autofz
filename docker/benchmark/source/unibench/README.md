# UniBench
20 benchmark programs



## Image

| Program            | Version           | Official Website                        | Get Latest                                | Issue                                                        | Fuzzing Arguments | CVE                                                          |
| ------------------ | ----------------- | --------------------------------------- | ----------------------------------------- | ------------------------------------------------------------ | ----------------- | ------------------------------------------------------------ |
| exiv2              | 0.26              | https://www.exiv2.org/                  | https://github.com/Exiv2/exiv2            | [github](https://github.com/Exiv2/exiv2/issues)              | @@                | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=exiv2) |
| gdk-pixbuf-pixdata | gdk-pixbuf 2.31.1 | https://developer.gnome.org/gdk-pixbuf/ | https://gitlab.gnome.org/GNOME/gdk-pixbuf | [gitlab](https://gitlab.gnome.org/GNOME/gdk-pixbuf/issues)   | @@ /dev/null      | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=gdk-pixbuf) |
| imginfo            | jasper 2.0.12     | https://www.ece.uvic.ca/~frodo/jasper/  | https://github.com/mdadams/jasper         | [github](https://github.com/mdadams/jasper/issues) [bugzilla](https://bugs.ghostscript.com/buglist.cgi?product=JasPer) | -f @@             | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=jasper) |
| jhead              | 3.00              | https://www.sentex.ca/~mwandel/jhead/   |                                           | Bugzilla [redhat](https://bugzilla.redhat.com/buglist.cgi?component=jhead) [ubuntu](https://bugs.launchpad.net/ubuntu/+source/jhead) | @@                | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=jhead) |
| tiffsplit          | libtiff 3.9.7     | https://gitlab.com/libtiff/libtiff      | https://gitlab.com/libtiff/libtiff        | [gitlab](https://gitlab.com/libtiff/libtiff/issues)          | @@                | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=libtiff) |

## Audio

Attention: running mp3gain may change the input file, **make a copy of your crash files before validating**, otherwise you may not be able to reproduce crashes.

| Program | Version        | Official Website                | Get Latest                                                   | Issue                                                      | Fuzzing Arguments                              | CVE link                                                     |
| ------- | -------------- | ------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| lame    | 3.99.5         | https://lame.sourceforge.io/    | https://sourceforge.net/p/lame/svn/HEAD/tree/trunk/lame/     | [sourceforge](https://sourceforge.net/p/lame/bugs/)        | @@ /dev/null                                   | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=lame) |
| mp3gain | 1.5.2          | http://mp3gain.sourceforge.net/ | https://sourceforge.net/p/mp3gain/code/ci/master/tree/mp3gain/ | [sourceforge](https://sourceforge.net/p/mp3gain/bugs/)     | @@ (Attention: input file will be overwritten) | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=mp3gain) |
| wav2swf | swftools 0.9.2 | http://swftools.org/            | https://github.com/matthiaskramm/swftools                    | [github](https://github.com/matthiaskramm/swftools/issues) | -o /dev/null @@                                | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=swftools) |

## Video

| Program | Version          | Official Website         | Get Latest                                  | Issue                                                        | Fuzzing Arguments                              | CVE link                                                     |
| ------- | ---------------- | ------------------------ | ------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------ |
| ffmpeg  | 4.0.1            | https://www.ffmpeg.org/  | https://git.ffmpeg.org/ffmpeg.git           | [debian](https://security-tracker.debian.org/tracker/source-package/ffmpeg) | -y -i @@ -c:v mpeg4 -c:a copy -f mp4 /dev/null | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=ffmpeg) |
| flvmeta | 1.2.1            | https://www.flvmeta.com/ | https://github.com/noirotm/flvmeta          | [github](https://github.com/noirotm/flvmeta/issues)          | @@                                             | N.A.                                                         |
| mp42aac | Bento4 1.5.1-628 | https://www.bento4.com/  | https://github.com/axiomatic-systems/Bento4 | [github](https://github.com/axiomatic-systems/Bento4/issues) | @@ /dev/null                                   | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=Bento4) |

## Text

Note: infotocap is actually binary `tic`, the name **infotocap** should not be changed. This is like busybox, which functionality is determined by its binary name

| Program   | Version      | Official Website                      | Get Latest                                            | Issue                                                        | Fuzzing Arguments | CVE link                                                     |
| --------- | ------------ | ------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------ | ----------------- | ------------------------------------------------------------ |
| cflow     | 1.6          | https://www.gnu.org/software/cflow/   | https://git.savannah.gnu.org/cgit/cflow.git           | [maillist](https://lists.gnu.org/archive/html/bug-cflow/)  [bug-cflow@gnu.org](mailto:bug-cflow@gnu.org) | @@                | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=cflow) |
| infotocap | ncurses 6.1  | https://www.gnu.org/software/ncurses/ | http://invisible-mirror.net/archives/ncurses/current/ | [maillist](https://lists.gnu.org/archive/html/bug-ncurses/) [bug-ncurses@gnu.org](mailto:bug-ncurses@gnu.org) | -o /dev/null @@   | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=ncurses) |
| jq        | 1.5          | https://stedolan.github.io/jq/        | https://github.com/stedolan/jq                        | [github](https://github.com/stedolan/jq/issues)              | . @@              | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=jq)  |
| mujs      | 1.0.2        | https://mujs.com/                     | https://github.com/ccxvii/mujs                        | [github](https://github.com/ccxvii/mujs/issues) [bugzilla](https://bugs.ghostscript.com/buglist.cgi?product=MuJS) | @@                | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=mujs) |
| pdftotext | 4.00         | https://www.xpdfreader.com/           | https://www.xpdfreader.com/download.html              | [forum](https://forum.xpdfreader.com//)                      | @@ /dev/null      | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=xpdf) |
| sqlite3   | SQLite 3.8.9 | https://www.sqlite.org/index.html     | https://www.sqlite.org/cgi/src/doc/trunk/README.md    | [tickets](https://www.sqlite.org/cgi/src/rptview?rn=1)       | (stdin)           | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=sqlite) |

## Binary

| Program | Version          | Official Website                       | Get Latest                                    | Issue                                                        | Fuzzing Arguments                                            | CVE link                                                     |
| ------- | ---------------- | -------------------------------------- | --------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| nm      | binutils 5279478 | https://www.gnu.org/software/binutils/ | http://sourceware.org/git/?p=binutils-gdb.git | [bugzilla](https://sourceware.org/bugzilla/buglist.cgi?component=binutils&product=binutils) | -A -a -l -S -s --special-syms --synthetic --with-symbol-versions -D @@ | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=binutils) |
| objdump | binutils 2.28    | https://www.gnu.org/software/binutils/ | http://sourceware.org/git/?p=binutils-gdb.git | [bugzilla](https://sourceware.org/bugzilla/buglist.cgi?component=binutils&product=binutils) | -S @@                                                        | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=binutils) |

## Network

| Program | Version               | Official Website         | Get Latest                                   | Issue                                                        | Fuzzing Arguments | CVE link                                                     |
| ------- | --------------------- | ------------------------ | -------------------------------------------- | ------------------------------------------------------------ | ----------------- | ------------------------------------------------------------ |
| tcpdump | 4.8.1 + libpcap 1.8.1 | https://www.tcpdump.org/ | https://github.com/the-tcpdump-group/tcpdump | [github](https://github.com/the-tcpdump-group/tcpdump/issues) | -e -vv -nr @@     | [link](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=tcpdump) |

