from problem import Problem
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: {} <path>".format(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    
    problem = Problem(path)
    prompt, output = problem.generate_prompt(4)

if __name__ == "__main__":
    main()
