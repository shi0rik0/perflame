import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import pkg_resources
import shutil
import argparse
import tempfile
from pathlib import Path
import random
import string
import subprocess


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class TempFile:

    def __init__(self, path):
        self._path = Path(tempfile.gettempdir()).resolve() / path

    def __enter__(self) -> Path:
        return self._path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._path.exists():
            self._path.unlink()
        return False


def main():
    for command in ['perf', 'perl']:
        if shutil.which(command) is None:
            print(
                f"The command `{command}` is not found in PATH. Please install it."
            )
            return

    parser = argparse.ArgumentParser(description='Profile with Linux perf and draw flame graphs.')
    parser.add_argument('-a',
                        '--all',
                        action='store_true',
                        help='If set, all processes will be profiled')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        required=True,
                        help='Output file path')
    parser.add_argument('command',
                        nargs=argparse.REMAINDER,
                        help='Command to execute')
    args = parser.parse_args()

    all_processes: bool = args.all
    output_path: str = args.output
    command: str = ' '.join(args.command)

    prefix = 'perflame_' + generate_random_string(6)
    with TempFile(f'{prefix}_perf.data') as perf_record_out, TempFile(
            f'{prefix}_out.perf') as perf_script_out, TempFile(
                f'{prefix}_out.folded') as folded_out:
        # 1. Run 'perf record'
        subprocess.run(
            f'perf record -o {perf_record_out} -g {'-a' if all_processes else ''} -- {command}',
            shell=True)
        
        # 2. Run 'perf script'
        subprocess.run(
            f'perf script -i {perf_record_out} > {perf_script_out}', shell=True),
        
        # 3. Run 'stackcollapse-perf.pl'
        stackcollapse = pkg_resources.resource_filename('perflame', 'FlameGraph/stackcollapse-perf.pl')
        subprocess.run(
            f'perl {stackcollapse} {perf_script_out} > {folded_out}',
            shell=True)

        # 4. Run 'flamegraph.pl'
        flamegraph = pkg_resources.resource_filename('perflame', 'FlameGraph/flamegraph.pl')
        subprocess.run(
            f'perl {flamegraph} {folded_out} > {output_path}', shell=True)
        
    print(f'Successfully generated a flame graph at {output_path}')