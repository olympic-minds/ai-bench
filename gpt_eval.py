from problem import Problem
import sys
import os
from dotenv import load_dotenv
import openai

def prompt_gpt(client, prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "What should @ANS be substituted for, for assert to evaluate true? Output only substitution for @ANS. Make sure to only print the substitution."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    gpt_response = response.choices[0].message.content
    gpt_response = gpt_response.replace(' ', '').replace('\n', '')
    gpt_response = gpt_response.removeprefix('```cpp').removeprefix('```cpp').removesuffix('```')
    return gpt_response
    

def main():
    if len(sys.argv) != 3:
        print("Usage: {} <path> <size>".format(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    size = int(sys.argv[2])
    
    
    problem = Problem(path)
    prompt, output = problem.generate_prompt(size)
    print(f"PROMPT: {prompt}")
    print(f"OUTPUT: {output}")
    if prompt is None or output is None:
        print("Generation test failed")
        return 1
    
    load_dotenv()
    OPENAI_KEY = os.getenv('OPENAI_KEY')
    client = openai.OpenAI(api_key=OPENAI_KEY)
    
    NUM_TESTS = 10
    CORRECT = 0
    for i in range(NUM_TESTS):
        gpt_response = prompt_gpt(client, prompt)
        print(f"RESPONSE {i}: {gpt_response}")
        CORRECT += int(gpt_response == output)
    
    print(f"CORRECT: {CORRECT}/{NUM_TESTS}")

if __name__ == "__main__":
    main()
