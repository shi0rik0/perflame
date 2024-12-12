# perflame

## Description

perflame is a tool to streamline the process of profiling with Linux `perf` and generating flame graphs with [brendangregg/FlameGraph](https://github.com/brendangregg/FlameGraph).

## Installation

Clone the repository first and then you MUST initialize the submodules:

```bash
git clone https://github.com/shi0rik0/perflame.git
cd perflame
git submodule update --init --recursive
```

Then you can use `pip` to install the package:

```bash
pip install .
```

Or if you prefer `pipx`:

```bash
pipx install .
```

Then you should be able to use the `perflame` command.

## Examples

Profile a command:

```bash
perflame -o output.svg COMMAND
```

Profile all processes in the system for 10 seconds:

```bash
perflame -a -o output.svg sleep 10
```

`perflame` will use `sudo` by default. If you want to disable it, you can use the `--no-sudo` flag:

```bash
perflame --no-sudo -a -o output.svg sleep 10
```
