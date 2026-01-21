# Publish repository to GitHub (PowerShell)
# Usage: run from repository root after configuring your local git credentials
# Replace <your-email> and <your-name> if needed. This script will create remote 'origin' pointing to your GitHub repo.

param(
    [string]$githubUser = "Narenadithya14",
    [string]$repoName = "fastapi-ocr-appointments",
    [string]$branch = "main"
)

Write-Host "Initializing git repository and publishing to GitHub: $githubUser/$repoName"

if (-not (Test-Path .git)) {
    git init
}

git add .
$commitMsg = "chore: initial demo commit"
git commit -m $commitMsg -q

$remote = "https://github.com/$githubUser/$repoName.git"

# Add remote if not present
try {
    git remote add origin $remote
} catch {
    Write-Host "Remote origin already exists, updating URL to $remote"
    git remote set-url origin $remote
}

git branch -M $branch

Write-Host "Now pushing to origin/$branch. You will be prompted for credentials if required."
try {
    git push -u origin $branch
    Write-Host "Pushed to origin/$branch successfully."
} catch {
    Write-Host "Initial push failed. Attempting to detect cause..."
    # Check if remote exists on GitHub (ls-remote will fail if repo missing or no access)
    $ls = git ls-remote origin 2>&1 | Out-String
    if ($ls -match "Repository not found") {
        Write-Host "Remote repository not found on GitHub: $remote"
        # Try to create repository using GitHub CLI if available
        $gh = Get-Command gh -ErrorAction SilentlyContinue
        if ($gh) {
            Write-Host "Found gh (GitHub CLI). Attempting to create repository $githubUser/$repoName..."
            try {
                gh repo create "$githubUser/$repoName" --public --source=. --remote=origin --push --confirm
                Write-Host "Repository created and pushed via gh CLI."
            } catch {
                Write-Host "gh CLI failed to create the repository. Please create the repository manually at https://github.com/new and re-run this script."
                exit 1
            }
        } else {
            Write-Host "gh CLI not found. Please create the repository 'https://github.com/$githubUser/$repoName' and re-run this script."
            exit 1
        }
    } else {
        Write-Host "Push failed for another reason. Inspect git output above."
        exit 1
    }
}

Write-Host "Done. If you see no repo on GitHub, create it manually and re-run this script or install gh CLI for automatic creation."