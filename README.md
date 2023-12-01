# Hamilton pre-commit hooks
This repository contains [pre-commit hooks](https://github.com/pre-commit/pre-commit) to improve the development experience with the open source dataflow library [Hamilton](https://github.com/dagworks-inc/hamilton).

## How to use
In your project, install the Python `pre-commit` package ([ref](https://pre-commit.com/)) and define a configuration.
1. `pip install pre-commit`
2. Define a `.pre-commit-config.yaml` file such as
```yaml
repos:
- repo: https://github.com/zilto/hamilton-pre-commit-hooks
  rev: v0.0.3
  hooks:
    - id: hamilton-view-dag
      name: Hamilton View DAG
      additional_dependencies: [sf-hamilton, graphviz, pillow]
      args: [
        /path/to/hamilton_module_a.py,
        /path/to/hamilton_module_b.py,
      ]
```

## Hooks available
`hamilton-view-dag`

Track Hamilton modules (`.py` files) and automatically generate DAG visualization when commiting changes to tracked files.
- Each `.py` builds an Hamilton Driver and generates a visualization of the same file name with `.png` extension next to it.
- Can specify a destination directory `dest_dir` where all visualizations are generated.

### TODO
- Pass configuration to the driver. Could be specified as YAML dictionary in `.pre-commit-config.yaml`
- Handle failures to build the DAG.
- The same logic could be reused to validate the DAG, but without generating a visualization. Almost feels like a test, but seems relevant as a pre-commit hook.