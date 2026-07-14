# GitHub Repository Setup for Smart Lender

This project can be published to GitHub once Git is installed on your machine.

## Local Git setup

1. Install Git for Windows from https://git-scm.com/download/win
2. Open a command prompt or Git Bash in the project folder:
   ```cmd
   cd "c:\Users\HP\OneDrive\Desktop\manoj.project"
   ```
3. Initialize the repository:
   ```cmd
   git init
   git add .
   git commit -m "Initial commit - Smart Lender project"
   ```
4. Create a GitHub repository named `project-name` under the account `manojbharadwaj`.
5. Add the remote and push:
   ```cmd
   git remote add origin https://github.com/manojbharadwaj/project-name.git
   git branch -M main
   git push -u origin main
   ```

## Recommended GitHub files

- `.gitignore` (already present)
- `README.md` (already present)
- `requirements.txt` (already present)

## Notes

- If you want, I can also prepare a `LICENSE` file and a more complete GitHub README section for the repository.
