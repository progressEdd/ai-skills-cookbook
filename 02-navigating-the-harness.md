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
null                                                                                                                                                             

 LICENSE


 Command exited with code 1                                                                                                                                               

 Took 0.0s   

---
 read ~/Documents/development_projects/progressEdd_projects/ai-skills-cookbook/LICENSE                                                                                    

---
 This repo is licensed under the GNU General Public License v2.0 (GPL-2.0), June 1991.                                                                                                          
                                                                                                                                                                                                
 There are two copies of the license in the project:                                                                                                                                            
 - ~/LICENSE — the root license file                                                                                                                                                            
 - 01-dev-onboarding/LICENSE — a duplicate for the dev-onboarding section                                                                                                                       
                                                                                                                                                                                                
 GPL-2.0 is a copyleft license: you're free to use, modify, and distribute the software (including commercially), but any distributed derivatives must also be released under GPL-2.0 with      
 source code provided. 
</blockquote>

**Your turn**
- [ ] Run the prompt `tell me what the License is`

### Referencing files in your harness
By default, the `@`, will look for child files within a given directory. Let's compare this to if we `@` the Licnse file in the repo's root.
1. Start a new session in your project directory
2. Use the `@` and search for `LICENSE`, pick the root `LICENSE` your first prompt should look like this:
    - <blockquote>>
      The LICENSE file is the GNU General Public License, Version 2 (GPL-2.0), June 1991.

      In short, this means the project is licensed as copyleft free software:

      - Freedom to use, study, modify, and redistribute --- anyone can copy, distribute, and change the software
      - Copyleft requirement --- derivative works must also be distributed under the GPL-2.0 terms (Section 2b)
      - Source code required --- if you distribute binaries, you must provide or offer the corresponding source code (Section 3)
      - No warranty --- the software is provided "as is" with no warranty, and the authors aren't liable for damages (Sections 11--12)
      - No later-version clause specified --- the license doesn't include the "or any later version" wording, so it's strictly GPL-2.0-only unless stated otherwise elsewhere
    </blockquote 


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

### The slash (`/`) command
The slash command `/` in many harnesses lets you access your settings and skills. A universal command is `/model`, which lets you change your model. As we get to later modules, you'll start using the `/` for skills. For now let's just run `/model` and review the output. In pi, you should see a output that looks like this
```

Only showing models from configured providers. Use /login to add providers.                                                                                                                     

>

→ glm-5.2 [zai] · default ✓
  gpt-5.3-codex-spark [openai-codex]
  gpt-5.4 [openai-codex]
  gpt-5.4-mini [openai-codex]
  gpt-5.5 [openai-codex]
  gpt-5.6-luna [openai-codex]
  gpt-5.6-sol [openai-codex]
  gpt-5.6-terra [openai-codex]
  glm-4.7 [zai]
  glm-5-turbo [zai]
  (1/15)

  Model Name: GLM-5.2

  Model catalogs refreshed.
```

**Your turn**
- [ ] Use the `/` in a session and find which model is selected
- My model is: `$MODEL_NAME` — if it's set to auto, just write `auto`

Paste your `/model` output below — the model list in the example above will date quickly, but your own paste stays accurate for you:
```
# Paste your /model output here
```

## Checkpoint
Every exercise above sits right next to the concept that taught it — if all boxes are checked, you're ready for [03-project-instructions.md](03-project-instructions.md). Commit your progress:
```
  git add -A
  git commit -m "02 navigating the harness complete"
```

## Further reading
[pi slash commands](https://pi.dev/docs/latest/usage#slash-commands)
[cursor slash commands](https://cursor.com/docs/cli/reference/slash-commands)
[claude code commands](https://code.claude.com/docs/en/commands#)
