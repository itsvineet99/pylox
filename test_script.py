import subprocess
from pathlib import Path

def run_all_tests():
    # 1. Update this to point directly to the tests folder
    tests_dir = Path("tests") 
    
    # 2. Update this to point to the executable inside src (as you suggested!)
    lox_executable = "src/lox.py"

    lox_files = sorted(tests_dir.glob("*.lox"))

    if not lox_files:
        print("No .lox files found in the tests directory.")
        return

    print(f"Found {len(lox_files)} test files. Starting execution...\n")

    for test_file in lox_files:
        print(f"{'='*40}")
        print(f"Running: {test_file.name}")
        print(f"{'='*40}")
        
        subprocess.run(["python", lox_executable, str(test_file)])
        print() 

if __name__ == "__main__":
    run_all_tests()
