# Git & GitHub CLI Cheat Sheet

## 🚀 GitHub Flow Model - Quick Reference

This cheat sheet follows the **GitHub Flow** model with **squash and merge** strategy for clean commit history.

### 📋 Core Principles
- `main` branch is always deployable
- Create feature/fix branches from `main`
- Use descriptive branch names
- Squash and merge PRs for clean history
- Delete branches after merging

---

## 🔧 Essential Git Commands

### 🎯 Daily Workflow

#### Start New Feature/Fix
```bash
# Switch to main and pull latest changes
git checkout main
git pull origin main

# Create new branch (use descriptive names)
git checkout -b feature/invoice-extraction
git checkout -b fix/pdf-parsing-error
git checkout -b docs/update-readme
```

#### Work on Changes
```bash
# Stage specific files
git add filename.py
git add .  # Stage all changes

# Commit with descriptive message
git commit -m "feat: add invoice data extraction logic"
git commit -m "fix: resolve PDF parsing error for corrupted files"
git commit -m "docs: update quick start guide"
```

#### Push Changes
```bash
# Push branch to remote (first time)
git push -u origin feature/invoice-extraction

# Push subsequent commits
git push
```

### 🔄 Keeping Branch Updated
```bash
# Fetch latest changes from main
git fetch origin main

# Merge main into your branch (if needed)
git merge origin/main

# Alternative: Rebase for cleaner history
git rebase origin/main
```

### 🧹 Cleanup
```bash
# Delete local branch after merge
git branch -d feature/invoice-extraction

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/invoice-extraction

# Prune deleted remote branches
git remote prune origin
```

---

## 🐙 GitHub CLI Commands

### 📥 Installation
```bash
# Install GitHub CLI
brew install gh  # macOS
# or visit: https://cli.github.com/

# Authenticate
gh auth login
```

### 🔀 Pull Request Workflow

#### Create PR
```bash
# Create PR from current branch
gh pr create --title "Add invoice extraction feature" --body "Implements core invoice data extraction using PyZerox"

# Create PR with template
gh pr create --title "Fix PDF parsing error" --body-file .github/pull_request_template.md

# Create draft PR
gh pr create --draft --title "WIP: Add batch processing"
```

#### Manage PRs
```bash
# List PRs
gh pr list
gh pr list --state open
gh pr list --author @me

# View PR details
gh pr view 123
gh pr view --web  # Open in browser

# Checkout PR locally
gh pr checkout 123
```

#### Review Process
```bash
# Request review
gh pr edit 123 --add-reviewer username

# Add labels
gh pr edit 123 --add-label "enhancement,documentation"

# Mark ready for review (from draft)
gh pr ready 123
```

#### Merge PR (Squash and Merge)
```bash
# Squash and merge (preferred)
gh pr merge 123 --squash --delete-branch

# Merge with custom commit message
gh pr merge 123 --squash --delete-branch --subject "feat: add invoice extraction" --body "Implements core extraction logic"
```

---

## 📝 Commit Message Conventions

### Format
```
type(scope): brief description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
git commit -m "feat: add PDF invoice parsing"
git commit -m "fix: resolve memory leak in batch processing"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify error handling logic"
```

---

## 🌟 Branch Naming Conventions

### Patterns
```bash
feature/description-of-feature
fix/description-of-fix
docs/description-of-docs
refactor/description-of-refactor
test/description-of-test
```

### Examples
```bash
feature/add-claude-support
fix/pdf-memory-leak
docs/setup-instructions
refactor/extract-validation-logic
test/add-integration-tests
```

---

## 🚨 Common Scenarios

### 🔧 Fix Mistakes

#### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

#### Undo Last Commit (Discard Changes)
```bash
git reset --hard HEAD~1
```

#### Amend Last Commit
```bash
git commit --amend -m "New commit message"
```

### 🔄 Sync with Main

#### Your Branch is Behind Main
```bash
git checkout main
git pull origin main
git checkout your-branch
git merge main
```

#### Resolve Merge Conflicts
```bash
# After merge conflicts appear
git status  # See conflicted files
# Edit files to resolve conflicts
git add .
git commit
```

### 📦 Stash Changes
```bash
# Save work in progress
git stash

# Apply stashed changes
git stash pop

# List stashes
git stash list
```

---

## 🎯 Quick Actions

### 🔍 Status & Info
```bash
git status                    # Check working directory
git log --oneline -10        # Last 10 commits
git branch -a                # All branches
gh repo view --web           # Open repo in browser
```

### 🚀 Fast Track
```bash
# Complete feature workflow
git checkout main && git pull && git checkout -b feature/new-feature
# ... make changes ...
git add . && git commit -m "feat: implement new feature"
git push -u origin feature/new-feature
gh pr create --title "Add new feature" --body "Description"
```

### 🧹 Cleanup
```bash
# Delete merged branches
git branch --merged main | grep -v "main" | xargs -n 1 git branch -d

# Reset to clean state
git checkout main && git pull && git branch -D old-branch
```

---

## ⚡ Copy-paste Git Aliases

Add the following to your `~/.gitconfig` for faster Git commands:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
    graph = log --graph --oneline --decorate --all
    pushf = push --force-with-lease
```

---

## 🔗 Useful Aliases

Add to your `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
    graph = log --graph --oneline --decorate --all
    pushf = push --force-with-lease
```

---

## 📚 Quick Reference Card

| Action | Git Command | GitHub CLI |
|--------|-------------|------------|
| New branch | `git checkout -b feature/name` | - |
| Create PR | - | `gh pr create` |
| Merge PR | - | `gh pr merge --squash --delete-branch` |
| View PRs | - | `gh pr list` |
| Switch branch | `git checkout branch-name` | `gh pr checkout 123` |
| Push changes | `git push` | - |
| Pull changes | `git pull` | - |
| Check status | `git status` | `gh pr status` |

---

## 🎯 Best Practices

1. **Always start from main**: `git checkout main && git pull`
2. **Use descriptive branch names**: `feature/add-invoice-parsing`
3. **Write clear commit messages**: Follow conventional commits
4. **Keep PRs small**: Easier to review and merge
5. **Squash and merge**: Clean commit history on main
6. **Delete branches**: After merging to keep repo clean
7. **Review before merge**: Use PR reviews for quality
8. **Test before push**: Ensure code works before pushing

---

*📖 For more advanced Git workflows, see the [official Git documentation](https://git-scm.com/doc)*
