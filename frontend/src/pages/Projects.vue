<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const repos = ref([])
const loading = ref(true)
const error = ref(null)
const selectedLang = ref('all')

const GITHUB_USER = 'Darkvus'

// Language color map (GitHub-style)
const langColors = {
  Python:     '#3572A5',
  JavaScript: '#f1e05a',
  TypeScript: '#3178c6',
  Vue:        '#41b883',
  HTML:       '#e34c26',
  CSS:        '#563d7c',
  Shell:      '#89e051',
  Go:         '#00ADD8',
  Rust:       '#dea584',
  Java:       '#b07219',
}

onMounted(async () => {
  try {
    const res = await fetch(
      `https://api.github.com/users/${GITHUB_USER}/repos?sort=created&direction=desc&per_page=100&type=public`
    )
    if (!res.ok) throw new Error('GitHub API error')
    const data = await res.json()
    repos.value = data.filter(r => !r.fork)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const languages = computed(() => {
  const langs = new Set(repos.value.map(r => r.language).filter(Boolean))
  return ['all', ...Array.from(langs).sort()]
})

const filtered = computed(() => {
  if (selectedLang.value === 'all') return repos.value
  return repos.value.filter(r => r.language === selectedLang.value)
})

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime()
  const days = Math.floor(diff / 86400000)
  if (days === 0) return 'today'
  if (days === 1) return '1d ago'
  if (days < 30) return `${days}d ago`
  const months = Math.floor(days / 30)
  if (months < 12) return `${months}mo ago`
  return `${Math.floor(months / 12)}y ago`
}

function formatStars(n) {
  return n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n)
}
</script>

<template>
  <section class="space-y-8 pt-6">

    <!-- Header -->
    <div class="space-y-1">
      <h1 class="text-2xl font-bold tracking-tight">{{ t('projects.title') }}</h1>
      <p class="text-sm text-zinc-500 font-mono">{{ t('projects.description') }}</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="font-mono text-sm text-zinc-400 animate-pulse">
      {{ t('projects.loading') }}
    </div>

    <!-- Error -->
    <div v-else-if="error" class="font-mono text-sm text-red-400">
      // error: {{ error }}
    </div>

    <template v-else>
      <!-- Language filters -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="lang in languages"
          :key="lang"
          @click="selectedLang = lang"
          class="px-3 py-1 rounded-full text-xs font-mono transition-all border"
          :class="selectedLang === lang
            ? 'bg-violet-600 border-violet-600 text-white'
            : 'border-zinc-700 text-zinc-400 hover:border-violet-500 hover:text-violet-400'"
        >
          <span
            v-if="lang !== 'all'"
            class="inline-block w-2 h-2 rounded-full mr-1.5 align-middle"
            :style="{ background: langColors[lang] || '#8b8b8b' }"
          />
          {{ lang === 'all' ? t('projects.filterAll') : lang }}
        </button>
      </div>

      <!-- Count -->
      <p class="font-mono text-xs text-zinc-500">
        // {{ filtered.length }} {{ t('projects.repos') }}
      </p>

      <!-- Cards grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <a
          v-for="repo in filtered"
          :key="repo.id"
          :href="repo.html_url"
          target="_blank"
          rel="noopener"
          class="group flex flex-col gap-3 p-4 rounded-xl border border-zinc-800/60
                 bg-zinc-900/30 hover:bg-zinc-900/70 hover:border-violet-700/50
                 transition-all duration-200 hover:shadow-lg hover:shadow-violet-950/20
                 hover:-translate-y-0.5"
        >
          <!-- Top row -->
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-2 min-w-0">
              <span class="i-lucide-folder text-violet-400 w-4 h-4 shrink-0 group-hover:text-violet-300 transition-colors" />
              <span class="font-mono text-sm font-semibold text-zinc-200 truncate group-hover:text-violet-300 transition-colors">
                {{ repo.name }}
              </span>
            </div>
            <span class="i-lucide-external-link w-3.5 h-3.5 text-zinc-600 group-hover:text-violet-400 transition-colors shrink-0 mt-0.5" />
          </div>

          <!-- Description -->
          <p class="text-xs text-zinc-500 leading-relaxed line-clamp-2 flex-1">
            {{ repo.description || t('projects.noDescription') }}
          </p>

          <!-- Topics -->
          <div v-if="repo.topics?.length" class="flex flex-wrap gap-1">
            <span
              v-for="topic in repo.topics.slice(0, 4)"
              :key="topic"
              class="px-1.5 py-0.5 text-[10px] font-mono rounded bg-zinc-800 text-zinc-500"
            >
              {{ topic }}
            </span>
          </div>

          <!-- Footer -->
          <div class="flex items-center gap-3 text-[10px] font-mono text-zinc-600 pt-1 border-t border-zinc-800/60">
            <!-- Language -->
            <span v-if="repo.language" class="flex items-center gap-1">
              <span
                class="inline-block w-2 h-2 rounded-full"
                :style="{ background: langColors[repo.language] || '#8b8b8b' }"
              />
              {{ repo.language }}
            </span>

            <!-- Stars -->
            <span v-if="repo.stargazers_count > 0" class="flex items-center gap-1">
              <span class="i-lucide-star w-3 h-3" />
              {{ formatStars(repo.stargazers_count) }}
            </span>

            <!-- Forks -->
            <span v-if="repo.forks_count > 0" class="flex items-center gap-1">
              <span class="i-lucide-git-fork w-3 h-3" />
              {{ repo.forks_count }}
            </span>

            <!-- Updated -->
            <span class="ml-auto">{{ timeAgo(repo.pushed_at) }}</span>
          </div>
        </a>
      </div>

      <!-- Empty state -->
      <div v-if="filtered.length === 0" class="py-12 text-center font-mono text-sm text-zinc-500">
        // {{ t('projects.empty') }}
      </div>
    </template>

  </section>
</template>
