# %%
from ollama import chat, ChatResponse
import subprocess
import sys
import tempfile
import subprocess

arguments = ' '.join(sys.argv[1:])

def run_in_python(script_str):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as temp_file:
            # Write the script to the temporary file
            temp_file.write(script_str)
            temp_file.flush()  # Ensure all data is written
            
            # Execute the temporary script and capture stdout and stderr
            result = subprocess.run(
                ['python', temp_file.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        stdout = result.stdout.strip() or "None"
        stderr = result.stderr.strip() or "None"
        output = f"stdout: {stdout}; stderr: {stderr}"
    except Exception as e:
        output = f"execution error: {str(e)}."
        
    return output

def run_in_bash(script):
    try:
        # Run the Bash script using /bin/bash with the script passed via stdin
        result = subprocess.run(
            ['/bin/bash'],
            input=script,
            text=True,
            capture_output=True,
            check=True
        )

        # Extract stdout and stderr, defaulting to "None" if empty
        stdout = result.stdout.strip() or "None"
        stderr = result.stderr.strip() or "None"

        # Format the output string
        output = f"stdout: {stdout}; stderr: {stderr}"
    except Exception as e:
        output = f"execution error: {str(e)}."
        
    return output   

# task = 'count how many folders are there under the current folder.'
task = arguments
prompt = f"""
I want you to complete a task for me. You should break down the task step by step and perform the first step here.  

You have three response options:  

1. Write a Python script to execute. I will provide you with the output of the execution. If you choose this option, respond strictly in the format:  
   1: <python code> 
   and nothing else.  

2. Write a Bash script to execute. I will provide you with the terminal output. If you choose this option, respond strictly in the format:  
   2: <bash code>  
   and nothing else.  

3. Provide a final answer or confirm task completion. If you believe the task is finished, respond strictly in the format:  
   `3: <your answer>`  
   and nothing else.  
   **Note:** Returning code for execution does **not** count as completing the task. You must verify the results and explicitly confirm completion.  

### Important Rules:  
- **You should break down the task into logical steps** and execute them sequentially. Perform the first step in your response.  
- **I am only responsible for executing your code and providing related output.** It is your choice when to proceed to the next step.  
- **You are responsible for debugging your own code.** If the execution fails, I will provide error messages, but you must decide whether to fix the code or take a different approach.  
- **Do not include any additional explanations** when providing code for execution. Your response should only contain the formatted response as specified (1, 2, or 3).  
- **Execute one step per response.** Do not combine multiple actions in a single response. For example, do **not** respond with `1: <code>` and `2: <code>` in the same turn.  

### Example Interaction:  
Me: Create a folder under the parent directory with the name `48593 * 37533` followed by an 'a'.  
You: `1: print(48593 * 37533)`  
Me: `1823841069`  
You: `2: mkdir ../1823841069a`  
Me: (No output)  
You: `2: ls ..`  
Me: `index.html  microsoft-logo.png  static 1823841069a`  
You: `3: Finished.`  

### Hints:  
1. If you are unsure of your current directory, start by running `pwd` or `ls`.  
2. If your responses are repeatedly invalid, you may be adding unnecessary text. **Follow the response format exactly (1/2/3: <content>).**  
3. Only provide **one action per response.**  

This is your task:  
{task}  
"""


confirmation_prompt = f"You do not have to follow the formatting anymore. Using the results you have, give me your answer to my task. \n Task: {task}. Still, keep it short."
model='deepseek-r1:70b'

messages=[
    {
        'role': 'user',
        'content': prompt,
    }
]
response: ChatResponse = chat(
    model=model, 
    messages=messages
)
cnt = 0
while 1:
    messages.append(response.message)
    try:
        llm_response = response.message.content[response.message.content.index("</think>") + len("</think>"):].strip()
        print(cnt, llm_response)
        index = int(llm_response[0])    
        script = llm_response[2:].strip()
    except:
        index = -1
        output = "your response is invalid. If you are coding, do NOT explain your codes. Return the codes only." 
    # return condition
    if cnt > 10 and index == -1:
        print("Failed.")
        exit()
    if index == 3:
        print('Work done.')
        break
    elif index == 1:
        output = run_in_python(script) 
    elif index == 2:
        output = run_in_bash(script)

    messages.append(
        {
            'role': 'user',
            'content': output,
        },
    )
    response: ChatResponse = chat(
        model=model, 
        messages=messages
    )
    cnt += 1


messages.append(
    {
        'role': 'user',
        'content': confirmation_prompt,
    },
)

stream = chat(
    model=model, 
    messages=messages,
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
