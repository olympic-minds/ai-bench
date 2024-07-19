import os
import re
import shutil
import argparse
from problem import Problem
from typing import Dict, List, Tuple
from util import match_tests_to_prompts, TerminalColor


def print_evaluation_result_for_testcase(
    problem_path: str,
    prompt: str,
    input: str,
    solution_output: str,
    model_output: str,
    verbose: bool = False,
):
    width = shutil.get_terminal_size((60, 30)).columns

    def print_wraped(s: str):
        ansi_escape_regex = re.compile(r"\033\[[0-9;]*m")
        cleaned_string = re.sub(ansi_escape_regex, "", s)
        length = len(cleaned_string)
        print(f"{'-' * ((width - length) // 2)}{s}{'-' * ((width - length + 1) // 2)}")

    print_wraped(
        f"{TerminalColor.HEADER}{TerminalColor.BOLD}PROBLEM: {problem_path} | INPUT{TerminalColor.ENDC}"
    )
    if verbose:
        print(prompt.strip())
    else:
        print(input.strip())

    clean_solution_output = Problem.clean_output(solution_output)
    clean_model_output = Problem.get_last_integer(model_output)

    answer = (
        f"{TerminalColor.OKGREEN}ANSWER: {clean_solution_output}{TerminalColor.ENDC}"
    )
    output_color = (
        TerminalColor.OKGREEN
        if clean_solution_output == clean_model_output
        else TerminalColor.FAIL
    )
    output_string = "None" if clean_model_output is None else clean_model_output
    output = f"{output_color}OUTPUT: {output_string}{TerminalColor.ENDC}"
    print_wraped(f"{answer} | {output}")
    print()


def print_results_for_problem(problem_path: str, verbose: bool = False):
    prompt_in_dir = f"{problem_path}/{Problem.dirs['prompt_in']}"
    in_dir = f"{problem_path}/{Problem.dirs['in']}"
    model_out_dir = f"{problem_path}/{Problem.dirs['model_out']}"
    solution_out_dir = f"{problem_path}/{Problem.dirs['out']}"

    prompt_ins = os.listdir(prompt_in_dir)
    ins = os.listdir(in_dir)
    model_outs = os.listdir(model_out_dir)
    solution_outs = os.listdir(solution_out_dir)

    if len(model_outs) % len(ins) != 0:
        raise Problem.IncorrectNumberOfFiles(model_out_dir, solution_out_dir)

    num_tests = len(model_outs) // len(ins)

    model_outs = sorted(model_outs)
    prompt_ins = sorted(match_tests_to_prompts(prompt_ins, num_tests))
    ins = sorted(match_tests_to_prompts(ins, num_tests))
    solution_outs = sorted(match_tests_to_prompts(solution_outs, num_tests))

    for (
        prompt_in_filename,
        in_filename,
        model_out_filename,
        solution_out_filename,
    ) in zip(prompt_ins, ins, model_outs, solution_outs):
        print_evaluation_result_for_testcase(
            problem_path,
            open(os.path.join(prompt_in_dir, prompt_in_filename), "r").read(),
            open(os.path.join(in_dir, in_filename), "r").read(),
            open(os.path.join(model_out_dir, model_out_filename), "r").read(),
            open(os.path.join(solution_out_dir, solution_out_filename), "r").read(),
            verbose,
        )


def main():
    parser = argparse.ArgumentParser(description="Evaluate model on a problem")
    parser.add_argument(
        "path", type=str, help="Path to problem or directory of problems"
    )
    parser.add_argument(
        "--folder",
        "-f",
        action="store_true",
        help="Path is the path to problems directory",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print whole prompts instead of ins",
    )

    args = parser.parse_args()

    if args.folder:
        for problem in Problem.read_problems_from_dir(args.path):
            print_results_for_problem(problem.id, args.verbose)
    else:
        print_results_for_problem(args.path, args.verbose)


if __name__ == "__main__":
    main()
