from problem import Problem
import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        description="Generate jsonl for problems in given dir"
    )
    parser.add_argument("problems_folder", type=str, help="Path to problems folder")
    parser.add_argument("jsonl_path", type=str, help="Path to json file")

    args = parser.parse_args()

    problems = Problem.read_problems_from_dir(args.problems_folder)
    Problem.write_problems_to_jsonl_file(problems, args.jsonl_path)


if __name__ == "__main__":
    main()
