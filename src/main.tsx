import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/app.tsx';
import { CssBaseline } from '@mui/material';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CssBaseline />
    <App />
  </React.StrictMode>,
);
