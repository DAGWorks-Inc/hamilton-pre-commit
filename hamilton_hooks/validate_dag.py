import argparse
from pathlib import Path
from typing import Optional, Sequence

from hamilton_hooks.common import import_module, build_driver

PASS = 0
FAIL = 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Generate visualization of Hamilton modules that were edited."""
    parser = argparse.ArgumentParser()
    parser.add_argument("module_paths", nargs="+", help="Hamilton modules to validate.")
    args = parser.parse_args(argv)

    exit_code = PASS

    for arg in args.module_paths:
        module_path = Path(arg)
        try:
            module = import_module(module_path)
        except ModuleNotFoundError as e:
            print(e)
            exit_code |= 1
            continue

        try:
            build_driver(module)
        except Exception as e:
            print(e)
            exit_code |= 1


    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
