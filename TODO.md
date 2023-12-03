### TODO
- Pass configuration to the driver. Could be specified as YAML dictionary in `.pre-commit-config.yaml`
- Handle failures to build the DAG.
- The same logic could be reused to validate the DAG, but without generating a visualization. Almost feels like a test, but seems relevant as a pre-commit hook.