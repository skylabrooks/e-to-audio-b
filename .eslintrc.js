module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true,
  },
  extends: ['eslint:recommended', 'react-app', 'react-app/jest'],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: ['react', 'react-hooks'],
  rules: {
    // Code quality rules
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'prefer-const': 'warn',
    'no-var': 'error',

    // React specific rules
    'react/jsx-uses-react': 'off', // Not needed in React 17+
    'react/react-in-jsx-scope': 'off', // Not needed in React 17+
    'react/prop-types': 'warn',
    'react/jsx-key': 'error',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // Style rules
    indent: ['warn', 2],
    quotes: ['warn', 'single'],
    semi: ['warn', 'always'],
    'comma-dangle': ['warn', 'always-multiline'],
    'object-curly-spacing': ['warn', 'always'],
    'array-bracket-spacing': ['warn', 'never'],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  ignorePatterns: ['build/', 'dist/', 'node_modules/', '*.min.js', 'Backend/'],
};
