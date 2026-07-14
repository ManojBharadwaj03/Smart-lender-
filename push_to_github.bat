@echo off
cd /d "%~dp0"
set REPO_URL=https://github.com/manojbharadwaj/project-name.git

echo Initializing git repository...
git init

echo Adding files...
git add .

echo Creating initial commit...
git commit -m "Initial commit - Smart Lender project"

echo Adding remote origin...
git remote add origin %REPO_URL%

echo Setting main branch...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo Done. If push fails, please verify that Git is installed and you are authenticated with GitHub.
