## BRO!!!

This is a simple script to make an llm your partner.

#### Prerequisite:
1. Install ollama
   ```
   python -m pip install ollama
   apt-get install ollama
   ollama run deepseek-r1:70b // you can use any llms, just don't forget to change the model version in llm.py
   ```
2. Quit ollama. Give llm a name.
   ```
   // in ~/.bashrc
   alias bro="python <your path to llm.py>"
   ```
3. Use your bro
   ```
   >>> bro say hi
   0 1: print("hi")
   1 3: Task completed. The output was 'hi'.
   Work done.
   <think>
   Okay, so the user has changed their instructions now. They initially asked me to perform a task by breaking it down into steps and executing code, but after I confirmed that "hi" was outputted, they told me not to follow the formatting anymore and to provide my answer directly.
    
   Given this change, I need to respond simply with "hi." There's no need for any code or multiple steps now. They just want a short answer to their task of saying hi.
   </think>
    
   Hi!

   >>> bro how many folders are there in the current directory
   0 1: ls -d .*/
   1 2: ls -d */ | wc -l
   2 2: find . -maxdepth 1 -type d | wc -l
   3 3: There are 23 folders in the current directory.
   Work done.
   <think>
   Alright, so let's figure out how many folders are in the current directory step by step.
    
   First, I remember that using `ls` command can list files and directories, but we only want folders. The initial attempt was to use `ls -d */ | wc -l`, which gave an output of 9. However, this might not include hidden directories because they don't end with a slash.
    
   To ensure accuracy, I need to account for both regular and hidden directories. Hidden directories start with a dot (.), so we should include those in our count.
    
   A better approach is to use the `find` command, which can search for directories explicitly. Using `find . -maxdepth 1 -type d | wc -l`, where:
   - `.` specifies the current directory,
   - `-maxdepth 1` ensures we only look at the current level (not subdirectories),
   - `-type d` tells `find` to only consider directories.
    
   Running this command, I get an output of 23. This means there are 23 folders in the current directory, including both regular and hidden ones.
    
   So, after considering all possibilities and ensuring no directories are missed, the final count is 23.
   </think>
    
   There are **23** folders in the current directory.
   ```
