from problem import Problem
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate tests for a problem")
    parser.add_argument("path", type=str, help="Path to problem")
    parser.add_argument(
        "--precompiled_stdc",
        "-s",
        type=str,
        help="Path to precompiled bits/stdc++ header (without .gch)",
    )

    args = parser.parse_args()

    problem = Problem(args.path)
    success = problem.generate_prompts(args.precompiled_stdc)
    if success:
        print("Generation was successful")
    else:
        print("Generation failed")


if __name__ == "__main__":
    main()
