import argparse
from typing import List
from problem import Problem
from tqdm import tqdm


def generate_variants(
    problems: List[Problem], seed: int, parallel: int = 1, verbose: bool = False
) -> bool:
    print("Generating problems...")
    for _, problem in tqdm(enumerate(problems), total=len(problems)):
        if not problem.generate_prompts(seed, parallel, verbose):
            print(f"Test generation failed for problem {problem.id}")
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate problems from description. Does not require API keys."
    )
    parser.add_argument("path", type=str, help="a problem path")
    parser.add_argument(
        "--folder",
        "-f",
        action="store_true",
        help="Path is the path to problems directory",
    )
    parser.add_argument("--seed", type=int, help="an optional integer seed", default=1)
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print whole prompts instead of ins",
    )
    parser.add_argument(
        "--parallel",
        "-j",
        type=int,
        help="Number of cpus to use for compilation",
        default=1,
    )

    args = parser.parse_args()

    problems = (
        Problem.read_problems_from_dir(args.path)
        if args.folder
        else [Problem(args.path)]
    )
    generate_variants(problems, args.seed, args.parallel, args.verbose)
