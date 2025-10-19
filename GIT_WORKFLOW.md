# Git Workflow Guide

## Before Making Changes (Pull Latest)

Always run these commands BEFORE you start making changes to ensure you have the latest code:

```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project

# Check current status
git status

# Pull latest changes from GitHub
git pull origin main

# If there are conflicts, Git will tell you which files
# You'll need to manually resolve conflicts before continuing
```

**Why?** This prevents conflicts by making sure you're working with the latest version.

---

## After Making Changes (Push Updates)

Run these commands AFTER you've made changes and want to sync to GitHub:

```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project

# See what files changed
git status

# Add all changed files
git add .

# Commit with a descriptive message
git commit -m "Brief description of what you changed"

# Push to GitHub
git push origin main
```

---

## Common Scenarios

### Scenario 1: Quick Update (Most Common)

```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project
git add .
git commit -m "Updated slideshow configuration"
git push origin main
```

### Scenario 2: Check What Changed Before Committing

```bash
# See which files changed
git status

# See exactly what changed in files
git diff

# Add and commit
git add .
git commit -m "Your message here"
git push origin main
```

### Scenario 3: Undo Changes (Before Commit)

```bash
# Undo changes to a specific file
git checkout -- filename.py

# Undo ALL changes (careful!)
git reset --hard
```

### Scenario 4: Made a Mistake in Last Commit

```bash
# Change the last commit message
git commit --amend -m "New commit message"
git push origin main --force
```

---

## Daily Workflow (Recommended)

### Morning (Before Starting Work)
```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project
git pull origin main
```

### Evening (After Making Changes)
```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project
git add .
git commit -m "Description of today's changes"
git push origin main
```

---

## Troubleshooting

### Problem: "Your branch is behind"
```bash
# Pull the latest changes
git pull origin main
```

### Problem: "Merge conflict"
```bash
# 1. Open the conflicted files in your editor
# 2. Look for markers like <<<<<<< HEAD
# 3. Manually fix the conflicts
# 4. Then:
git add .
git commit -m "Resolved merge conflicts"
git push origin main
```

### Problem: "Remote repository not found"
```bash
# Check your remote URL
git remote -v

# If wrong, update it:
git remote set-url origin https://github.com/YOUR_USERNAME/esp32-tft-project.git
```

### Problem: "Permission denied"
```bash
# You may need to authenticate with GitHub
# Use a Personal Access Token instead of password
# Generate one at: https://github.com/settings/tokens
```

### Problem: "Diverged branches"
```bash
# Pull and merge
git pull origin main

# Or pull and rebase (cleaner history)
git pull --rebase origin main
```

---

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `git status` | Show what files changed |
| `git pull origin main` | Get latest from GitHub |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save changes locally |
| `git push origin main` | Upload to GitHub |
| `git diff` | Show exact changes |
| `git log` | Show commit history |
| `git remote -v` | Show GitHub URL |

---

## Best Practices

1. **Always pull before making changes** - Prevents conflicts
2. **Commit often** - Small, frequent commits are better than large ones
3. **Write clear commit messages** - Future you will thank you
4. **Don't commit sensitive data** - API keys, passwords, etc.
5. **Test before committing** - Make sure your code works

---

## Example Commit Messages

Good:
- ✅ "Add per-image delay configuration"
- ✅ "Fix display orientation bug"
- ✅ "Optimize image loading speed"
- ✅ "Update README with setup instructions"

Bad:
- ❌ "stuff"
- ❌ "changes"
- ❌ "fix"
- ❌ "asdf"

---

## Need Help?

- Check status: `git status`
- See what changed: `git diff`
- View commit history: `git log --oneline`
- Undo last commit (keep changes): `git reset --soft HEAD~1`
- Undo last commit (discard changes): `git reset --hard HEAD~1`
