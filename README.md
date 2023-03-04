# autofz
[![Docker Pulls](https://img.shields.io/docker/pulls/fuyu0425/autofz)](https://hub.docker.com/r/fuyu0425/autofz)

autofz is a meta fuzzer for automated fuzzer composition at runtime.

For technical details, please check our [paper](https://gts3.org/assets/papers/2023/fu:autofz.pdf) ([extended version](https://arxiv.org/abs/2302.12879)), "autofz: Automated Fuzzer Composition at Runtime" published at USENIX Security'23.

Some part of the source code might use `autofuzz` (which is the old name of `autofz`).

We provided the following for artifact evaluation:
- A pre-built docker image which includes all baseline fuzzers and benchmarks used in the paper.
- A VM that configures all necessary things and can be used to luanch the docker containers. If you want to use the VM, plase jump to [VM setup section](#vm-setup).

## Directory Structure
- `autofz`: main directory for autofz framework
    - `main.py`: the entry point for autofz framework
    - `cli.py`: argument parsing, which lists all tuning parameters for autofz
    - `config.py`: config file for baseline fuzzers and benchmarks
      - queue/crash directories for fuzzers
      - arguments for each benchmark
    - `evaluator.py`: the thread calculating AFL bitmap for each baseline fuzzer
    - `aflforkserver.so`: from quickcov component of CUPID, used to get AFL bitmap coverage.
    - `wather.py`: Inotify handler for new files in fuzzer directores, modify from CollabFuzz
    - `fuzzer_driver`: directory for fuzzer API implementations
        - `main.py`: entrypoint of fuzzer driver
        - `afl.py`: AFL-based fuzzers, same for other files
- `afl-cov`: modifed from [original afl-cov](https://github.com/mrash/afl-cov) to do post-processing on fuzzing output to get line/branch (edge) coverage over time.


## Installing (Skipped if you are using the provided VM)

### required system packages
Please refer to the `Dockerfile`.

### autofz
`cd` into the directory containing `setup.py`
```sh
pip install .
```

Then you can called `autofz --help` to verify whether you install successfully.


## Before running
Make sure your uid in the host is `2000`, which is the same as the user in the docker container.
  - We use this trick to prevent from using `sudo` and make the mounted volumn can be read outside of docker.

It's not mandatory. If you don't do that, you might need to use `sudo` to bypass some permission issues.


## Running
### Init
After entering the docker container, run the following commands; it will setup necessary paramters for fuzzing and create the cgroups.
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


### Increase inotify limits
```sh
sysctl -w fs.inotify.max_user_instances=8192
sysctl -w fs.inotify.max_user_watches=524288
```
To make it persistent between reboot; add the following lines to `/etc/sysctl.conf`.
```
fs.inotify.max_user_instances=8192
fs.inotify.max_user_watches=524288
```

### Fuzzing ###
All the evaluation is run by `autofz` framework.

#### autofz ####

For example, we want to fuzz `exiv2` (by `-t`) using 4 fuzzers by `-f`: `AFL`, `FairFuzz`, `AFLFast`, `QSYM`.

##### Single-core implementation #####

```sh
autofz -o output -T 30m -f afl fairfuzz aflfast qsym -t exiv2
```

##### Multi-core implementation #####

For multi-core implementaiton, we need to specify CPUs/jobs (by `-j`) and `-p` (shorthand for `--parallel`).
```sh
autofz -o output -T 30m -f afl fairfuzz aflfast qsym -j4 -p -t exiv2
```


#### EnFuzz/CUPID/autofz- ####

For example, we want to fuzz `exiv2` (by `-t`) using 4 fuzzers by `-f`: `AFL`, `FairFuzz`, `AFLFast`, `QSYM`.

Additionally, you can specifiy how many CPUs/jobs by `-j` arguments; here we use 4 CPUs (one for each fuzzer).

<!-- Note that by specifiying `-j` other than 1, we use the multi-core implemention. -->

It is recommended to use at least the same number of CPUs as the number of fuzzers to prevent resource competition.

Finally, enable EnFuzz mode by `--enfuzz ${SYNC_TIME}`; it specifies the time interval for seed synchronization.

```sh
autofz -o output -T 30m -f afl fairfuzz aflfast qsym -j4 -t exiv2 --enfuzz 300
```
The fuzzing result reside in `output` (by specifying `-o`).


#### Run a single fuzzer ####

For example, AFL only by specifying `--focus-one`.
```sh
autofz -o output -T 30m -f afl -t exiv2 --focus-one afl
```

#### Example output result ####

```
❯ tree -L 1 output
output
├── eval
├── exiv2
├── exiv2_2023-02-27-14-49-57.json
```
- `eval`: baseline fuzzer evaluation directory
- `exvi2`: baseline fuzzer raw output
- `exiv2_2023-02-27-14-49-57.json`: log of `autofz`

`output/eval/global` is the aggregate output for all baseline fuzzers, which is the final `autofz` output.
```
.
├── bitmap
├── crashes
├── unique_bugs
├── unique_bugs_ip
├── unique_bugs_trace
└── unique_bugs_trace3
```
- `crashes`: crashes output by fuzzers
- `unique_bugs_*`: deduplicated bugs by `ip` (instruction pointer), `trace` (whole stack traces), `trace3` (top 3 stack frame).



### aflforkserver.so
It is built from [quickcov](https://github.com/egueler/quickcov), which is a part of CUPID.

## Output Post Processing by afl-cov
TODO

## VM Setup ###

1. Download the VirtualBox and install the Oracle Extension Pack
2. Download and import the OVA files
   - [OVA URL](https://TBD)
3. Start the VM, the credential is `autofz:autofz`
   - SSH is installed, and you need to configure VirtualBox network first to ssh into the VM. Port forwarding would be the easiet way.
4. All the data will in the home directory

#### Resource
- CPU: 2 (more if you want to use multi-core implementation)
- RAM: 8GM (really depends on the chosen fuzzers and target you want to fuzz, autofz itself takes few memory.)

#### How to run
See above.

#### Example Output Result
`/home/autofz/output_exiv2` is the sample output after 24 hours fuzzing of autofz.

## Build docker image
TODO

## Extend

### How to add a baseline fuzzer
- build the fuzzer
- add it to `config.py`

### How to add a target
- build the target for each baseline fuzzer
- add it to `config.py`

## Reference
- [ENFUZZ](https://github.com/enfuzz/enfuzz)
- [CUPID](https://github.com/RUB-SysSec/cupid)
- [quickcov](https://github.com/egueler/quickcov)
- [collabfuzz](https://github.com/vusec/collabfuzz)
- [UNIFUZZ](https://github.com/unifuzz)
- [fuzzer test suite](https://github.com/google/fuzzer-test-suite)
- [afl-cov](https://github.com/mrash/afl-cov)

Thanks above projects for open sourcing their code.
