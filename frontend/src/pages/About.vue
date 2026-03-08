<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const skills = [
  {
    category: '// backend',
    items: ['Python', 'FastAPI', 'Django', 'Typer', 'SQLAlchemy', 'Pytest'],
  },
  {
    category: '// databases',
    items: ['PostgreSQL', 'SQLite', 'MongoDB', 'Redis'],
  },
  {
    category: '// cloud & infra',
    items: ['AWS S3', 'Docker', 'GitHub Actions', 'Render', 'Vercel'],
  },
  {
    category: '// tools',
    items: ['Git', 'REST APIs', 'JWT', 'OpenAPI', 'Linux'],
  },
]
</script>

<template>
  <section class="space-y-12">

    <div class="space-y-2 pt-6">
      <h1 class="text-3xl font-bold">{{ t('about.title') }}</h1>
    </div>

    <!-- Bio -->
    <div class="space-y-4 text-zinc-600 dark:text-zinc-400 leading-relaxed">
      <p v-html="t('about.bio1')" />
      <p v-html="t('about.bio2')" />
      <p v-html="t('about.bio3')" />
    </div>

    <!-- Skills -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">{{ t('about.skills') }}</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div
          v-for="cat in skills"
          :key="cat.category"
          class="p-4 rounded-xl border border-zinc-100 dark:border-zinc-800/60"
        >
          <p class="text-xs font-mono text-violet-500 mb-2.5">{{ cat.category }}</p>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="s in cat.items"
              :key="s"
              class="text-xs px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400"
            >
              {{ s }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">{{ t('about.contact') }}</p>
      <div class="flex flex-col gap-3">
        <a
          href="https://github.com/Darkvus"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400 hover:text-violet-500 transition-colors w-fit"
        >
          <span class="i-simple-icons-github w-4 h-4" />
          self →
        </a>
        <a
          href="https://www.linkedin.com/in/alejandro-jose-c-66010aa1/"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400 hover:text-[#0077b5] transition-colors w-fit"
        >
          <span class="i-simple-icons-linkedin w-4 h-4" />
          self →
        </a>
      </div>
    </div>

  </section>
</template>
