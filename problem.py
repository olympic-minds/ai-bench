import os
import subprocess
import random
import json
import hashlib

from util import process_files

class Problem:
    IN_KEYWORD = "@IN_{num}"
    OUT_KEYWORD = "@ANS"
    
    INGEN_EXEC_PATH = "./bin/ingen_{sum}.e"
    SOLUTION_EXEC_PATH = "./bin/solution_{sum}.e"
    
    TESTLIB_PATH = "testlib/testlib.h"
    READWRITER_PATH = "testlib/readwriter.h"

    dirs = {
        "in": "in",
        "solution-in": "solution-in",
        "out": "out",
        "prompt-in": "prompt-in",
        "prompt-out": "prompt-out"
    }
    
    def __init__(self, folder_path=None):
        self.ingen = ""
        self.solution = ""
        self.statement = ""
        self.id = folder_path # todo: consider security of this bit
        if folder_path:
            self.read_from_folder(folder_path)

    def read_from_folder(self, folder_path):
        ingen_path = os.path.join(folder_path, 'gen.cpp')
        solution_path = os.path.join(folder_path, 'solution.cpp')
        statement_path = os.path.join(folder_path, 'problem-statement.md')

        with open(ingen_path, 'r') as ingen_file:
            self.ingen = ingen_file.read()
            
        with open(solution_path, 'r') as solution_file:
            self.solution = solution_file.read()
        
        with open(statement_path, 'r') as statement_file:
            self.statement = statement_file.read()

    @staticmethod
    def compile_cpp(code: str, executable: str, include_testlib: bool = False, precompiled_stdc_path: str = None):
        executable = executable.format(sum = hashlib.md5(code.encode('utf-8')).hexdigest())
        if os.path.isfile(executable):
            return executable
        
        directory = os.path.dirname(executable)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        compile_command = ["g++", "-std=c++20"]
        
        if include_testlib:
            compile_command += ["-include", Problem.TESTLIB_PATH, "-include", Problem.READWRITER_PATH]
            
        if precompiled_stdc_path is not None:
            compile_command += ["-include", precompiled_stdc_path]
            
        compile_command += ["-o", executable, "-x", "c++","-"]
        
        process = subprocess.Popen(compile_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate(input=code.encode())

        if process.returncode != 0:
            print("Compilation failed with the following error:")
            print(stderr.decode())
            return
        return executable
        

    def generate_tests(self, seed: int) -> bool:
        run_command = [self.ingen_bin]
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=f"{seed}\n".encode())

        if process.returncode != 0:
            print(f"Ingen execution failed (return code: {process.returncode}) with the following error:")
            print(stderr.decode())
            return False
    
        return True
    
    def generate_solution(self, test: str) -> str:
        run_command = [self.solution_bin]
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=test.encode())

        if process.returncode != 0:
            print(f"Solution execution failed (return code: {process.returncode}) with the following error:")
            print(stderr.decode())
            return ""
    
        return stdout.decode()
    
    @staticmethod
    def clean_output(output: str):
        output = output.replace(' ', '').replace('\n', '')
        output = output.removeprefix('```cpp').removeprefix('```cpp').removesuffix('```')
        return output
        
    def generate_prompts(self, precompiled_stdc_path: str = None) -> bool:
        self.ingen_bin = Problem.compile_cpp(self.ingen, Problem.INGEN_EXEC_PATH, True, precompiled_stdc_path)
        self.solution_bin = Problem.compile_cpp(self.solution, Problem.SOLUTION_EXEC_PATH, False, precompiled_stdc_path)
        
        if self.ingen_bin is None or self.solution_bin is None:
            return False
        
        random_seed = random.randint(0, 10000)
        if(not self.generate_tests(random_seed)):
            return False
        
        def generate_prompt(input: str) -> str:
            prompt = self.statement
            for i, input_line in enumerate(input.splitlines()):
                prompt = prompt.replace(Problem.IN_KEYWORD.format(num = i+1), input_line)
            return prompt.replace(Problem.OUT_KEYWORD, "@ANS")

        def get_prompt_filename(in_filename: str) -> str:
            base, _ = os.path.splitext(in_filename)
            return f'prompt_{base}.txt'

        in_directory = f'{self.id}/in'
        prompt_directory = f'{self.id}/{self.dirs["prompt_in"]}'

        # generate prompts from ins, which were generated into in/ directory by gen.cpp
        process_files(
            input_dir=in_directory, 
            output_dir=prompt_directory, 
            modify_content=generate_prompt, 
            modify_filename=get_prompt_filename
        )
        
        def get_out_filename(in_filename: str) -> str:
            base, _ = os.path.splitext(in_filename)
            return f'{base}.out'

        solution_in_directory = f'{self.id}/solution-in'
        solution_out_in_directory = f'{self.id}/out'
        
        # generate solutions from ins, which were generated into solution-in/ directory by gen.cpp
        process_files(
            input_dir=solution_in_directory, 
            output_dir=solution_out_in_directory, 
            modify_content=self.generate_solution,
            modify_filename=get_out_filename
        )
        
        return True

    def to_dict(self):
        return {
            'ingen': self.ingen,
            'solution': self.solution,
            'statement': self.statement,
            'id': self.id
        }

    @staticmethod
    def from_dict(data):
        problem = Problem()
        problem.ingen = data['ingen']
        problem.solution = data['solution']
        problem.statement = data['statement']
        problem.id = data['id']
        return problem

    @staticmethod
    def write_problems_to_jsonl_file(problems, file_path: str):
        with open(file_path, 'w') as jsonl_file:
            for problem in problems:
                jsonl_file.write(json.dumps(problem.to_dict()) + '\n')

    @staticmethod
    def read_problems_from_jsonl_file(file_path: str):
        problems = []
        with open(file_path, 'r') as jsonl_file:
            for line in jsonl_file:
                problem_dict = json.loads(line.strip())
                problems.append(Problem.from_dict(problem_dict))
        return problems
    
    @staticmethod
    def read_problems_from_dir(dir_path: str):
        problems = []
        for root, dirs, files in os.walk(dir_path):
            for dir_name in dirs:
                path = os.path.join(root, dir_name)
                problem = Problem(path)
                problems.append(problem)
        return problems
