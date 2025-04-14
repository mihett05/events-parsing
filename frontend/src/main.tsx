import React from 'react';
import ReactDOM from 'react-dom/client';
import App from '@/app/app.tsx';
import { CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './shared/store/store';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <CssBaseline />
      <App />
    </Provider>
  </React.StrictMode>,
);
