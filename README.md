# Hamilton pre-commit hooks
This repository contains [pre-commit hooks](https://github.com/pre-commit/pre-commit) to improve the development experience with the open source dataflow library [Hamilton](https://github.com/dagworks-inc/hamilton).

# Installation
## Using pre-commit-hooks with pre-commit
Install [pre-commit](https://github.com/pre-commit/pre-commit) and add this to your `.pre-commit-config.yaml`
```yaml
- repo: https://github.com/zilto/hamilton-hooks
  rev: v0.1.0  # Use the ref you want to point at
  hooks:
    - id: cli-command
      additional_dependencies: [sf-hamilton, graphviz, typer]
      args: [  # a list of CLI commands passed as strings
        "hamilton build my_functions.py",
        "hamilton view -o my_func2.png my_func2.py",
      ]
```

## As a standalone package
If you'd like to use these hooks, they're also available as a standalone package.

Simply `pip install hamilton-hooks`

# License
Distributed under the terms of the MIT license, hamilton-pre-commit-hooks is free and open source software.

# Issues
If you encounter any problems, please [file an issue](https://github.com/zilto/hamilton-hooks/issues/new) along with a detailed description.
