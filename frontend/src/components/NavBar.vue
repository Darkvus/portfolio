<script setup>
import { ref, watch } from 'vue'
import { inject } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { isDark, toggleTheme } = inject('theme')
const route = useRoute()
const { t, locale } = useI18n()

const menuOpen = ref(false)

const pages = [
  { path: '/',         key: 'nav.home'     },
  { path: '/blog',     key: 'nav.blog'     },
  { path: '/projects', key: 'nav.projects' },
  { path: '/about',    key: 'nav.about'    },
]

function setLang(lang) {
  locale.value = lang
  localStorage.setItem('lang', lang)
}

// Close menu on navigation
watch(() => route.path, () => { menuOpen.value = false })
</script>

<template>
  <nav class="fixed top-0 left-0 right-0 z-[100] bg-zinc-950/90 backdrop-blur-sm border-b border-zinc-800">
    <div class="max-w-3xl mx-auto px-6 h-12 flex items-center gap-3 font-mono text-xs">

      <!-- Prompt -->
      <span class="text-violet-500 shrink-0">darkvus_dev</span>
      <span class="text-zinc-600 shrink-0">:</span>
      <span class="text-blue-400 shrink-0">{{ route.path }}</span>
      <span class="text-zinc-600 shrink-0">$</span>

      <!-- Nav links — desktop only -->
      <div class="hidden sm:flex items-center gap-1 ml-1">
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

      <div class="flex-1" />

      <!-- Unified controls pill -->
      <div class="flex items-center rounded-md border border-zinc-800 overflow-hidden">
        <button
          @click="setLang(locale === 'en' ? 'es' : 'en')"
          class="w-8 h-6 flex items-center justify-center text-[10px] font-mono text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 transition-all border-r border-zinc-800"
        >{{ locale === 'en' ? 'EN' : 'ES' }}</button>
        <button
          @click="toggleTheme"
          class="w-8 h-6 flex items-center justify-center text-zinc-500 hover:text-zinc-200 hover:bg-zinc-800 transition-all"
        >
          <span :class="isDark ? 'i-lucide-sun' : 'i-lucide-moon'" class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Burger button — mobile only -->
      <button
        @click="menuOpen = !menuOpen"
        class="sm:hidden w-8 h-6 flex items-center justify-center text-zinc-500 hover:text-zinc-200 transition-colors"
        :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
      >
        <span :class="menuOpen ? 'i-lucide-x' : 'i-lucide-menu'" class="w-4 h-4" />
      </button>
    </div>

    <!-- Mobile menu -->
    <div
      v-if="menuOpen"
      class="sm:hidden border-t border-zinc-800 bg-zinc-950/95 backdrop-blur-sm"
    >
      <div class="max-w-3xl mx-auto px-6 py-3 flex flex-col gap-1">
        <RouterLink
          v-for="p in pages"
          :key="p.path"
          :to="p.path"
          class="px-3 py-2 rounded-lg font-mono text-sm transition-colors"
          :class="route.path === p.path
            ? 'text-violet-400 bg-violet-950/60'
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'"
        >{{ t(p.key) }}</RouterLink>
      </div>
    </div>
  </nav>
</template>
