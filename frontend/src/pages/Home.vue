<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getPosts } from '../api/index.js'
import NewsletterSignup from '../components/NewsletterSignup.vue'

const { t, locale } = useI18n()
const posts = ref([])
const loading = ref(true)

const stack = [
  'Python', 'FastAPI', 'Django', 'Typer',
  'SQLAlchemy', 'PostgreSQL', 'MongoDB',
  'Docker', 'AWS', 'GitHub Actions',
]

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(locale.value === 'es' ? 'es-ES' : 'en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

onMounted(async () => {
  try {
    posts.value = await getPosts(locale.value)
  } catch {
    // no posts yet or API unavailable
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="space-y-16">

    <!-- Hero -->
    <div class="space-y-6 pt-6">
      <div class="flex items-center gap-6">
        <div class="space-y-3 flex-1">
          <h1 class="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Alejandro<br />Caraballo
          </h1>
          <p class="text-xl text-zinc-400 font-light">
            {{ t('home.role') }}
          </p>
        </div>
        <img
          src="/darkvus.png"
          alt="Alejandro Caraballo"
          class="w-24 h-24 sm:w-28 sm:h-28 rounded-full object-cover ring-2 ring-violet-500/30 shrink-0"
        />
      </div>
      <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-lg text-base">
        {{ t('home.bio') }}
      </p>
      <div class="flex flex-wrap items-center gap-3">
        <a
          href="https://github.com/Darkvus"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-zinc-900 dark:bg-zinc-100 text-zinc-100 dark:text-zinc-900 text-sm font-medium hover:opacity-80 transition-opacity"
        >
          <span class="i-simple-icons-github w-5 h-5" />
        </a>
        <a
          href="https://www.linkedin.com/in/alejandro-jose-c-66010aa1/"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0077b5] text-white text-sm font-medium hover:opacity-80 transition-opacity"
        >
          <span class="i-simple-icons-linkedin w-5 h-5" />
        </a>
        <RouterLink
          to="/about"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-violet-500 transition-colors"
        >
          <span class="i-lucide-user w-5 h-5" />
          {{ t('home.about') }}
        </RouterLink>
      </div>
    </div>

    <!-- Stack -->
    <div class="space-y-3">
      <p class="font-mono text-xs text-zinc-400">{{ t('home.stack') }}</p>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="tech in stack"
          :key="tech"
          class="px-3 py-1 text-xs font-mono rounded-full bg-zinc-100 dark:bg-zinc-800/80 text-zinc-600 dark:text-zinc-400"
        >
          {{ tech }}
        </span>
      </div>
    </div>

    <!-- Recent posts -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <p class="font-mono text-xs text-zinc-400">{{ t('home.recent') }}</p>
        <RouterLink to="/blog" class="text-xs text-violet-500 hover:text-violet-400 transition-colors">
          {{ t('home.viewAll') }}
        </RouterLink>
      </div>

      <div v-if="loading" class="text-sm text-zinc-400 font-mono">{{ t('home.loading') }}</div>

      <div v-else-if="posts.length === 0" class="py-8 text-center">
        <p class="font-mono text-zinc-400 text-sm">{{ t('home.noPosts') }}</p>
      </div>

      <div v-else class="space-y-2">
        <RouterLink
          v-for="post in posts.slice(0, 3)"
          :key="post.id"
          :to="`/blog/${post.slug}`"
          class="flex items-start justify-between gap-4 p-4 rounded-xl border border-zinc-100 dark:border-zinc-800/60 hover:border-violet-200 dark:hover:border-violet-800/60 hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-all group"
        >
          <div class="space-y-0.5 min-w-0">
            <p class="font-medium text-sm group-hover:text-violet-500 transition-colors truncate">
              {{ post.title }}
            </p>
            <p v-if="post.excerpt" class="text-xs text-zinc-500 truncate">{{ post.excerpt }}</p>
          </div>
          <span class="text-xs text-zinc-400 shrink-0 mt-0.5">{{ formatDate(post.created_at) }}</span>
        </RouterLink>
      </div>
    </div>

    <!-- Newsletter -->
    <NewsletterSignup />

  </section>
</template>
