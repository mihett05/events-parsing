module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
    'airbnb',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs', 'vite.config.ts'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', '@typescript-eslint'],
  rules: {
    'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    'react/jsx-filename-extension': [1, { extensions: ['.jsx', '.js', '.tsx', '.ts'] }],
    'react/react-in-jsx-scope': 'off',
    'linebreak-style': ['warn', 'windows'],
    'import/extensions': 'never',
  },
};
