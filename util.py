import os
from typing import Callable, List


# iterates over files in input_dir.
# calls modify_content function on the content of the file, which returns list of modified contents
# calls modify_filename function on the filename of the file which returns the list of modified files,
# prints the new files (with updated content) to the second directory
def process_files(
    input_dir: str,
    output_dir: str,
    modify_content: Callable[[str], List[str]],
    modify_filename: Callable[[str], List[str]],
) -> None:

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        input_file_path = os.path.join(input_dir, filename)

        if os.path.isdir(input_file_path):
            continue

        with open(input_file_path, "r") as f:
            content = f.read()

        modified_content_list = modify_content(content)
        modified_filename_list = modify_filename(filename)

        assert len(modified_content_list) == len(modified_filename_list)

        for modified_filename, modified_content in zip(
            modified_filename_list, modified_content_list
        ):
            output_file_path = os.path.join(output_dir, modified_filename)
            with open(output_file_path, "w") as f:
                f.write(modified_content)


# makes an array, which has the original elements repeated `num_tests` times.
# for example [test1, test2, test3] num_tests = 2 -> [test1, test1, test2, test2, test3, test3]
def match_tests_to_prompts(tests, num_tests):
    return [test for test in tests for _ in range(num_tests)]


class TerminalColor:
    HEADER = "\033[36m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[32m"
    WARNING = "\033[93m"
    FAIL = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
