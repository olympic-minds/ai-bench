from problem import Problem
from chat import Chat
from gemini import Gemini
from chatgpt import ChatGPT
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
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
    
def evaluate_test(client: Chat, prompt: str, expected_output: str, verbose: bool):
    response = client.prompt(SYSTEM_PROMPT, prompt)
    response = Problem.clean_output(response)
    if verbose:
        print(f"OUTPUT {expected_output} RESPONSE: {response}")
    return int(response == expected_output)

def eval_chat(problem: Problem, client: Chat, size: int, num_workers: int = 4, num_tests: int = 5, num_prompts: int = 5, verbose: bool = False):
    correct = 0
    print("Generating tests...")
    tests = []
    for test_num in range(num_tests):
        prompt, output = problem.generate_prompt(size)
        if prompt is None or output is None:
            print("Generation test failed")
            return
        if verbose:
            print(f"TEST {test_num} - PROMPT: {prompt}")
            print(f"TEST {test_num} - OUTPUT: {output}")
        tests.append((prompt, output))
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        results = defaultdict(list)

        for sample in tests:
            prompt, output = sample
            args = (client, prompt, output, verbose)
            for i in range(num_prompts):
                future = executor.submit(evaluate_test, *args)
                futures.append(future)

        print("Evalutaing model...")
        if verbose:
            for future in as_completed(futures):
                result = future.result()
                correct += result
        else:
            for future in tqdm(as_completed(futures), total=len(futures)):
                result = future.result()
                correct += result
       
    total_prompts = num_tests * num_prompts
    if verbose:
        print(f"CORRECT: {correct}/{total_prompts}")
    return correct / total_prompts
    

import argparse

def main():
    parser = argparse.ArgumentParser(description="Evaluate model on a problem")
    parser.add_argument('path', type=str, help="Path to problem")
    parser.add_argument('model', type=ChatModel, help="Model gpt/gemini")
    parser.add_argument('size', type=int, help="Size of the input")
    parser.add_argument('--tests', '-t', type=int, help="Number of generated tests",  default=5)
    parser.add_argument('--prompts', '-p', type=int, help="Number of prompts for evert test case", default=5)
    parser.add_argument('--workers', '-w', type=int, help="Max number of workers",  default=5)
    parser.add_argument('--verbose', '-v', action='store_true', help="Print prompts and expected outputs")

    args = parser.parse_args()
    
    problem = Problem(args.path)
    client = get_chat(args.model)
    accuracy = eval_chat(problem, client, args.size, args.workers, args.tests, args.prompts, args.verbose)
    print(f"ACCURACY: {accuracy}")
   

if __name__ == "__main__":
    main()
