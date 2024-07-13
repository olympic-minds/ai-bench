from problem import Problem
from chat import Chat
from gemini import Gemini
from chatgpt import ChatGPT
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
from tqdm import tqdm

from enum import Enum
class ChatModel(Enum):
    GPT = "gpt"
    GEMINI = "gemini"

SYSTEM_PROMPT = "What should @ANS be substituted for, for assert to evaluate true? Output only substitution for @ANS. Make sure to only print the substitution."

def get_chat(chatModel: ChatModel):
    if chatModel == ChatModel.GEMINI:
        return Gemini()
    elif chatModel == ChatModel.GPT:
        return ChatGPT()
    
def evaluate_test(problem_id: str, client: Chat, prompt: str, expected_output: str, verbose: bool):
    response = client.prompt(SYSTEM_PROMPT, prompt)
    response = Problem.clean_output(response)
    if verbose:
        print(f"OUTPUT {expected_output} RESPONSE: {response}")
    return problem_id, int(response == expected_output)

def eval_chat(problems, client: Chat, size: int, num_workers: int, num_tests: int, num_prompts: int, verbose: bool = False, precompiled_stdc: str = None):
    print("Generating tests...")
    tests = []
    for problem_num, problem in enumerate(problems):
        for test_num in range(num_tests):
            prompt, output = problem.generate_prompt(size, precompiled_stdc)
            if prompt is None or output is None:
                print("Test generation failed")
                return
            if verbose:
                print(f"PROBLEM {problem.id} TEST {test_num} - PROMPT: {prompt}")
                print(f"PROBLEM {problem.id} TEST {test_num} - OUTPUT: {output}")
            tests.append((problem.id, prompt, output))
        
    results = Counter()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []

        for sample in tests:
            id, prompt, output = sample
            args = (id, client, prompt, output, verbose)
            for i in range(num_prompts):
                future = executor.submit(evaluate_test, *args)
                futures.append(future)

        print("Evalutaing model...")
        if verbose:
            for future in as_completed(futures):
                problem_id, result = future.result()
                results[problem_id] += result
        else:
            for future in tqdm(as_completed(futures), total=len(futures)):
                problem_id, result = future.result()
                results[problem_id] += result
       
    total_prompts = num_tests * num_prompts
    if verbose:
        for id, correct in results.items():
            print(f"PROBLEM {id} CORRECT: {correct}/{total_prompts}")
    results = {id: correct/total_prompts for id, correct in results.items()}
    return results
    

import argparse

def main():
    parser = argparse.ArgumentParser(description="Evaluate model on a problem")
    parser.add_argument('path', type=str, help="Path to problem or directory of problems")
    parser.add_argument('model', type=ChatModel, help="Model gpt/gemini")
    parser.add_argument('size', type=int, help="Size of the input")
    parser.add_argument('--tests', '-t', type=int, help="Number of generated tests",  default=5)
    parser.add_argument('--prompts', '-p', type=int, help="Number of prompts for evert test case", default=5)
    parser.add_argument('--workers', '-w', type=int, help="Max number of workers",  default=5)
    parser.add_argument('--precompiled_stdc', '-s', type=str, help="Path to precompiled bits/stdc++ header (without .gch)")
    parser.add_argument('--folder', '-f', action='store_true', help="Path is the path to problems directory")
    parser.add_argument('--verbose', '-v', action='store_true', help="Print prompts and expected outputs")

    args = parser.parse_args()
    
    problems = Problem.read_problems_from_dir(args.path) if args.folder else [Problem(args.path)]
    client = get_chat(args.model)
    results = eval_chat(problems, client, args.size, args.workers, args.tests, args.prompts, args.verbose, args.precompiled_stdc)
    for id, accuracy in results.items():
        print(f"PROBLEM {id} ACCURACY: {accuracy}")
   

if __name__ == "__main__":
    main()
