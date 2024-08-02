import os
import subprocess
import random
import json
import hashlib
import re
from util import process_files


class Problem:
    IN_KEYWORD = "@IN_{num}"
    OUT_KEYWORD = "@ANS"

    INGEN_EXEC_PATH = "./gen"
    SOLUTION_EXEC_PATH = "./solution"

    dirs = {
        "in": "in",
        "solution-in": "solution-in",
        "out": "out",
        "prompt_in": "prompt-in",
        "model_out": "model-out",
    }

    class SolutionExecutionFailed(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    class InvalidSolutionOutputFormat(Exception):
        def __init__(self, output):
            self.output = output
            self.message = f"Invalid solution output format, it should be a single integer, but got: {output}"
            super().__init__(self.message)

    class IncorrectNumberOfFiles(Exception):
        def __init__(self, model_out_dir, solution_out_dir):
            self.message = f"""Directories '{model_out_dir}' and '{solution_out_dir}' have incorrect number of files.
                        The number of files in '{model_out_dir}' should be equal to the number of files in '{solution_out_dir} multipled by the number of tests (-t parameter)'
                        """
            super().__init__(self.message)

    def __init__(self, folder_path: str = ""):
        self.ingen = ""
        self.solution = ""
        self.statement = ""
        self.id = folder_path  # todo: consider security of this bit
        if folder_path != "":
            self.read_from_folder(folder_path)

    def read_from_folder(self, folder_path):
        ingen_path = os.path.join(folder_path, "gen.cpp")
        solution_path = os.path.join(folder_path, "solution.cpp")
        statement_path = os.path.join(folder_path, "problem-statement.md")

        with open(ingen_path, "r") as ingen_file:
            self.ingen = ingen_file.read()

        with open(solution_path, "r") as solution_file:
            self.solution = solution_file.read()

        with open(statement_path, "r") as statement_file:
            self.statement = statement_file.read()

    @staticmethod
    def compile_cpp(
        problem_path: str,
    ) -> str | None:
        result = subprocess.run(['make'], cwd=problem_path, check=True, capture_output=True, text=True)
        return # todo: handle error

    def generate_tests(self, seed: int) -> bool:
        try:
            process = subprocess.run([self.INGEN_EXEC_PATH], input=str(seed), cwd=self.id, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
        return True # todo: handle error

    def generate_solution(self, test: str) -> str:
        process = subprocess.run([self.SOLUTION_EXEC_PATH], input=str(test), cwd=self.id, check=True, capture_output=True, text=True)
        return process.stdout

    @staticmethod
    def clean_output(solution_output: str) -> int:
        solution_output = solution_output.strip()
        try:
            return int(solution_output)
        except ValueError as e:
            raise Problem.InvalidSolutionOutputFormat(solution_output) from e

    @staticmethod
    def get_last_integer(output: str) -> int | None:
        numbers = re.findall(r"[-\+]?\d+", output)
        if numbers:
            return int(numbers[-1])

    @staticmethod
    def compare_outputs(
        solution_output: str,
        model_output: str,
    ) -> bool:
        clean_solution_output = Problem.clean_output(solution_output)
        clean_model_output = Problem.get_last_integer(model_output)
        return clean_solution_output == clean_model_output

    def generate_prompts(self, seed: int) -> bool:
        Problem.compile_cpp(self.id)

        if not self.generate_tests(seed):
            return False

        def generate_prompt(input: str) -> str:
            prompt = self.statement
            for i, input_line in enumerate(input.splitlines()):
                prompt = prompt.replace(
                    Problem.IN_KEYWORD.format(num=i + 1), input_line
                )
            return prompt.replace(Problem.OUT_KEYWORD, "@ANS")

        def get_prompt_filename(in_filename: str) -> str:
            base, _ = os.path.splitext(in_filename)
            return f"prompt_{base}.txt"

        in_directory = f'{self.id}/{Problem.dirs["in"]}'
        directory = os.path.dirname(in_directory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        prompt_directory = f'{self.id}/{self.dirs["prompt_in"]}'
        directory = os.path.dirname(prompt_directory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # generate prompts from ins, which were generated into in/ directory by gen.cpp
        process_files(
            input_dir=in_directory,
            output_dir=prompt_directory,
            modify_content=lambda content: [generate_prompt(content)],
            modify_filename=lambda filename: [get_prompt_filename(filename)],
        )

        def get_out_filename(in_filename: str) -> str:
            base, _ = os.path.splitext(in_filename)
            return f"{base}.out"

        solution_in_directory = f'{self.id}/{Problem.dirs["solution-in"]}'
        solution_out_in_directory = f'{self.id}/{Problem.dirs["out"]}'

        # generate solutions from ins, which were generated into solution-in/ directory by gen.cpp
        try:
            process_files(
                input_dir=solution_in_directory,
                output_dir=solution_out_in_directory,
                modify_content=lambda test_in: [
                    str(Problem.clean_output(self.generate_solution(test_in)))
                ],
                modify_filename=lambda filename: [get_out_filename(filename)],
            )
        except (
            Problem.SolutionExecutionFailed,
            Problem.InvalidSolutionOutputFormat,
        ) as e:
            print(e.message)
            return False

        return True

    def to_dict(self):
        return {
            "ingen": self.ingen,
            "solution": self.solution,
            "statement": self.statement,
            "id": self.id,
        }

    @staticmethod
    def from_dict(data):
        problem = Problem()
        problem.ingen = data["ingen"]
        problem.solution = data["solution"]
        problem.statement = data["statement"]
        problem.id = data["id"]
        return problem

    @staticmethod
    def write_problems_to_jsonl_file(problems, file_path: str):
        with open(file_path, "w") as jsonl_file:
            for problem in problems:
                jsonl_file.write(json.dumps(problem.to_dict()) + "\n")

    @staticmethod
    def read_problems_from_jsonl_file(file_path: str):
        problems = []
        with open(file_path, "r") as jsonl_file:
            for line in jsonl_file:
                problem_dict = json.loads(line.strip())
                problems.append(Problem.from_dict(problem_dict))
        return problems

    @staticmethod
    def read_problems_from_dir(dir_path: str):
        problems = []
        for dirname in os.listdir(dir_path):
            problem_dir_path = os.path.join(dir_path, dirname)

            if not os.path.isdir(problem_dir_path):
                continue

            problem = Problem(problem_dir_path)
            problems.append(problem)
        return problems
