# Judge Server From VNOI (forked from DMOJ)

Setup [tutorial here](https://vnoi-admin.github.io/vnoj-docs/#/judge/setting_up_a_judge)

## Supported platforms and runtimes

The judge implements secure grading on Linux and FreeBSD machines.

|     | Linux | FreeBSD |
| --: | :---: | :-----: |
| x64 | [✔](https://github.com/DMOJ/judge-server/actions/workflows/build.yml) | [✔](https://ci.dmoj.ca/job/dmoj-judge-freebsd/) |
| x86 | ✔ | ¯\\\_(ツ)\_/¯ |
| x32 | ✔ | &mdash; |
| ARM | [✔](https://github.com/DMOJ/judge-server/actions/workflows/build.yml) | ❌ |

Versions up to and including [v1.4.0](https://github.com/DMOJ/judge-server/releases/tag/v1.4.0) also supported grading on Windows machines.

Versions up to and including [v3.0.2](https://github.com/DMOJ/judge-server/releases/tag/v3.0.2) also supported grading
with pure ptrace without seccomp, which is useful on Linux kernel versions before 4.8.

The DMOJ judge does **not** need a root user to run on Linux machines: it will run just fine under a normal user.

Supported languages include:

* C++ 11/14/17/20 (GCC and Clang)
* C 99/11
* Java 8-19
* Python 2/3
* PyPy 2/3
* Pascal
* Mono C#/F#/VB

The judge can also grade in the languages listed below:

* Ada
* Algol 68
* AWK
* Brain\*\*\*\*
* COBOL
* D
* Dart
* Forth
* Fortran
* Go
* Groovy
* Haskell
* INTERCAL
* JavaScript (Node.js and V8)
* Kotlin
* Lean 4
* LLVM IR
* Lua
* NASM
* Objective-C
* OCaml
* Perl
* PHP
* Pike
* Prolog
* Racket
* Ruby
* Rust
* Scala
* Chicken Scheme
* sed
* Steel Bank Common Lisp
* Swift
* Tcl
* Turing
* V8 JavaScript
* Zig

## Installation

Installing the DMOJ judge creates two executables in your Python's script directory: `dmoj` and `dmoj-cli`.
`dmoj` is used to connect a judge to a DMOJ site instance, while `dmoj-cli` provides a command-line interface to a
local judge, useful for testing problems.

For more detailed steps, read the [installation instructions](https://docs.dmoj.ca/#/judge/setting_up_a_judge).

Note that **the only Linux distribution with first-class support is the latest Debian**, with the default `apt` versions of all runtimes. This is [what we run on dmoj.ca](https://dmoj.ca/runtimes/matrix/), and it should "just work". While the judge will likely still work with other distributions and runtime versions, some runtimes might fail to initialize. In these cases, please [file an issue](https://github.com/DMOJ/judge-server/issues).

### Stable build

[![PyPI version](https://badge.fury.io/py/dmoj.svg)](https://pypi.org/project/dmoj/)
[![PyPI](https://img.shields.io/pypi/pyversions/dmoj.svg)](https://pypi.org/project/dmoj/)

We periodically publish builds [on PyPI](https://pypi.org/project/dmoj/). This is the easiest way to get started,
but may not contain all the latest features and improvements.

```bash
pip install dmoj
```

### Bleeding-edge build

This is the version of the codebase we run live on [dmoj.ca](https://dmoj.ca/).

```bash
git clone --recursive https://github.com/DMOJ/judge-server.git
cd judge-server
pip install -e .
```

Several environment variables can be specified to control the compilation of the sandbox:

* `DMOJ_TARGET_ARCH`; use it to override the default architecture specified for compiling the sandbox (via `-march`).
   Usually this is `native`, but will not be specified on ARM unless `DMOJ_TARGET_ARCH` is set (a generic, slow build will be compiled instead).

### With Docker

We maintain Docker images with all runtimes we support in the [runtimes-docker](https://github.com/DMOJ/runtimes-docker) project.

Runtimes are split into three tiers of decreasing support. Tier 1 includes
Python 2/3, C/C++ (GCC only), Java 8, and Pascal. Tier 3 contains all the
runtimes we run on [dmoj.ca](https://dmoj.ca/). Tier 2 contains some in-between
mix; read the `Dockerfile` for each tier for details. These images are rebuilt
and tested every week to contain the latest runtime versions.

The script below spawns a tier 1 judge image. It expects the relevant
environment variables to be set, the network device to be `enp1s0`, problems
to be placed under `/mnt/problems`, and judge-specific configuration to be in
`/mnt/problems/judge.yml`. Note that runtime configuration is already done for you,
and will be merged automatically into the `judge.yml` provided.

```bash
$ git clone --recursive https://github.com/DMOJ/judge-server.git
$ cd judge-server/.docker
$ make judge-tier1
$ exec docker run \
    --name judge \
    -p "$(ip addr show dev enp1s0 | perl -ne 'm@inet (.*)/.*@ and print$1 and exit')":9998:9998 \
    -v /mnt/problems:/problems \
    --cap-add=SYS_PTRACE \
    -d \
    --restart=always \
    dmoj/judge-tier1:latest \
    run -p15001 -s -c /problems/judge.yml \
    "$BRIDGE_ADDRESS" "$JUDGE_NAME" "$JUDGE_KEY"
```

## Usage

### Running a judge server

```bash
$ dmoj --help
usage: dmoj [-h] [-p SERVER_PORT] -c CONFIG [-l LOG_FILE] [--no-watchdog]
            [-a API_PORT] [-A API_HOST] [-s] [-k] [-T TRUSTED_CERTIFICATES]
            [-e ONLY_EXECUTORS | -x EXCLUDE_EXECUTORS] [--no-ansi]
            server_host [judge_name] [judge_key]

Spawns a judge for a submission server.

positional arguments:
  server_host           host to connect for the server
  judge_name            judge name (overrides configuration)
  judge_key             judge key (overrides configuration)

optional arguments:
  -h, --help            show this help message and exit
  -p SERVER_PORT, --server-port SERVER_PORT
                        port to connect for the server
  -c CONFIG, --config CONFIG
                        file to load judge configurations from
  -l LOG_FILE, --log-file LOG_FILE
                        log file to use
  --no-watchdog         disable use of watchdog on problem directories
  -a API_PORT, --api-port API_PORT
                        port to listen for the judge API (do not expose to
                        public, security is left as an exercise for the
                        reverse proxy)
  -A API_HOST, --api-host API_HOST
                        IPv4 address to listen for judge API
  -s, --secure          connect to server via TLS
  -k, --no-certificate-check
                        do not check TLS certificate
  -T TRUSTED_CERTIFICATES, --trusted-certificates TRUSTED_CERTIFICATES
                        use trusted certificate file instead of system
  -e ONLY_EXECUTORS, --only-executors ONLY_EXECUTORS
                        only listed executors will be loaded (comma-separated)
  -x EXCLUDE_EXECUTORS, --exclude-executors EXCLUDE_EXECUTORS
                        prevent listed executors from loading (comma-
                        separated)
  --no-ansi             disable ANSI output
  --skip-self-test      skip executor self-tests
```

### Running a CLI judge

```bash
$ dmoj-cli --help
usage: dmoj-cli [-h] -c CONFIG
                [-e ONLY_EXECUTORS | -x EXCLUDE_EXECUTORS]
                [--no-ansi]

Spawns a judge for a submission server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        file to load judge configurations from
  -e ONLY_EXECUTORS, --only-executors ONLY_EXECUTORS
                        only listed executors will be loaded (comma-separated)
  -x EXCLUDE_EXECUTORS, --exclude-executors EXCLUDE_EXECUTORS
                        prevent listed executors from loading (comma-
                        separated)
  --no-ansi             disable ANSI output
  --skip-self-test      skip executor self-tests
```

## Documentation

For info on the problem file format and more, [read the documentation](https://docs.dmoj.ca).
