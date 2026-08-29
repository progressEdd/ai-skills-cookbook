# Navigating the harness
> The `@` references files precisely, and the `/` invoke commands without leaving the chat.

## Learning objectives
- [ ] Explore how to reference files in your harness
- [ ] Understand how agents will handle .gitignore
- [ ] invoke a `/` command

Each concept below ends with a **Your turn** — run it before moving on, and by the time you reach the end of this lesson every box will be checked.

## Concepts

> **Back to the kitchen:** `@`-referencing a file is placing one specific ingredient on the counter; letting the agent explore a folder is handing it the pantry keys. `/` commands are standardized order chits — write once, invoke every shift.

### Why mention the file
When we reference a file, our agent can just read the file instead of looking for it. Let's observe what happens when we just use the prompt 
> tell me the License


Your Agent might have an output of
<blockquote>
$ ls ~/Documents/development_projects/progressEdd_projects/ai-skills-cookbook/ | grep -i -E "license|copying" ; grep -i -m 5 "license"                                   
 ~/Documents/development_projects/progressEdd_projects/ai-skills-cookbook/README.md 2>/dev/null                                                                           
                                                                                                                                                                          
 LICENSE                                                                                                                                                                  
                                                                                                                                                                          
                                                                                                                                                                          
 Command exited with code 1                                                                                                                                               

 Took 0.0s   

---
 read ~/Documents/development_projects/progressEdd_projects/ai-skills-cookbook/LICENSE                                                                                    

---
This repository is licensed under the GNU General Public License, Version 2 (GPL-2.0), June 1991 — see the LICENSE file in the project root.                             
                                                                                                                                                                          
 Key points:                                                                                                                                                              
 - Free to use, copy, modify, and redistribute, provided the license and copyright notices are preserved                                                                  
 - Derivative works must also be distributed under GPL-2.0 (copyleft)                                                                                                     
 - No warranty — the software is provided "as is"                                                                                                                         
 - The LICENSE file itself contains the standard "or, at your option, any later version" language only in the template appendix; no specific copyright holder is named in 
   the file                                                                                                                                                               
                                                                                                                                                                          
 The full text is in ~/Documents/development_projects/progressEdd_projects/ai-skills-cookbook/LICENSE.  
</blockquote>

**Your turn**
- [ ] Run the prompt `tell me what the License is`

### Referencing files in your harness
By default, the `@`, will look for child files within a given directory. Let's compare this to if we `@` the Licnse file in the repo's root.
1. Start a new session in your project directory
2. Use the `@` and search for `LICENSE`, pick the root `LICENSE` your first prompt should look like this:
    - >  tell me what the @LICENSE is
    - Your agent should have a response of
      - <blockquote> 
        read LICENSE   
        
        --- 
        
        The LICENSE file is the GNU General Public License, Version 2 (GPL-2.0), June 1991.                                                                                      
                                                                                                                                                                          
        In short, this means the project is licensed as copyleft free software:                                                                                                                                                                                                                                                                            
           - Freedom to use, study, modify, and redistribute — anyone can copy, distribute, and change the software                                                                 
           - Copyleft requirement — derivative works must also be distributed under the GPL-2.0 terms (Section 2b)                                                                  
           - Source code required — if you distribute binaries, you must provide or offer the corresponding source code (Section 3)                                                 
           - No warranty — the software is provided "as is" with no warranty, and the authors aren't liable for damages (Sections 11–12)                                            
           - No later-version clause specified — the license doesn't include the "or any later version" wording, so it's strictly GPL-2.0-only unless stated otherwise elsewhere 
                    
        </blockquote>

**Your turn**
- [ ] Use the `@` in a session and find the repo's root license
- [ ] Enter the prompt `tell me what the @LICENSE is`

In the second example, the agent read the file directly rather than search for it using `ls` in the first example. If you want the agent to modify a specific file, it's better to mention it so that you don't have to wait for your agent to search for it. As of the writing of this guide, it is better to be explicit with your agent as it is faster to have it read the file directly rather than wait for it to find and open it. 

If the `@` search doesn't work, you can always provide the full file path for the agent to read. This can be handy for files outside your directory. Some editors and terminals might support dragging the file from the file explorer.

### How agents respond to .gitignore
By default, many harnesses will ignore files/directories referenced in the .gitignore. It's great when you don't want your agent to read secrets (environment keys, passwords, etc.). In the case of our course worktrees folder, we have a gitignore rule in [root .gitignore](../../.gitignore), that ignores the files within the `02-worktrees` folder
```.gitignore
# Git worktrees (ignore all worktree contents but keep the directory)
02-worktrees/*
```
This makes it so that our individual worktree branches don't get committed to our branch. In my case I don't want the `progressEdd` branch to include all the worktrees, because they are tracked individually

## Checkpoint
Every exercise above sits right next to the concept that taught it — if all boxes are checked, you're ready for [03-project-instructions.md](03-project-instructions.md). Commit your progress:
```
git add -A
git commit -m "02 navigating the harness complete"
```

## Further reading
<!-- TODO -->
