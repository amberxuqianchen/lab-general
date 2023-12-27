import sys
from utils import add_numbers

def main(arg1, arg2):
    num1 = int(arg1)
    num2 = int(arg2)
    result = add_numbers(num1, num2)
    print(f"Running with arguments {arg1} and {arg2}")
    print(f"The sum is: {result}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
