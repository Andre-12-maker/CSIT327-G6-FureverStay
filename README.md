# FureverStay: AirBNB for pets
FureverStay: Airbnb for pets is an online platform designed to connect pet owners with trusted pet sitters who can care for their pets while they are away. The platform provides secure bookings, sitter profiles, and reviews, ensuring peace of mind for owners and a reliable income stream for sitters.

# Tech stacks used:
- Django
- Python
- HTML/CSS
- Javascript
- Supabase

# Git Playground (Fork Workflow) — AY 2025

A hands-on lab to practice **basic Git** with a real **GitHub PR workflow**.  
You will **fork** this repo, work on a **feature branch**, and open a **Pull Request** (PR) back to this class repo’s `main`.

> ✅ This repo has automated checks (GitHub Actions). Your PR will **fail** if:
> - Your **branch** does not start with **your GitHub username** (e.g., `ericrev/feature-readme`)
> - **README** does not list your **name + @username** under **Contributors**
> - Your **bio** file is missing or does not include **@username**
> - No **conventional commit** message or **issue number** in commits

---

## Objectives
- Practice **fork → branch → commit → push → pull request**
- Use **conventional commit messages** and reference issues
- Resolve a simple **merge conflict**
- Identify yourself clearly using your **GitHub username**

## Rules
- **Branch naming (required):** `your-github-username/feature-…`
- **Commit style:** Conventional Commits (e.g., `feat: …`, `docs: …`) and reference an issue `(#1)` or `(#2)`
- **Do not** push directly to `main`. Use a PR and request review.
- **Files to modify/add:** `README.md` (Contributors) and `students/<lastname>-bio.md`

## Prerequisites
- Git installed; GitHub account
- Perform **Task A**
- Configure your identity (once):
  ```bash
  git config --lobal user.name  "Your Name"
  git config --lobal user.email "your_email@example.com"
  ```

---

## Tasks (follow in order)

### A) Fork & clone
1. Click **Fork** (top-right) to create a copy under your GitHub account.
2. Clone **your fork** and inspect remotes:
   ```bash
   git clone <URL-of-your-fork>
   cd git-playground-AY2025
   git remote -v
   ```
   *(Optional but useful):*
   ```bash
   git remote add upstream <URL-of-class-repo>
   ```

### B) Create a branch (must start with your GitHub username)
```bash
git branch <your-github-username>/<branch-name>
```
Example: `ericrev/feature-readme`

### C) Improve README (Issue #1)
Add **your real name + @username** under **Contributors** (see assigned contributors file):
```
- Lastname, Firstname (**@your-github-username**)
```
Example:
```
- Doe, John (**@johndoe123**)
```
Commit:
```bash
git add README.md
git commit -m "docs(readme): add Doe to contributors (#1)"
```

### D) Push & open a Pull Request
```bash
git push -u origin <your-username>/feature-readme
```
Then open a **Pull Request** to **this class repo**’s `main`:
- **Title:** `feat: update README – Lastname, Firstname`
- **Description:** Mention **Issue #1** and describe your changes

### E) Add your bio (Issue #2)
Create `students/<lastname>-bio.md` with the following bullets (include your **@username**):
```markdown
- Program: e.g., BSIT
- Year: e.g., 3rd Year
- Section: e.g., G1
- Favorite Language: e.g., Java
- One Git Tip Learned: e.g., Use `git status` often
- GitHub: @blissfuljuan
```
Commit and push:
```bash
git add students/<lastname>-bio.md
git commit -m "feat(bio): add <lastname> student bio (#2)"
git push
```

### F) Sync and resolve conflicts (if any)
If your PR shows conflicts:
```bash
git fetch origin
git merge origin/main
# (Or if you set upstream earlier)
# git fetch upstream
# git merge upstream/main
# Resolve conflict markers in README.md, keep both your contributor line and class updates
git add README.md
git commit -m "fix: resolve README merge conflict"
git push
```

### G) Finalize
- Address any review comments
- When approved, **Squash merge** your PR

*(Optional bonus)*
```bash
git tag v0.1.<your-initials>
git push --tags
git restore README.md   # demo undo
```

---

## Commit Message Guide (Conventional Commits)
- **feat:** new feature — `feat(bio): add Doe student bio (#2)`
- **fix:** bug fix — `fix: resolve README merge conflict`
- **docs:** docs only — `docs(readme): add Doe to contributors (#1)`
- Others: `chore`, `refactor`, `test`, `style`, `perf`

Include an **issue number** in at least one commit: `(#1)` or `(#2)`.

---

## Cheatsheet
```bash
git status
git log --oneline --graph --decorate
git switch -c <branch>        # create/switch branch
git add <file>
git commit -m "type(scope): message (#issue)"
git push -u origin <branch>
git fetch origin && git merge origin/main
```

---

## Troubleshooting
- **Permission denied on push:** You’re pushing to the class repo. Ensure `origin` points to **your fork**.
- **Checks failing (branch name):** Rename branch to start with your **GitHub username**.
- **Checks failing (username missing):** Ensure `@your-username` appears in both **README (Contributors)** and your **bio** file.
- **No issue reference:** Amend/add a new commit including `(#1)` or `(#2)`.

---

# Team members:
- Clint Pacaña (clint.pacana@cit.edu) - Lead Developer
- Ritter Padin (ritter.padin@cit.edu) - Frontend Developer
- Andre Policios (andre.policios@cit.edu) - Backend Developer

# Deployed Links
TBA


