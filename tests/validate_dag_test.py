from hamilton_hooks import validate_dag
from testing.util import get_resource_path


def test_fail_on_invalid_dag():
    exit_code = validate_dag.main([get_resource_path("invalid_module.py")])
    assert exit_code == 1


def test_success_on_valid_dag():
    exit_code = validate_dag.main([get_resource_path("valid_module_v1.py")])
    assert exit_code == 0   
