import React from 'react';
import ReactDOM from 'react-dom/client';
import App from '@/app/app.tsx';
import { CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './shared/store/store';
import './shared/config/i18n';

import dayjs from 'dayjs';
import 'dayjs/locale/ru';

import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

dayjs.locale('ru');

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ru">
      <Provider store={store}>
        <CssBaseline />
        <App />
      </Provider>
    </LocalizationProvider>
  </React.StrictMode>,
);
