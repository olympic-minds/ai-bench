import argparse
from problem import Problem

def generate_variants(path, folder: bool, seed: int):
    problems = (
        Problem.read_problems_from_dir(path)
        if folder
        else [Problem(path)]
    )
    
    for _, problem in enumerate(problems):
        if not problem.generate_prompts(seed):
            print(f"Test generation failed for problem {problem.id}")
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate problems from description. Does not require API keys.')
    parser.add_argument('path', type=str, help='a problem path')
    parser.add_argument(
        "--folder",
        "-f",
        action="store_true",
        help="Path is the path to problems directory",
    )
    parser.add_argument('--seed', type=int, help='an optional integer seed', default=0)
    
    args = parser.parse_args()
    generate_variants(args.path, args.folder, args.seed)