@echo off
echo Linting frontend code with ESLint (legacy config)...
npx eslint --config .eslintrc.js --fix "Frontend/src/**/*.{js,jsx}"
echo Frontend linting complete.
