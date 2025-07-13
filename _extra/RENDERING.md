# Rendering Strategy

This repository uses a **hybrid rendering approach** that combines the benefits of both local pre-rendering and GitHub Actions automation.

## How It Works

### 1. Primary: Local Pre-rendering
- Run `quarto render` locally
- Commit both source files and `docs/` folder
- Push to GitHub
- Site is immediately updated

### 2. Fallback: GitHub Actions
- Monitors all source file changes
- Automatically re-renders if you forget
- Ensures `docs/` stays in sync with source
- Adds commit with updated files

## Workflows

### Quick Edit Workflow
```bash
# Edit your content
edit sessions/day1/index.md

# Render locally (recommended)
quarto render

# Commit everything
git add .
git commit -m "Update day 1 content"
git push
```

### Lazy Workflow (Let GitHub Do It)
```bash
# Edit your content
edit sessions/day1/index.md

# Just commit source (GitHub will render)
git add sessions/day1/index.md
git commit -m "Update day 1 content"
git push

# GitHub Actions will:
# 1. Detect the change
# 2. Run quarto render
# 3. Commit updated docs/
```

### Force Rebuild
```bash
# Via GitHub UI: Actions → Verify and Update Site → Run workflow → Force render ✓

# Or trigger with empty commit
git commit --allow-empty -m "Trigger rebuild"
git push
```

## Benefits

1. **Fast Updates**: Pre-render locally for immediate deployment
2. **Safety Net**: GitHub Actions catches forgotten renders
3. **Consistency**: Ensures docs/ always matches source
4. **Flexibility**: Work locally or through GitHub web editor
5. **Verification**: PRs show what needs rendering

## Configuration

### For Heavy Computations
Add to frontmatter of computation-heavy files:
```yaml
---
title: "Heavy Analysis"
execute:
  freeze: true  # Cache results
---
```

### Skip Auto-render
Add `[skip ci]` to commit message:
```bash
git commit -m "WIP: Draft content [skip ci]"
```

## Monitoring

Check render status:
1. Go to **Actions** tab in GitHub
2. Look for ✓ or ✗ next to commits
3. Click for details if failed

## Troubleshooting

**If GitHub Actions fails:**
1. Check the error in Actions tab
2. Fix the issue locally
3. Run `quarto render` locally
4. Commit and push both source and docs/

**If docs/ gets out of sync:**
1. Delete local `docs/` folder
2. Run `quarto render`
3. Commit fresh `docs/` folder
4. Push with message "Rebuild docs folder"

## Best Practices

1. **Usually**: Render locally before pushing
2. **Quick fixes**: Let GitHub handle small edits
3. **Heavy computation**: Always pre-render locally
4. **Check Actions**: Monitor for failures
5. **Keep synced**: Don't edit `docs/` directly
