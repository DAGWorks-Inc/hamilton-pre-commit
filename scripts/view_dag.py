import argparse
import importlib
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import Optional, Sequence

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from hamilton import driver


PASS = 0
FAIL = 1


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
    

def get_visualization_file_path(
    module_path: Path, dest_dir: Optional[str] = None,
) -> Path:
    """Get the visualization file path. It shares the name of the module,
    but with the `.png` extension.

    If `dest_dir` is specified, generate visualizations there.
    By default, generate visualizations next to the .py file.
    """
    if dest_dir:
        viz_path = Path(dest_dir, module_path.stem, ".png")
    else:
        viz_path = module_path.with_suffix(".png")
    return viz_path


def add_commit_metadata(viz_path: Path, file_hash: str) -> None:
    """Open a PNG file and add the `file_hash` to the metadata"""
    metadata = PngInfo()
    metadata.add_text("file_hash", file_hash)

    image = Image.open(viz_path)
    image.save(viz_path, pnginfo=metadata)


def check_viz_commit(file_path: Path, file_hash: str) -> bool:
    """Open a PNG file and check if its metadata corresponds
    to the passed `file_hash` value.
    
    NOTE. If True, you need to regenerate the figure
    """
    if not file_path.exists():
        return True

    metadata = Image.open(file_path).text
    return metadata.get("file_hash") != file_hash


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


def visualize_dag(dr: driver.Driver, file_path: Path) -> None:
    """Generate a visualization for the Driver."""
    # remove the file path extension since it will be added by graphviz
    dr.display_all_functions(
        str(file_path.with_suffix("")),
        render_kwargs=dict(format="png", view=False)
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Generate visualization of Hamilton modules that were edited."""
    parser = argparse.ArgumentParser()
    parser.add_argument("module_paths", nargs="+", help="Hamilton modules to visualize.")
    parser.add_argument("-d", "--dest-dir")
    args = parser.parse_args(argv)

    exit_code = PASS

    for arg in args.module_paths:
        module_path = Path(arg)
        module_hash = get_current_file_hash(module_path)
        viz_path = get_visualization_file_path(module_path)
        exit_code_for_file = check_viz_commit(viz_path, module_hash)

        if exit_code_for_file:
            module = import_module(module_path)
            dr = build_driver(module)
            visualize_dag(dr, viz_path)
            add_commit_metadata(viz_path, module_hash)
            print(f"Rendered `{module_path.stem}` at {viz_path.parent}")

        exit_code |= exit_code_for_file
        
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
