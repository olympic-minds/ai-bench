from problem import Problem
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Generate jsonl for problems in given dir")
    parser.add_argument('problems_folder', type=str, help="Path to problems folder")
    parser.add_argument('jsonl_path', type=str, help="Path to json file")
    
    args = parser.parse_args()
    
    problems = []
    for root, dirs, files in os.walk(args.problems_folder):
        for dir_name in dirs:
            path = os.path.join(root, dir_name)
            problem = Problem(path)
            problems.append(problem)
    Problem.write_problems_to_jsonl_file(problems, args.jsonl_path)

if __name__ == "__main__":
    main()