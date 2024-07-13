from problem import Problem
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate test for a problem")
    parser.add_argument('path', type=str, help="Path to problem")
    parser.add_argument('size', type=int, help="Size of the input")
    
    args = parser.parse_args()
    
    problem = Problem(args.path)
    prompt, output = problem.generate_prompt(args.size)
    print(f"PROMPT: {prompt}")
    print(f"OUTPUT: {output}")

if __name__ == "__main__":
    main()
