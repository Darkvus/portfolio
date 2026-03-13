<script setup>
import { inject, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

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
const settingsRef  = ref(null)

function onDocClick(e) {
  if (settingsRef.value && !settingsRef.value.contains(e.target)) {
    settingsOpen.value = false
  }
}

onMounted(()  => document.addEventListener('click', onDocClick))
onUnmounted(() => document.removeEventListener('click', onDocClick))

function setLang(lang) {
  locale.value = lang
  localStorage.setItem('lang', lang)
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

      <!-- Nav links -->
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

      <div class="flex-1" />

      <!-- Settings gear -->
      <div ref="settingsRef" class="relative">
        <button
          @click.stop="settingsOpen = !settingsOpen"
          class="p-1 rounded transition-colors"
          :class="settingsOpen ? 'text-violet-400' : 'text-zinc-500 hover:text-violet-400'"
        >
          <span class="i-lucide-settings w-3.5 h-3.5" />
        </button>

        <Transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition duration-75 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="settingsOpen"
            class="absolute right-0 top-8 w-44 rounded-xl border border-zinc-800 bg-zinc-950 shadow-xl shadow-black/50 py-1 origin-top-right"
          >
            <!-- Language -->
            <p class="px-3 pt-1.5 pb-1 text-[10px] font-mono text-zinc-600 uppercase tracking-wider">language</p>
            <button
              v-for="lang in ['en', 'es']"
              :key="lang"
              @click.stop="setLang(lang)"
              class="w-full flex items-center justify-between px-3 py-1.5 text-xs font-mono hover:bg-zinc-800/60 transition-colors"
              :class="locale === lang ? 'text-violet-400' : 'text-zinc-400'"
            >
              <span>{{ lang === 'en' ? '🇬🇧 English' : '🇪🇸 Español' }}</span>
              <span v-if="locale === lang" class="i-lucide-check w-3 h-3" />
            </button>

            <div class="mx-3 my-1 border-t border-zinc-800" />

            <!-- Theme -->
            <p class="px-3 pt-1.5 pb-1 text-[10px] font-mono text-zinc-600 uppercase tracking-wider">theme</p>
            <button
              @click.stop="isDark || toggleTheme()"
              class="w-full flex items-center justify-between px-3 py-1.5 text-xs font-mono hover:bg-zinc-800/60 transition-colors"
              :class="isDark ? 'text-violet-400' : 'text-zinc-400'"
            >
              <span>🌙 Dark</span>
              <span v-if="isDark" class="i-lucide-check w-3 h-3" />
            </button>
            <button
              @click.stop="!isDark || toggleTheme()"
              class="w-full flex items-center justify-between px-3 py-1.5 text-xs font-mono hover:bg-zinc-800/60 transition-colors"
              :class="!isDark ? 'text-violet-400' : 'text-zinc-400'"
            >
              <span>☀️ Light</span>
              <span v-if="!isDark" class="i-lucide-check w-3 h-3" />
            </button>
          </div>
        </Transition>
      </div>

    </div>
  </nav>
</template>
