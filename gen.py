import argparse
from problem import Problem

def generate_variants(path, folder, seed: int):
    problems = (
        Problem.read_problems_from_dir(folder)
        if folder
        else [Problem(path)]
    )
    
    for _, problem in enumerate(problems):
        if not problem.generate_prompts(seed):
            print(f"Test generation failed for problem {problem.id}")
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate problems from description. Does not require API keys.')
    parser.add_argument('--path', type=str, help='a problem path')
    parser.add_argument('--folder', type=str, help='path to a folder of problems')
    parser.add_argument('--seed', type=int, help='an optional integer seed', default=0)
    
    args = parser.parse_args()
    if args.path == None and args.folder == None:
        print("I need either a --path or --folder to generate problems")
        exit(1)
    generate_variants(args.path, args.folder, args.seed)