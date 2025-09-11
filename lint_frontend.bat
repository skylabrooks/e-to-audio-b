@echo off
echo Linting frontend code with ESLint...
npx eslint --fix "Frontend/src/**/*.{js,jsx}"
echo Frontend linting complete.
