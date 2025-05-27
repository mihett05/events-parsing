import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { z } from 'zod';
import { zodI18nMap } from 'zod-i18n-map';
import translation from 'zod-i18n-map/locales/ru/zod.json';
import LanguageDetector from 'i18next-browser-languagedetector';

import translationRU from '../locales/ru/translation.json';

const resources = {
  ru: {
    translation: translationRU,
    zod: translation,
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'ru',

    interpolation: {
      escapeValue: false,
    },

    detection: {
      order: ['querystring', 'cookie', 'localStorage', 'sessionStorage', 'navigator', 'htmlTag'],
      caches: ['cookie', 'localStorage'],
    },
  });
z.setErrorMap(zodI18nMap);

export { z };
export default i18n;
