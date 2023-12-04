import importlib
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import Optional

from hamilton import driver, telemetry

telemetry.disable_telemetry()


def get_current_file_hash(file_path: Path) -> str:
    """Call `git hash-object <filename>` in a subprocess"""
    try:
        return subprocess.run(
            ['git', 'hash-object', str(file_path)],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        ).stdout.strip()

    except subprocess.CalledProcessError as e:
        raise e


def import_module(module_path: Path) -> ModuleType:
    """Import a Python module dynamically from a file path."""
    module_name = str(module_path.stem)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def build_driver(
    module: ModuleType,
    config: Optional[dict] = None,
    allow_experimental_mode: bool = True,
) -> driver.Driver:
    """Build the Hamilton Driver using a single module.
    TODO. Allow to pass `config`
    """
    config = dict() if config is None else config
    return (
        driver.Builder()
        .enable_dynamic_execution(
            allow_experimental_mode=allow_experimental_mode
        )
        .with_config(config)
        .with_modules(module)
        .build()
    )
