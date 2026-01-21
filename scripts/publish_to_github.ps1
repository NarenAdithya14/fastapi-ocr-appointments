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

git push -u origin $branch

Write-Host "Done. If push failed, ensure you have rights to create the repository or create it on GitHub and then run this script again."