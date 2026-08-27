# copier-template-github-action-typescript

Copier template to scaffold a GitHub Action with TypeScript.

## 🚀 Quick Start

To create a new GitHub Action, run the following commands:

1. Create a new empty repository on GitHub and clone it to your local machine.

2. Run the following commands in the root of the cloned repository :

```bash
copier copy gh:mihaly-farkas/copier-template-github-action-typescript --vcs-ref main .
npm install
npm run dependency-management:update-minor-dependencies
git init
git add .
git commit -m "chore: scaffold the GitHub Action (TypeScript) skeleton"
git branch -M main
git remote add origin https://github.com/$(yq .githubRepositoryOwner .copier-answers.yml)/$(yq .githubRepositoryName .copier-answers.yml).git
git push -u origin main
```

## ⚠️ Disclaimer & Liability

This is a hobby project. I make no guarantee that it is production-ready. The project may contain experimental or incomplete features.

Use it at your own risk, and carefully review and adapt the configuration before using it in your own environment.

## ⚖️ License

This project is licensed under the [MIT License](https://github.com/mihaly-farkas/copier-template-github-action-typescript?tab=MIT-1-ov-file).
