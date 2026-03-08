import { defineConfig, presetUno, presetIcons, presetWebFonts } from 'unocss'
import presetTypography from '@unocss/preset-typography'

export default defineConfig({
  presets: [
    presetUno({ dark: 'class' }),
    presetIcons(),
    presetTypography(),
    presetWebFonts({
      fonts: {
        sans: 'Inter',
        mono: 'Fira Code',
      },
    }),
  ],
  theme: {
    colors: {
      accent: '#8b5cf6',
      'accent-hover': '#7c3aed',
    },
  },
})
