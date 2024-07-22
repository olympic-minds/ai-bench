import os
import argparse
from tqdm import tqdm
from enum import Enum
from typing import Dict, List, Tuple
from problem import Problem
from chat import Chat
from gemini import Gemini
from chatgpt import ChatGPT
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
from util import process_files, match_tests_to_prompts
from print_results import print_results_for_problem


class ChatModel(Enum):
    GEMINI = "gemini"
    GEMINI_FLASH = "gemini-flash"
    GPT = "gpt"
    GPT4 = "gpt4"


class SystemPrompt(Enum):
    ONE_SHOT = "one_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"


SYSTEM_PROMPT = {
    SystemPrompt.ONE_SHOT: "What should @ANS be substituted for, for assert to evaluate true? The answer is an integer. Output only the substitution for @ANS - an integer.",
    SystemPrompt.CHAIN_OF_THOUGHT: "What value should replace @ANS for the assertion to evaluate to true? The answer is an integer. Start by writing down your thoughts and possibly simulate the program's execution. Remember, the final number you write will be the answer that should replace @ANS.",
}


def get_chat(
    chat_model: ChatModel,
    system_prompt: SystemPrompt,
):
    match chat_model:
        case ChatModel.GEMINI:
            return Gemini(system_prompt=SYSTEM_PROMPT[system_prompt])
        case ChatModel.GEMINI_FLASH:
            return Gemini(
                model="gemini-1.5-flash", system_prompt=SYSTEM_PROMPT[system_prompt]
            )
        case ChatModel.GPT:
            return ChatGPT(system_prompt=SYSTEM_PROMPT[system_prompt])
        case ChatModel.GPT4:
            return ChatGPT(
                model="gpt-4-turbo", system_prompt=SYSTEM_PROMPT[system_prompt]
            )


# evaluates the model. Returns problem_id, the number of successful answers and the total number of problems
def evaluate_test(
    problem_path: str,
    client: Chat,
    num_tests: int,
    executor: ThreadPoolExecutor | None = None,
    verbose: int = 0,
) -> tuple[str, int, int]:
    prompt_in_dir = f"{problem_path}/{Problem.dirs['prompt_in']}"
    model_out_dir = f"{problem_path}/{Problem.dirs['model_out']}"
    solution_out_dir = f"{problem_path}/{Problem.dirs['out']}"

    def fetch_model_response(prompt: str) -> List[str]:
        return client.prompt(prompt, completions=num_tests)

    def create_additional_files(filename: str) -> List[str]:
        name, ext = os.path.splitext(filename)
        return [f"{name}_{i}{ext}" for i in range(num_tests)]

    process_files(
        input_dir=prompt_in_dir,
        output_dir=model_out_dir,
        modify_content=fetch_model_response,
        modify_filename=create_additional_files,
    )

    model_outs = os.listdir(model_out_dir)
    solution_outs = os.listdir(solution_out_dir)

    if len(model_outs) != num_tests * len(solution_outs):
        raise Problem.IncorrectNumberOfFiles(model_out_dir, solution_out_dir)

    if verbose > 0:
        print_results_for_problem(problem_path, verbose > 1)

    return (
        problem_path,
        sum(
            1
            for model_out_filename, solution_out_filename in zip(
                sorted(model_outs),
                sorted(match_tests_to_prompts(solution_outs, num_tests)),
            )
            if Problem.compare_outputs(
                open(os.path.join(solution_out_dir, solution_out_filename), "r").read(),
                open(os.path.join(model_out_dir, model_out_filename), "r").read(),
            )
        ),
        len(model_outs),
    )


def eval_chat(
    problems: List[Problem],
    client: Chat,
    num_workers: int,
    num_tests: int,
    verbose: int = 0,
    precompiled_stdc: str | None = None,
) -> dict[str, float] | None:
    print("Generating tests...")
    for problem_num, problem in enumerate(problems):
        if not problem.generate_prompts(precompiled_stdc):
            print(f"Test generation failed for problem {problem.id}")
            return

    results: Dict[str, Tuple[int, int]] = {}
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []

        for problem in problems:
            future = executor.submit(
                evaluate_test, problem.id, client, num_tests, executor, verbose
            )
            futures.append(future)

        print("Evaluating model...")
        for future in tqdm(as_completed(futures), total=len(futures)):
            problem_id, score, total = future.result()
            results[problem_id] = (score, total)

    if verbose:
        for id, correct in results.items():
            print(f"PROBLEM {id} CORRECT: {correct[0]}/{correct[1]}")
        print("-" * 32)
    return {id: correct[0] / correct[1] for id, correct in results.items()}


def main():
    parser = argparse.ArgumentParser(description="Evaluate model on a problem")
    parser.add_argument(
        "path", type=str, help="Path to problem or directory of problems"
    )
    parser.add_argument(
        "model", type=ChatModel, help="Model gpt/gpt4/gemini/gemini-flash"
    )
    parser.add_argument(
        "--tests", "-t", type=int, help="Number of generated tests", default=5
    )
    parser.add_argument(
        "--workers", "-w", type=int, help="Max number of workers", default=5
    )
    parser.add_argument(
        "--precompiled_stdc",
        "-s",
        type=str,
        help="Path to precompiled bits/stdc++ header (without .gch)",
    )
    parser.add_argument(
        "--folder",
        "-f",
        action="store_true",
        help="Path is the path to problems directory",
    )
    parser.add_argument(
        "--chain_of_thought",
        "--cot",
        action="store_true",
        help="Use 'chain of thought' prompting method",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (repeatable: -v, -vv) - level 1 prints evaluation results with ins, level 2 and above prints prompts instead of ins",
    )

    args = parser.parse_args()

    problems = (
        Problem.read_problems_from_dir(args.path)
        if args.folder
        else [Problem(args.path)]
    )
    client = get_chat(
        args.model,
        (
            SystemPrompt.CHAIN_OF_THOUGHT
            if args.chain_of_thought
            else SystemPrompt.ONE_SHOT
        ),
    )
    results = eval_chat(
        problems, client, args.workers, args.tests, args.verbose, args.precompiled_stdc
    )
    if results is not None:
        for id, accuracy in results.items():
            print(f"PROBLEM {id} ACCURACY: {accuracy:.3f}")


if __name__ == "__main__":
    main()
