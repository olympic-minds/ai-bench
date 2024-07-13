import os
from typing import Dict, List, Tuple
from problem import Problem
from chat import Chat
from gemini import Gemini
from chatgpt import ChatGPT
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
from tqdm import tqdm

from enum import Enum

from util import process_files
class ChatModel(Enum):
    GPT = "gpt"
    GEMINI = "gemini"

SYSTEM_PROMPT = "What should @ANS be substituted for, for assert to evaluate true? Output only substitution for @ANS. Make sure to only print the substitution."

def get_chat(chatModel: ChatModel):
    if chatModel == ChatModel.GEMINI:
        return Gemini()
    elif chatModel == ChatModel.GPT:
        return ChatGPT()
    
# evaluates the model. Returns problem_id, the number of successful answers and the total number of problems
def evaluate_test(problem_path: str, client: Chat) -> tuple[str, int, int]:
    prompt_in_dir = f"{problem_path}/{Problem.dirs['prompt_in']}"
    prompt_out_dir = f"{problem_path}/{Problem.dirs['prompt_in']}"
    solution_out_dir = f"{problem_path}/{Problem.dirs['prompt_in']}"
    
    def fetch_model_response(prompt: str) -> str:
        response = client.prompt(SYSTEM_PROMPT, prompt)
        return Problem.clean_output(response)
        
    
    
    process_files(
        input_dir=prompt_in_dir,
        output_dir=prompt_out_dir,
        modify_content=fetch_model_response,
        modify_filename=lambda filename: filename
    )

    prompt_outs = os.listdir(prompt_out_dir)
    solution_outs = os.listdir(solution_out_dir)

    if len(prompt_outs) != len(solution_outs):
        raise ValueError(f"Directories '{prompt_outs}' and '{solution_outs}' do not have the same number of .out files.")

    return problem_path, \
        sum(1 for prompt_out_filename, solution_out_filename in zip(sorted(prompt_outs), sorted(solution_outs))
            if open(os.path.join(prompt_outs, prompt_out_filename), 'r').read() == open(os.path.join(solution_outs, solution_out_filename), 'r').read()),  \
        len(prompt_outs)



def eval_chat(problems: List[Problem], client: Chat, num_workers: int, num_tests: int, num_prompts: int, verbose: bool = False, precompiled_stdc: str = None):
    print("Generating tests...")
    for problem_num, problem in enumerate(problems):
        for test_num in range(num_tests):
            if not problem.generate_prompts(precompiled_stdc):
                print("Test generation failed")
                return
        
    results = Dict[str, Tuple[int, int]]
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []

        for problem in problems:
            future = executor.submit(evaluate_test, (problem.id, client))
            futures.append(future)

        print("Evalutaing model...")
        for future in tqdm(as_completed(futures), total=len(futures)):
            problem_id, result = future.result()
            results[problem_id] = result
       
    if verbose:
        for id, correct in results.items():
            if isinstance(correct, Tuple[int, int]):
                print(f"PROBLEM {id} CORRECT: {correct[0]}/{correct[1]}")
    return {id: correct[0]/correct[1] if isinstance(correct, Tuple[int, int]) else 0 for id, correct in results.items()}
    

import argparse

def main():
    parser = argparse.ArgumentParser(description="Evaluate model on a problem")
    parser.add_argument('path', type=str, help="Path to problem or directory of problems")
    parser.add_argument('model', type=ChatModel, help="Model gpt/gemini")
    parser.add_argument('--tests', '-t', type=int, help="Number of generated tests",  default=5)
    parser.add_argument('--prompts', '-p', type=int, help="Number of prompts for evert test case", default=5)
    parser.add_argument('--workers', '-w', type=int, help="Max number of workers",  default=5)
    parser.add_argument('--precompiled_stdc', '-s', type=str, help="Path to precompiled bits/stdc++ header (without .gch)")
    parser.add_argument('--folder', '-f', action='store_true', help="Path is the path to problems directory")
    parser.add_argument('--verbose', '-v', action='store_true', help="Print prompts and expected outputs")

    args = parser.parse_args()
    
    problems = Problem.read_problems_from_dir(args.path) if args.folder else [Problem(args.path)]
    client = get_chat(args.model)
    results = eval_chat(problems, client, args.workers, args.tests, args.prompts, args.verbose, args.precompiled_stdc)
    for id, accuracy in results.items():
        print(f"PROBLEM {id} ACCURACY: {accuracy}")
   

if __name__ == "__main__":
    main()
