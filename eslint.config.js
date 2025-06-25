import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';

// ESLint flat config for JavaScript/React projects
export default [
  // Global ignores for build and config files
  {
    ignores: [
      'dist/',
      'build/',
      'tailwind.config.js',
      'client/tailwind.config.js'
    ]
  },
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module'
      }
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh
    },
    rules: {
      // Enforce camelCase for variable and function names
      camelcase: ['error', { properties: 'always' }],
      // Enforce single quotes for string literals
      quotes: ['error', 'single'],
      // Enforce 2-space indentation
      indent: ['error', 2, { SwitchCase: 1 }],
      // Recommended rules
      ...js.configs?.recommended?.rules,
      ...reactHooks.configs?.recommended?.rules,
      // No unused variables except for those starting with _ or uppercase (React components)
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
      // Only export components from files for react-refresh
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true }
      ]
    }
  }
];