# Hamilton pre-commit hooks
This repository contains [pre-commit hooks](https://github.com/pre-commit/pre-commit) to improve the development experience with the open source dataflow library [Hamilton](https://github.com/dagworks-inc/hamilton).

# Installation
## Using pre-commit-hooks with pre-commit
Install [pre-commit](https://github.com/pre-commit/pre-commit) and add this to your `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/zilto/hamilton-hooks
  rev: v0.1.1  # use a ref >= 0.1.0 
  hooks:
  - id: cli-command
    name: Hamilton CLI command
    additional_dependencies: ["sf-hamilton[visualization,cli]"]
    args: [
      hamilton build my_module.py,  # commands to execute
      hamilton build my_module2.py,  # they are executed in order
      hamilton validate --context config.json my_module.py my_module2.py,  # exits on the first failure
    ]
```

You can specify `hamilton` CLI commands to execute in a list. The hook will execute them in order. It's most useful with `hamilton build` to check for valid Hamilton syntax and `hamilton validate` to verify a specific dataflow path. More thorough validation should be done using tests given pre-commits are meant to be lightweight.

## Using the CLI manually
If you are interested in the command line tool, use `pip install sf-hamilton[cli]` and see the main [Hamilton repository](https://github.com/dagworks-inc/hamilton).

# License
Distributed under the terms of the MIT license, `hamilton-pre-commit-hooks` is free and open source software.

# Issues
If you encounter any problems, please [file an issue](https://github.com/zilto/hamilton-hooks/issues/new) along with a detailed description.
