# autofz
[![Docker Pulls](https://img.shields.io/docker/pulls/fuyu0425/autofz)](https://hub.docker.com/r/fuyu0425/autofz) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7701474.svg)](https://doi.org/10.5281/zenodo.7701474)

autofz is a meta fuzzer for automated fuzzer composition at runtime.

For technical details, please check our [paper](https://gts3.org/assets/papers/2023/fu:autofz.pdf) ([extended version](https://arxiv.org/abs/2302.12879)), "autofz: Automated Fuzzer Composition at Runtime" published at USENIX Security'23.

Some part of the source code might use `autofuzz` (which is the old name of `autofz`).

We provided the following for artifact evaluation:
- A pre-built docker image which includes all baseline fuzzers and benchmarks used in the paper.
- A VM that configures all necessary things and can be used to launch the docker containers. If you want to use the VM, please jump to [VM setup section](#vm-setup).

## Directory Structure
- `autofz`: main directory for autofz framework
    - `main.py`: the entry point for autofz framework
    - `cli.py`: argument parsing, which lists all tuning parameters for autofz
    - `config.py`: config file for baseline fuzzers and benchmarks
      - queue/crash directories for fuzzers
      - arguments for each benchmark
    - `evaluator.py`: the thread calculating AFL bitmap for each baseline fuzzer
    - `aflforkserver.so`: from quickcov component of CUPID, used to get AFL bitmap coverage.
    - `wather.py`: Inotify handler for new files in fuzzer directories, modify from CollabFuzz
    - `fuzzer_driver`: directory for fuzzer API implementations
        - `main.py`: entry-point of fuzzer driver
            - `afl.py`: AFL-based fuzzers, same for other files
- `afl-cov`: modified from [original afl-cov](https://github.com/mrash/afl-cov) to do post-processing on fuzzing output to get line/branch (edge) coverage over time.


## Installing (Skipped if you are using the provided VM)

### required system packages
- `docker`
- `docker-compose`

<!-- ### autofz -->
<!-- `cd` into the directory containing `setup.py` -->
<!-- ```sh -->
<!-- pip install . -->
<!-- ``` -->

<!-- Then you can called `autofz --help` to verify whether you install successfully. -->

### Pull docker image
```sh
docker pull fuyu0425/autofz
docker tag fuyu0425/autofz autofz
```

## Before running
### UID check
Make sure your uid in the host is `2000`, which is the same as the user in the docker container.
  - We use this trick to prevent from using `sudo` and make the mounted volume can be read outside of docker.

It's not mandatory. If you don't do that, you might need to use `sudo` to bypass some permission issues.


### Increase inotify limits
```sh
sysctl -w fs.inotify.max_user_instances=8192
sysctl -w fs.inotify.max_user_watches=524288
```
To make it persistent between reboot; add the following lines to `/etc/sysctl.conf` on the host.
```
fs.inotify.max_user_instances=8192
fs.inotify.max_user_watches=524288
```

## Running
### Launching a docker container
```sh
docker run --rm --privileged -it autofz /bin/bash
```
Note that, the result is not preserved. To preserve the fuzzing output, we need
to mount a docker volume.

```sh
docker run --rm --privileged -v $PWD:/work/autofz -w /work/autofz -it autofz /bin/bash
```
This command mount (by `-v`) your current directory (`$PWD`) to `/work/autofz` in the container and change the working directory to `/work/autofz` (by `-w`).

Afterward, make sure the fuzzing output directory is under `/work/autofz` and it will be preserved under your `$PWD`.


### Init
After entering the docker container, run the following commands; it will setup necessary parameters for fuzzing and create the cgroups.
```sh
sudo /init.sh
```

Or you can do it the manually, the following is the content of `init.sh`
```sh
#!/bin/bash
echo "" > /proc/sys/kernel/core_pattern
echo 0 > /proc/sys/kernel/core_uses_pid
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
echo 0 > /proc/sys/kernel/yama/ptrace_scope
echo 1 > /proc/sys/kernel/sched_child_runs_first
echo 0 > /proc/sys/kernel/randomize_va_space

# get container id
CPU_CGROUP_PATH=$(cat /proc/1/cpuset)
CID=$(basename ${CPU_CGROUP_PATH})

set -x
# create subgroup
cgcreate -t autofz -a autofz -g cpu:/autofz
```

Note that `/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` might not exist in VM; just ignore that error.


### Fuzzing ###
All the evaluation is run by `autofz` framework.
Please refer to [cli.py](./autofz/cli.py) for all possible arguments.

#### autofz ####

For example, we want to fuzz `exiv2` (by `-t`) using 4 fuzzers by `-f`: `AFL`, `FairFuzz`, `AFLFast`, `QSYM` (`-f all` to use all baseline fuzzers, which is the one we used in the evaluation). `-T` for the timeout (human friendly foramt like `1d`, `24h` or `30m`).

The fuzzing result reside in `output` (by specifying `-o`).

##### Single-core implementation #####

```sh
autofz -o output -T 24h -f afl fairfuzz aflfast qsym -t exiv2
```

##### Multi-core implementation #####

For multi-core implementation, we need to specify CPUs/jobs (by `-j`) and `-p` (shorthand for `--parallel`).
```sh
autofz -o output -T 24h -f afl fairfuzz aflfast qsym -j4 -p -t exiv2
```

##### Tuning the parameter of two-phase algorithm.
- `--prep`: prepration time (in seconds) (default: 300)
- `--focus`: focus time (in seconds) (default: 300)
- `--diff_threshold`: initial threshold (default: 100)
- the default values are used in the paper.


#### EnFuzz/CUPID/autofz- ####

For example, we want to fuzz `exiv2` (by `-t`) using 4 fuzzers by `-f`: `AFL`, `FairFuzz`, `AFLFast`, `QSYM`.

Additionally, you can specify how many CPUs/jobs by `-j` arguments; here we use 4 CPUs (one for each fuzzer).

<!-- Note that by specifiying `-j` other than 1, we use the multi-core implemention. -->

It is recommended to use at least the same number of CPUs as the number of fuzzers to prevent resource competition.

Finally, enable EnFuzz mode by `--enfuzz ${SYNC_TIME}`; it specifies the time interval (in seconds) for seed synchronization.

```sh
autofz -o output -T 24h -f afl fairfuzz aflfast qsym -p -j4 -t exiv2 --enfuzz 300
```


#### Run a single fuzzer ####

For example, AFL only by specifying `--focus-one`.
```sh
autofz -o output -T 24h -f afl -t exiv2 --focus-one afl
```

#### Example output result ####

```
??? tree -L 1 output
output
????????? eval
????????? exiv2
????????? exiv2_2023-02-27-14-49-57.json
```
- `eval`: baseline fuzzer evaluation directory
- `exvi2`: baseline fuzzer raw output
- `exiv2_2023-02-27-14-49-57.json`: log of `autofz`

`output/eval/global` is the aggregate output for all baseline fuzzers, which is the final `autofz` output.
```
.
????????? bitmap
????????? crashes
????????? unique_bugs
????????? unique_bugs_ip
????????? unique_bugs_trace
????????? unique_bugs_trace3
```
- `crashes`: crashes output by fuzzers
- `unique_bugs_*`: deduplicated bugs by `ip` (instruction pointer), `trace` (whole stack traces), `trace3` (top 3 stack frame).


### aflforkserver.so
It is built from [quickcov](https://github.com/egueler/quickcov), which is a part of CUPID.

## Inspect log files of autofz
The log file of `autofz` is in JSON format and can be easily parsed by standard
libraries in most programming languages.

To inspect the log file (e.g. `exiv2.json`), we recommend using a tool called
[jq](https://github.com/stedolan/jq), which can be installed by the
package manager in most Linux distributions. We already installed it in both the
docker image and the VM image.

There are many fields in the log file.

One of them is `log`, which can be retrieved by the following command.

```sh
jq .log exiv2.json
```

The output is an array and each element of the array contains the coverage
(`bitmap` field) and
unique bugs information and the timestamp for that record. By default, a new log
entry is appended for every 60 seconds.

To get the results based on rounds, we can use the following commands.

```sh
jq .round exiv2.json
```

The output is also an array and each element is the result of one round.

Each element records information for different phases in one round (e.g. the
coverage before/after preparation/focus phases, resource allocation metadata and
current difference threshold.)

In the provided VM, we provided one of the fuzzing log with the path

`/home/autofz/output_exiv2/exiv2.json`.


## Output Post Processing by afl-cov
We use `exiv2` as an exmaple.
```sh
afl-cov --output output \
        -d output/exiv2 \
        -t queue \
        --input /seeds/unibench/general_evaluation/jpg \
        --coverage-cmd='/d/p/cov/unibench/exiv2/exiv2 @@' \
        --code-dir /autofz_bench/unibench/exiv2-0.26 \
        -T 1s \
        --cover-corpus \
        --disable-lcov-web \
        --ignore-core-pattern --overwrite --enable-branch-coverage
```
- Please use `afl-cov --help` to see the meaning of argument definition.
- `output/exiv2` is the raw fuzzing output directory of baseline fuzzers.
Note that `output` is the root of fuzzing output directory of `autofz`. 
- `queue` is directory name to find the queue directory of fuzzers. It can only support one name now.
- `/seeds/unibench/general_evaluation/jpg` is the seeds to fuzz `exiv2`.
- `/d/p/cov/unibench/exiv2/exiv2` is binary compiled with coverage support. Please check [`docker/benchmark/coverage/Dockerfile`](./docker/benchmark/coverage/Dockerfile).
- `/autofz_bench/unibench/exiv2-0.26`: source code directory for `exiv2`, it is required to get line/branch coverage.
- `--output ouput`, it will create a `cov` directory under `output`.
- afl-cov will store the log under `output/cov/cov.json`. It has the similiar structure as the log of `autofz`.

## VM Setup ###

1. Download the VirtualBox and install the Oracle Extension Pack
2. Download and import the OVA files
   - [OVA URL](https://doi.org/10.5281/zenodo.7701474)
3. Start the VM, the credential is `autofz:autofz`
   - SSH is installed, and you need to configure VirtualBox network first to ssh into the VM. Port forwarding would be the easiest way.
4. All the data will in the home directory

#### Resource
- CPU: 2 (more if you want to use multi-core implementation)
- RAM: 8GM (really depends on the chosen fuzzers and target you want to fuzz, autofz itself takes few memory.)

#### How to run
See [running](#running) section.

#### Example Output Result
`/home/autofz/output_exiv2` is the sample output after 24 hours fuzzing of autofz.


## Fuzzing using docker image on the host
Example
```
autofz.sh run --rm -v `pwd`:/work/autofz -w /work/autofz autofz -o output -t exiv2 -f all -T 24h
```



## Docker image
Pre-built docker image:
```
docker pull fuyu0425/autofz
docekr tag fuyu0425/autofz autofz
```

### Build docker image
We have built the docker image for you, but you want to build it by yourself; here is the process.

First build baseline fuzzers and benchmarks.

```
./docker/build.sh
```

Then, build the all-in-one docker including `autofz` and all the fuzzers/benchmarks.

```
./build.sh
```

You can tune the image name/tag in these `build.sh`.

You might need to tune `_UID` and `GID` (they are hard-coded to `2000` when building the pre-built image) in `build.sh` to bypass docker volume permission issue if you don't want to use root user.



#### Build Note/Warning

The build script parallels the compilation process a lot by making the jobs runs in the background (by inserting `&` at the end of shell commands). It will takes a lot of CPU and RAM (especially during linking). Please remove `&` in build scripts (`build.sh` or `build_all.sh` under `docker/benchmark`) when you are building under less performant machines.

## Extend
Please look at the content of [config.py](./autofz/config.py) first; it has some comments.

### How to add a baseline fuzzer
- build the fuzzer
- add it to `config.py` under `Config['fuzzer']`

#### Add the necessary group code in autofz
- implement fuzzer API/driver under `autofz/fuzzer_driver` directories.
  - Only Start/Pause/Resume/Stop APIs are needed in single-core (default) mode.
  - Please take a look at `autofz/fuzzer_driver/afl.py` as a reference.
  - You might need to add some code in`autofz/fuzzer_driver/db.py` and `autofz/fuzzer_driver/main.py` too.
- add fuzzer to `autofz/mytypy.py`.
- add fuzzer to `autofz/watcher.py`.

### How to add a target
- build the target for each baseline fuzzer
- add it to `config.py`  under `Config['target']`

### Reinstall after changing `config.py`
After modifying `config.py`, you need to do `pip install` again.

decoupling `config.py` is on the roadmap.

## Reference

### Fuzzers
- [AFL](https://github.com/google/AFL)
- [AFLFast](https://github.com/mboehme/aflfast)
- [AFL++](https://github.com/AFLplusplus/AFLplusplus)
- [Angora](https://github.com/AngoraFuzzer/Angora)
- [FairFuzz](https://github.com/carolemieux/afl-rb)
- [LAF-Intel](https://lafintel.wordpress.com/)
  - AFL++ version is used
- [LearnAFL](https://github.com/MoonLight-SteinsGate/LearnAFL)
- [LibFuzzer](https://github.com/carolemieux/afl-rb)
  - [patched version](https://github.com/phi-go/llvm-project/tree/fuzzer_sync) from CUPID team to enable seed sync
- [MOpt](https://github.com/puppet-meteor/MOpt-AFL)
- [QSYM](https://github.com/sslab-gatech/qsym)
- [Radamsa](https://gitlab.com/akihe/radamsa)
  - AFL++ version with custom mutators is used
- [RedQueen](https://github.com/RUB-SysSec/redqueen)
  - AFL++ version is used


### Collaborative fuzzing
- [ENFUZZ](https://github.com/enfuzz/enfuzz)
- [CUPID](https://github.com/RUB-SysSec/cupid)
- [collabfuzz](https://github.com/vusec/collabfuzz)

### Benchmarks
- [UNIFUZZ](https://github.com/unifuzz)
- [Fuzzer Test Suite](https://github.com/google/fuzzer-test-suite)

### Coverage tools
- [quickcov](https://github.com/egueler/quickcov)
- [afl-cov](https://github.com/mrash/afl-cov)

Thanks above projects for open sourcing their code.
