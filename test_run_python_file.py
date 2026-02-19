
from functions.run_python_file import run_python_file

def test_run_python_file():
    print(run_python_file("calculator", "main.py")) # should print the calculator's usage instructions
    print(run_python_file("calculator", "main.py", ["3 + 5"])) # should run the calculator... and out a nastyish result
    print(run_python_file("calculator", "tests.py")) # should run the calculator's tests successfully
    print(run_python_file("calculator", "../main.py")) # should return an error
    print(run_python_file("calculator", "nonexistent.py")) # should return an error
    print(run_python_file("calculator", "lorem.txt")) # should return an error


if __name__ == "__main__":
    test_run_python_file()