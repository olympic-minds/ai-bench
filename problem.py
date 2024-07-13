import os
import subprocess
import random
import json
import hashlib

class Problem:
    IN_KEYWORD = "@IN_{num}"
    OUT_KEYWORD = "@ANS"
    
    INGEN_EXEC_PATH = "./bin/ingen_{sum}.e"
    SOLUTION_EXEC_PATH = "./bin/solution_{sum}.e"
    
    
    def __init__(self, folder_path=None):
        self.ingen = ""
        self.solution = ""
        self.statement = ""
        self.id = folder_path
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
    def compile_cpp(code: str, executable: str):
        executable = executable.format(sum = hashlib.md5(code.encode('utf-8')).hexdigest())
        if os.path.isfile(executable):
            return executable

        directory = os.path.dirname(executable)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        compile_command = ["g++", "-o", executable, "-x", "c++", "-"]
        process = subprocess.Popen(compile_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate(input=code.encode())

        if process.returncode != 0:
            print("Compilation failed with the following error:")
            print(stderr.decode())
            return
        return executable
        

    def generate_test(self, size: int, random_seed: int, format: int):
        run_command = [self.ingen_bin]
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=f"{size} {random_seed} {format}\n".encode())

        if process.returncode != 0:
            print(f"Ingen execution failed (return code: {process.returncode}) with the following error:")
            print(stderr.decode())
            return
    
        return stdout.decode()
    
    def get_output(self, test: str):
        run_command = [self.solution_bin]
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=test.encode())

        if process.returncode != 0:
            print(f"Solution execution failed (return code: {process.returncode}) with the following error:")
            print(stderr.decode())
            return
    
        return stdout.decode()
    
    @staticmethod
    def clean_output(output: str):
        output = output.replace(' ', '').replace('\n', '')
        output = output.removeprefix('```cpp').removeprefix('```cpp').removesuffix('```')
        return output
        
    def generate_prompt(self, size: int):
        self.ingen_bin = Problem.compile_cpp(self.ingen, Problem.INGEN_EXEC_PATH)
        self.solution_bin = Problem.compile_cpp(self.solution, Problem.SOLUTION_EXEC_PATH)
        if self.ingen_bin is None or self.solution_bin is None:
            return None, None
        
        random_seed = random.randint(0, 10000)
        test_prompt = self.generate_test(size, random_seed, 0)
        if test_prompt is None:
            return None, None
        test_prompt = test_prompt.split('\n')
        test_out = self.generate_test(size, random_seed, 1)
        # print("test_prompt: ", test_prompt)
        # print("test_out: ", test_out)
        if test_out is None:
            return None, None
        output = self.get_output(test_out)
        if output is None:
            return None, None
        prompt = self.statement
        for i, t in enumerate(test_prompt):
            prompt = prompt.replace(Problem.IN_KEYWORD.format(num = i+1), t)
        prompt = prompt.replace(Problem.OUT_KEYWORD, "@ANS")
        return prompt, Problem.clean_output(output)

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
