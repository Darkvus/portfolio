import { createI18n } from 'vue-i18n'
import en from './en.js'
import es from './es.js'

export default createI18n({
  legacy: false,
  locale: localStorage.getItem('lang') || 'en',
  fallbackLocale: 'en',
  messages: { en, es },
})
