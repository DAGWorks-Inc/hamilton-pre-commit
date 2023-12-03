# Hamilton pre-commit hooks
This repository contains [pre-commit hooks](https://github.com/pre-commit/pre-commit) to improve the development experience with the open source dataflow library [Hamilton](https://github.com/dagworks-inc/hamilton).

# Installation
### Using pre-commit-hooks with pre-commit
Install [pre-commit](https://github.com/pre-commit/pre-commit) and add this to your `.pre-commit-config.yaml`
```yaml
- repo: https://github.com/zilto/hamilton-pre-commit-hooks
  rev: v0.0.3  # Use the ref you want to point at
  hooks:
    - id: hamilton-view-dag
    # - id: ...
```
### As a standalone package
If you'd like to use these hooks, they're also available as a standalone package.

Simply `pip install hamilton-pre-commit-hooks`


# Hooks available
`hamilton-view-dag`
```yaml
- id: hamilton-view-dag
  name: Hamilton View DAG
  additional_dependencies: [sf-hamilton, graphviz, pillow]
  args: [
    /path/to/hamilton_module_a.py,  # files to track
    /path/to/hamilton_module_b.py,
  ]
```

Track Hamilton modules (`.py` files) and automatically generate DAG visualization when commiting changes to tracked files.
- Each `.py` builds an Hamilton Driver and generates a visualization of the same file name with `.png` extension next to it.
- Can specify a destination directory `dest_dir` where all visualizations are generated.


# License
Distributed under the terms of the MIT license, hamilton-pre-commit-hooks is free and open source software.

# Issues
If you encounter any problems, please [file an issue](https://github.com/zilto/hamilton-pre-commit-hooks/issues/new) along with a detailed description.
