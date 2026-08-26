# Git crash course
> Git is your undo button when an agent goes sideways. Commit fearlessly, revert easily. 

## Learning objectives
- [ ] Explain what version control is and why it matters more, not less, when an agent edits your code
- [ ] Run the common workflow: `status` → `add` → `commit` → `push` / `pull`
- [ ] Create branches to isolate agent work
- [ ] Read a diff and revert a change (file, commit, or branch) after a bad agent edit
- [ ] Bring another branch's changes into yours with `git rebase` (and know when to prefer it over merge)
- [ ] Describe what a worktree is and when parallel agent sessions want one

Every exercise below sits right after the concept that teaches it — run each command as you read, and by the end of the lesson every box will be checked (and you'll be working inside your own `my-course` worktree). I recommend typing the commands manually, so you get familiar with the commands especially if this is your first time learning git. If you are already familiar, you can instruct your AI agent to create worktrees and branches instead.

## Concepts

### Why git matters more with agents
Git is a version control system: it tracks every change to your files, keeps a full history, and lets you return to any earlier state. Sites like [GitHub](https://github.com/) and [GitLab](https://about.gitlab.com/) host git repositories and add collaboration on top.

If you're new to agents, it's tempting to think the agent makes git *less* important — it writes the code, after all. The opposite is true:

- **Agents edit fast.** What used to be ten minutes of typing is now ten seconds of changes. Commits become checkpoints between agent runs.
- **You review, the agent authors.** Reading a `git diff` before committing is how you catch a confident-sounding agent's mistakes.
- **Mistakes are cheap to undo.** A bad agent edit is a `git restore`, not a lost afternoon. That safety is what lets you say "try it" without fear.

### The common workflow
Before running any of this, [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

And before running *any* terminal command, know where you are. Every terminal has a **current working directory (cwd)** — the folder commands operate on. It's also what an agent sees when you launch it, so it's the first thing to check when something "runs in the wrong place."

| Action | macOS / Linux | Windows (cmd / PowerShell) |
|---|---|---|
| Print working directory (see where you are) | `pwd` | `cd` (cmd) / `pwd` (PowerShell) |
| Change directory | `cd <path>` | `cd <path>` |
| Go up one folder | `cd ..` | `cd ..` |
| Go to your home folder | `cd ~` | `cd %USERPROFILE%` (cmd) / `cd ~` (PowerShell) |

(Yes, bare `cd` in cmd on windows really does print the current directory — run `cd /?` to see it documented.)

`cd` is the same everywhere; only the "where am I" and "home" spellings differ. Home-folder shorthand like `~/Documents` is understood by macOS/Linux shells and PowerShell, but not cmd — spell out `C:\Users\<you>\Documents` there (or use forward slashes, which git accepts).

The `<path>` can be a single folder or several at once — `cd 02-worktrees` moves one level, while `cd 02-worktrees/progressedd` jumps multiple levels in one go (each segment relative to where you are now). You can also use an absolute path that starts from the root of the drive/filesystem, like `cd C:\Users\<you>\projects` or `cd /home/<you>/projects` — those work no matter where you currently are.

**Your turn**
- [ ] Run `pwd` (or `cd` in cmd) to see where you are, `cd` into the repo folder if you're not there yet, then confirm with `pwd` again

1. **Clone an existing repo**
    ```
    git clone https://github.com/progressEdd/ai-skills-cookbook.git
    ```
    - Replace the URL with the `HTTPS` or `SSH` address shown in the repo's *Code* tab
    - `git clone` creates a new subfolder named after the repo *inside your current directory* — so first `cd` to where you keep your projects (e.g. `~/Documents` or `~/Desktop`), then clone
    - Then move into the repo folder it created: `cd $repo-folder` (here, `cd ai-skills-cookbook`)

    **Your turn**
    - [ ] If you haven't cloned yet: `cd` into the folder where you want the repo to live (e.g. `Documents`), run the command above, then `cd ai-skills-cookbook` into it — if you already cloned by following the root README, check the box and move on
    - [ ] Run `git log --oneline` in this repo and skim the output — every line is a checkpoint someone can return to; that's the safety net agents make you want
2. **Check out a branch**
    - `git branch` lists your local branches (`git branch -a` includes remote ones like `course` and `starter-skills`); `git checkout $branch` switches to one
    - Rather than committing straight to `master`, branch off an existing branch to create your own working branch. Use `starter-skills` — a branch off `master` that adds the starter `.agents/skills/` kit (`master` itself stays clean of it):
        ```
        git checkout -b $my-branch origin/starter-skills
        ```
    - (`origin/starter-skills` is your clone's copy of the remote branch — cloning doesn't create a local `starter-skills`, and branching off the `origin/` copy works the same)
    - For an example, see the [`progressedd` branch](https://github.com/progressEdd/ai-skills-cookbook/tree/progressedd) on GitHub — a working branch created off `master` just like this
    - This branch is yours — you'll practice the workflow below on it, then stack your course work on top of it with a rebase later in this lesson

    **Your turn**
    - [ ] Run `git branch -a` to list the branches, then create your own working branch: `git checkout -b $my-branch origin/starter-skills` (replace `$my-branch` with a name you'll recognize)
3. **Make modifications** — you, or an agent on your behalf

    **Your turn**
    - [ ] Make a small change on your branch (fix a typo, add a note) and run `git status` — your file should show up as modified
4. **Commit changes.** Commit whenever you've made progress or before you test something risky; if it breaks, you'll know which change caused it.
    1. `git status` — see which files have been modified
    2. `git add $file-name` — stage a specific file, or `git add -A` for all changes
        - **Git and paths:** git works from any folder inside the repo (it finds the root by walking up to `.git`), but `git add` interprets `$file-name` relative to *where you are*, not the repo root. From `02-worktrees/my-course/01-lessons/`, `git add 01-lessons/foo.md` fails — it's `git add foo.md` (or `git add :/01-lessons/foo.md` to spell it from the root). `git status` shows paths relative to your location too (`../` = up a level)
        - `git add -A` is the exception: it stages the entire repo no matter where you are
        - Simplest habit while learning: run git commands from the repo root, so "where I am" and "the repo root" are the same thing
        - Run `git help add` (quit with `q`) for examples of staging subsets of files
    3. `git commit -m "added new feature to function a"` — the quotes let the message contain spaces; write messages your future self will understand

    **Your turn**
    - [ ] Review your change with `git diff` first — you'll read diffs constantly when reviewing agent edits
    - [ ] Stage the file with `git add $file-name`, confirm with `git status` that it's staged, then commit with a message your future self will understand
5. **Push local changes to the remote**
    ```
    git push origin $branch-name
    ```
    - `origin` is shorthand for the remote repo you cloned from; note that many repos restrict pushing directly to `master`/`main`

    **Your turn**
    - [ ] Push your branch with `git push origin $my-branch`, then find it on GitHub — your commits now live on the remote too
6. **Open a pull request** — after pushing, GitHub/GitLab will prompt you with a link (or use the *Pull requests* tab → *Compare & pull request*). Some organizations require a review before merge

    **Your turn**
    - [ ] Open the pull-request link GitHub shows for your branch and read the diff it presents — you don't have to merge anything, just see how a review reads
7. **Merge changes from the remote**
    - `git status` first — commit or stash any local changes (`git stash` caches them; `git stash apply` brings them back)
    - `git pull` fetches and merges remote changes into your current branch (`git fetch` only downloads them, if you'd rather `merge` manually)

    **Your turn**
    - [ ] Run `git pull` on your branch — right after a push, "Already up to date." is exactly what you want to see

### Undoing things
The undo toolbox, ordered safest first:

- `git restore $file` — discard uncommitted changes to a file; the file returns to its last committed state
- `git restore --staged $file` — unstage a file (keeps the edits, pulls it out of the next commit)
- `git revert $commit` — create a *new* commit that undoes an old one; safe on shared branches because history is preserved
- `git reset` — move the branch pointer back; `--soft` keeps changes staged, `--hard` throws them away. Powerful and destructive — read twice, run once

Rule of thumb for agent work: commit *before* letting the agent try something ambitious. Then a bad outcome is one `git restore` or `git reset --hard` away from gone.

**Your turn**
- [ ] Deliberately break a file (delete a line, paste in junk), inspect the damage with `git diff`, then discard it with `git restore $file`
- [ ] Stage a change with `git add`, then pull it back out with `git restore --staged $file` — the edits stay, only the staging goes

### Working with worktrees
When you need multiple branches checked out at the same time, `git worktree` gives each one its own working directory, all sharing the same repository history. Instead of stashing changes and switching branches, you can keep a feature branch open in one editor while hotfixing `main` in another — or run two agent sessions in parallel without them stepping on each other. (This course itself lives in a worktree.)

Run these commands from the repo root — if you're inside a subfolder, `cd` back to it first (`pwd` shows where you are).

1. **Create a worktree.** A common convention is a dedicated folder at the repo root
    - For an existing branch:
        ```
        git worktree add $worktree-dir/$branch-name $branch-name
        ```
    - For a new branch (like `checkout -b`), optionally based on a different branch:
        ```
        git worktree add $worktree-dir/$new-branch -b $new-branch [$source-branch]
        ```
2. **List worktrees:** `git worktree list` shows every working directory attached to the repo
3. **Work inside it** — open the worktree folder in your editor; commits, pushes, and pulls all work the same
4. **Clean up:** `git worktree remove $worktree-dir/$branch-name` once the work is committed and merged

    **Your turn**
    - [ ] Practice the full cycle with a throwaway worktree: create one (`git worktree add 02-worktrees/practice -b practice`), make a commit inside it, confirm it shows up in `git worktree list`, then remove it with `git worktree remove 02-worktrees/practice` (add `--force` if you left uncommitted changes behind)

**Your turn, for real:** create the worktree you'll use for the rest of the course — your own branch off `course`, where you'll mark every lesson's checkboxes and commit your progress:
```
git worktree add 02-worktrees/my-course -b my-course course
```
Then `cd` into it and open it in your editor — this is where you'll work from now on:
```
cd 02-worktrees/my-course
```

- [ ] Create your `my-course` worktree and open `02-worktrees/my-course/` in your editor — the rest of the course happens inside it
- [ ] Inside the worktree, commit the screenshot you saved in [00-start-here.md](00-start-here.md): `git add` the image, then `git commit` — your first progress commit

Each marked checkbox becomes a commit — your progress doubles as git practice — and `course` stays clean so it can receive future content updates.

Things to keep in mind:
- Each worktree has its own working directory but they share the same git history
- Worktree directories aren't tracked in git — a shared worktrees folder usually keeps only a `README.md` describing its conventions
- The same branch can't be checked out in two worktrees at once

### Bringing in another branch's changes with rebase
Your `my-course` branch started from `course` — it has the lessons, but not the rest of the repo. Your `$my-branch` — your branch off `master` via `starter-skills` — has `master`'s supporting files (the harnesses the later lessons study), the starter `.agents/skills/` kit, and the practice commits you made above. You want both worlds in one clean history.

Git has two tools for combining branches:
- `git merge $branch` — combines both histories and adds a merge commit. The right call on shared branches like `master`
- `git rebase $branch` — replays *your* commits on top of `$branch`'s tip, as if you'd started your work from there. Linear history, no merge commit — the right call for your own working branch

From inside your `my-course` worktree, rebase onto your own branch:
```
git rebase $my-branch
```
(Branches are shared across worktrees — `my-course` can see `$my-branch` even though it's checked out in your main checkout — so no `cd`-ing back and forth.)

Git takes every commit `my-course` has that `$my-branch` doesn't — the course content and your progress commits — and replays them on top of your branch's tip. Verify:
```
ls .agents/skills/
git log --oneline -5
```
The skill kit is there, and your commits sit at the top of a single straight line of history. You'll also notice `master`'s supporting-file folders arrived — if the `00-supporting-files/harnesses/` folders look empty, populate them once with `git submodule update --init`.

**If both branches changed the same file** (say, `README.md`), the rebase pauses mid-way and `git status` shows the conflict:
1. Open the file and edit it to the version you want (for a README conflict, keep the course version — it's your lesson hub)
2. `git add $file`
3. `git rebase --continue` — git moves on to the next commit

Changed your mind mid-rebase? `git rebase --abort` puts the branch back exactly where it was.

One golden rule: **rebase only branches that are yours.** Replaying commits rewrites history, so never rebase a branch others build on (`master`, shared features) — that breaks everyone else's clones.

**Your turn**
- [ ] Inside `my-course`, run the rebase onto your `$my-branch`, then verify with `ls .agents/skills/` and a linear `git log --oneline` — your course work now sits on top of your own branch of `master`

## Checkpoint
Every exercise above sits right next to the concept that taught it. If all boxes are checked, this lesson is complete: you ran the whole workflow (`status` → `add` → `commit` → `push` → `pull`), undid a bad change, practiced worktrees, rebased your course work onto your own branch of `master`, and you're now working inside `my-course` with the skill kit in place. From here on, mark each lesson's checkboxes and commit as you go.

## Terminology
- `clone`: download a repository
- `checkout`: switch to a specific branch
- `branch`: a particular version line of the repository
- `add` / `stage`: mark changes to include in the next commit (the staging area is where that snapshot is prepared)
- `commit`: save a snapshot of the staged changes
- `commit message`: the description attached to a commit
- `push`: upload local commits to the remote
- `pull`: fetch and merge remote changes into your local branch
- `fetch`: download remote changes without merging
- `merge`: combine commits from different branches into one history
- `rebase`: move a sequence of commits onto a new base commit
- `worktree`: an extra working directory attached to the same repository
- `stash`: temporarily save changes you don't want to commit yet
- `status`: show the state of the working directory and staging area
- `diff`: show differences between commits, the working tree, etc.
- `log`: show commit history
- `remote` / `origin`: the shared repository / the default name for the one you cloned from
- `HEAD`: a reference to the last commit on the checked-out branch
- `conflict`: overlapping changes on different branches that must be resolved manually
- `pull request (PR)`: a request to merge your branch, usually with review
- `fork`: your own copy of someone else's project

## Further reading
- [Intro to git](https://github.com/progressEdd/dev-onboarding) (dev-onboarding guide, with screenshots)
- [Pro Git book](https://git-scm.com/book/en/v2)
