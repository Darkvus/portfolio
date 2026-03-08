<script setup>
import { inject } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import i18n from '../i18n/index.js'

const { isDark, toggleTheme } = inject('theme')
const route = useRoute()
const { t, locale } = useI18n()

const pages = [
  { path: '/',      key: 'nav.home'  },
  { path: '/blog',  key: 'nav.blog'  },
  { path: '/about', key: 'nav.about' },
]

function toggleLang() {
  locale.value = locale.value === 'en' ? 'es' : 'en'
  localStorage.setItem('lang', locale.value)
}
</script>

<template>
  <nav class="fixed top-0 left-0 right-0 z-[100] bg-zinc-950/90 backdrop-blur-sm border-b border-zinc-800">
    <div class="max-w-3xl mx-auto px-6 h-12 flex items-center gap-2 font-mono text-xs">

      <!-- Prompt -->
      <span class="text-violet-500 shrink-0">darkvus_dev</span>
      <span class="text-zinc-600 shrink-0">:</span>
      <span class="text-blue-400 shrink-0">{{ route.path === '/' ? '~' : route.path }}</span>
      <span class="text-zinc-600 shrink-0">$</span>

      <!-- Nav links as "cd" commands -->
      <div class="flex items-center gap-1 ml-1">
        <RouterLink
          v-for="p in pages"
          :key="p.path"
          :to="p.path"
          class="px-2 py-0.5 rounded transition-colors"
          :class="route.path === p.path
            ? 'text-violet-400 bg-violet-950/60'
            : 'text-zinc-500 hover:text-zinc-200'"
        >{{ t(p.key) }}</RouterLink>
      </div>

      <!-- Spacer -->
      <div class="flex-1" />

      <!-- Language toggle -->
      <button
        @click="toggleLang"
        :title="locale === 'en' ? 'Cambiar a Español' : 'Switch to English'"
        class="text-zinc-500 hover:text-zinc-200 transition-colors px-1 text-[10px] font-mono"
      >
        {{ locale === 'en' ? 'ES' : 'EN' }}
      </button>

      <!-- Theme toggle -->
      <button
        @click="toggleTheme"
        :title="isDark ? 'light mode' : 'dark mode'"
        class="text-zinc-500 hover:text-zinc-200 transition-colors px-1"
      >
        <span class="text-[10px]">{{ isDark ? '☀️' : '🌙' }}</span>
      </button>

      <!-- Blinking cursor -->
      <span class="w-1.5 h-3.5 bg-violet-500 animate-pulse rounded-sm" />
    </div>
  </nav>
</template>
