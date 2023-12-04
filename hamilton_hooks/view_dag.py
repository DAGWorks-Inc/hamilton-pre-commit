import argparse
from pathlib import Path
from typing import Optional, Sequence

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from hamilton import driver

from hamilton_hooks import common


PASS = 0
FAIL = 1


def get_visualization_file_path(
    module_path: Path, dest_dir: Optional[str] = None,
) -> Path:
    """Get the visualization file path. It shares the name of the module,
    but with the `.png` extension.

    If `dest_dir` is specified, generate visualizations there.
    By default, generate visualizations next to the .py file.
    """
    if dest_dir:
        viz_path = Path(dest_dir, module_path.stem).with_suffix(".png")
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


def visualize_dag(dr: driver.Driver, file_path: Path) -> None:
    """Generate a visualization for the Driver."""
    # remove the file path extension since it will be added by graphviz
    dr.display_all_functions(
        str(file_path.with_suffix("")),
        render_kwargs=dict(format="png", view=False)
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Generate visualization of Hamilton modules that were edited."""
    parser = argparse.ArgumentParser()
    parser.add_argument("module_paths", nargs="+", help="Hamilton modules to visualize.")
    parser.add_argument("-d", "--dest-dir")
    args = parser.parse_args(argv)

    exit_code = PASS

    for m in args.module_paths:
        module_path = Path(m)
        module_hash = common.get_current_file_hash(file_path=module_path)
        viz_path = get_visualization_file_path(
            module_path=module_path, dest_dir=args.dest_dir,
        )
        exit_code_for_file = check_viz_commit(viz_path, module_hash)

        if exit_code_for_file:
            dr = common.build_driver(
                module=common.import_module(module_path)
            )
            visualize_dag(dr, viz_path)
            add_commit_metadata(viz_path, module_hash)
            print(f"Rendered `{module_path.stem}` at {viz_path.parent}")

        exit_code |= exit_code_for_file
        
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
