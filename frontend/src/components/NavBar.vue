<script setup>
import { inject, ref } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import i18n from '../i18n/index.js'

const { isDark, toggleTheme } = inject('theme')
const route = useRoute()
const { t, locale } = useI18n()

const pages = [
  { path: '/',         key: 'nav.home'     },
  { path: '/blog',     key: 'nav.blog'     },
  { path: '/projects', key: 'nav.projects' },
  { path: '/about',    key: 'nav.about'    },
]

const settingsOpen = ref(false)

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

      <!-- Settings gear -->
      <div class="relative">
        <button
          @click="settingsOpen = !settingsOpen"
          class="text-zinc-500 hover:text-violet-400 transition-colors p-1 rounded"
          :class="settingsOpen ? 'text-violet-400' : ''"
        >
          <span class="i-lucide-settings w-3.5 h-3.5" />
        </button>

        <!-- Dropdown -->
        <div
          v-if="settingsOpen"
          v-click-outside="() => settingsOpen = false"
          class="absolute right-0 top-8 w-44 rounded-xl border border-zinc-800 bg-zinc-950/95 backdrop-blur-sm shadow-xl shadow-black/40 py-1 z-50"
        >
          <!-- Language -->
          <div class="px-3 py-1.5 text-[10px] font-mono text-zinc-600 uppercase tracking-wider">language</div>
          <button
            v-for="lang in ['en', 'es']"
            :key="lang"
            @click="locale = lang; localStorage.setItem('lang', lang)"
            class="w-full flex items-center justify-between px-3 py-1.5 text-xs font-mono hover:bg-zinc-800/60 transition-colors"
            :class="locale === lang ? 'text-violet-400' : 'text-zinc-400'"
          >
            <span>{{ lang === 'en' ? '🇬🇧 English' : '🇪🇸 Español' }}</span>
            <span v-if="locale === lang" class="i-lucide-check w-3 h-3" />
          </button>

          <div class="mx-3 my-1 border-t border-zinc-800" />

          <!-- Theme -->
          <div class="px-3 py-1.5 text-[10px] font-mono text-zinc-600 uppercase tracking-wider">theme</div>
          <button
            @click="isDark || toggleTheme()"
            class="w-full flex items-center justify-between px-3 py-1.5 text-xs font-mono hover:bg-zinc-800/60 transition-colors"
            :class="isDark ? 'text-violet-400' : 'text-zinc-400'"
          >
            <span>🌙 Dark</span>
            <span v-if="isDark" class="i-lucide-check w-3 h-3" />
          </button>
          <button
            @click="!isDark || toggleTheme()"
            class="w-full flex items-center justify-between px-3 py-1.5 text-xs font-mono hover:bg-zinc-800/60 transition-colors"
            :class="!isDark ? 'text-violet-400' : 'text-zinc-400'"
          >
            <span>☀️ Light</span>
            <span v-if="!isDark" class="i-lucide-check w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
