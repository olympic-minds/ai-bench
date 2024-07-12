from problem import Problem
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: {} <path>".format(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    
    problem = Problem(path)
    prompt, output = problem.generate_prompt(4)
    print(f"PROMPT: {prompt}")
    print(f"OUTPUT: {output}")

if __name__ == "__main__":
    main()

# # Generate JSON from the problem
# json_str = problem.to_json()
# print(json_str)

# Create a list of problems
# problems = [problem, problem]  # Example with the same problem repeated

# Write the list of problems to a JSON file
# Problem.write_problems_to_jsonl_file(problems, 'problems.jsonl')

# Read the list of problems from a JSON file
# problems_from_file = Problem.read_problems_from_jsonl_file('problems.jsonl')
# for prob in problems_from_file:
#     print(prob.ingen, prob.statement)
