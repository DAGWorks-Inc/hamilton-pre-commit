import json
import subprocess
from typing import Optional, Sequence


PASS = 0
FAIL = 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Execute a list of commands using the Hamilton CLI"""
    exit_code = PASS
    
    if argv is None:
        print("hamilton-hooks.cli-command received no command to execute")
        return exit_code
        
    for cmd in argv:
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
            response = json.loads(result.stdout)
            
            if response["success"] is False:
                raise ValueError
                
        except Exception as e:
            print(e)
            exit_code |= 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
