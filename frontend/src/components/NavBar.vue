<script setup>
import { inject } from 'vue'
import { RouterLink } from 'vue-router'

const { isDark, toggleTheme } = inject('theme')
</script>

<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-sm border-b border-zinc-100 dark:border-zinc-800/60">
    <div class="max-w-3xl mx-auto px-6 h-14 flex items-center justify-between">
      <RouterLink
        to="/"
        class="font-mono text-sm font-semibold text-violet-500 hover:text-violet-400 transition-colors"
      >
        darkvus<span class="text-zinc-400 dark:text-zinc-600">_dev</span>
      </RouterLink>

      <div class="flex items-center gap-6">
        <RouterLink
          to="/blog"
          class="text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
          active-class="text-zinc-900 dark:text-zinc-100 font-medium"
        >
          Blog
        </RouterLink>
        <RouterLink
          to="/about"
          class="text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
          active-class="text-zinc-900 dark:text-zinc-100 font-medium"
        >
          About
        </RouterLink>
        <button
          @click="toggleTheme"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          class="w-8 h-8 flex items-center justify-center rounded-lg text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-all text-base"
        >
          <span v-if="isDark">☀️</span>
          <span v-else>🌙</span>
        </button>
      </div>
    </div>
  </nav>
</template>
