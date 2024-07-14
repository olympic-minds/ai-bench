import os
from typing import Callable


# iterates over files in input_dir.
# applies modify_content function to the content of the file
# applies modify_filename function to the filename of the file,
# prints the new files (with updated content) to the second directory
def process_files(input_dir: str, 
                  output_dir: str, 
                  modify_content: Callable[[str], str], 
                  modify_filename: Callable[[str], str]) -> None:

    os.makedirs(output_dir, exist_ok = True)
    
    for filename in os.listdir(input_dir):
        input_file_path = os.path.join(input_dir, filename)
        
        if os.path.isdir(input_file_path):
            continue
        
        with open(input_file_path, 'r') as f:
            content = f.read()
        
        modified_content = modify_content(content)
        modified_filename = modify_filename(filename)
        
        output_file_path = os.path.join(output_dir, modified_filename)
        with open(output_file_path, 'w') as f:
            f.write(modified_content)
        