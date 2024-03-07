import sys
import json
import subprocess


PASS = 0
FAIL = 1


def main() -> int:
    """Execute a list of commands using the Hamilton CLI"""
    exit_code = PASS
    
    commands = sys.argv[1:]

    if len(commands) == 0:
        print("`hamilton-hooks.cli-command` received no command to execute")
        return exit_code
        
    for command in commands:
        try:
            args = command.split(" ")
            # insert `--json-out` right after `hamilton` for proper stdout parsing
            # no issue if `--json-out` is present twice
            args.insert(1, "--json-out")
            result = subprocess.run(args, stdout=subprocess.PIPE, text=True)
            response = json.loads(result.stdout)
            print(response)
            
            if response["success"] is False:
                raise ValueError
                
        except Exception as e:
            print(e)
            exit_code |= 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
