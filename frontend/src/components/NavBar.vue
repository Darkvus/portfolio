<script setup>
import { inject } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

const { isDark, toggleTheme } = inject('theme')
const route = useRoute()

const pages = [
  { path: '/',      label: 'home'  },
  { path: '/blog',  label: 'blog'  },
  { path: '/about', label: 'about' },
]

</script>

<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-zinc-950/90 backdrop-blur-sm border-b border-zinc-800">
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
        >cd {{ p.label }}</RouterLink>
      </div>

      <!-- Spacer -->
      <div class="flex-1" />

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
