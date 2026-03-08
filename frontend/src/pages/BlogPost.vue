<script setup>
import { ref, inject, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import { getPost } from '../api/index.js'

const { isDark } = inject('theme')
const route   = useRoute()
const { t, locale } = useI18n()
const post    = ref(null)
const loading = ref(true)
const notFound = ref(false)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(locale.value === 'es' ? 'es-ES' : 'en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

async function fetchPost() {
  loading.value = true
  notFound.value = false
  try {
    post.value = await getPost(route.params.slug, locale.value)
  } catch {
    notFound.value = true
  } finally {
    loading.value = false
  }
}

watch(locale, fetchPost)
onMounted(fetchPost)
</script>

<template>
  <div>
    <div v-if="loading" class="pt-6 text-sm text-zinc-400 font-mono">loading...</div>

    <div v-else-if="notFound" class="pt-6 text-center py-16">
      <p class="font-mono text-zinc-400">{{ t('post.notFound') }}</p>
      <RouterLink to="/blog" class="text-sm text-violet-500 hover:text-violet-400 mt-4 inline-block">
        {{ t('post.backLink') }}
      </RouterLink>
    </div>

    <article v-else class="space-y-8">
      <header class="space-y-4 pt-6">
        <RouterLink to="/blog" class="text-sm text-zinc-400 hover:text-violet-500 transition-colors">
          {{ t('post.back') }}
        </RouterLink>
        <div class="space-y-3">
          <h1 class="text-3xl sm:text-4xl font-bold leading-tight">{{ post.title }}</h1>
          <div class="flex flex-wrap items-center gap-3 text-sm text-zinc-400">
            <span>{{ formatDate(post.created_at) }}</span>
            <template v-if="post.tags">
              <span class="text-zinc-300 dark:text-zinc-700">·</span>
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="tag in post.tags.split(',')"
                  :key="tag"
                  class="px-2 py-0.5 rounded-full bg-violet-50 dark:bg-violet-950/60 text-violet-600 dark:text-violet-400 text-xs"
                >{{ tag.trim() }}</span>
              </div>
            </template>
          </div>
        </div>
        <div class="border-b border-zinc-100 dark:border-zinc-800/60"></div>
      </header>

      <MdPreview
        :model-value="post.content"
        :theme="isDark ? 'dark' : 'light'"
        preview-theme="github"
        language="en-US"
        class="md-post-content"
        style="background: transparent; padding: 0;"
      />
    </article>
  </div>
</template>

<style>
/*
 * MdPreview root element has classes:
 *   md-editor-v3  md-editor-v3-previewOnly  [md-editor-v3-dark]
 * Inner wrapper: .md-editor-v3-preview-wrapper
 * Preview div:   .md-editor-v3-preview
 */

/* ── Isolate stacking context so code blocks never leak above navbar ── */
.md-post-content {
  isolation: isolate;
  position: relative;
  z-index: 0;
}

/* ── Root & wrappers: fully transparent ── */
.md-post-content.md-editor-v3,
.md-post-content .md-editor-v3-preview-wrapper,
.md-post-content .md-editor-v3-preview {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

/* ── Code block container: never overflow the stacking context ── */
.md-post-content pre,
.md-post-content .md-editor-v3-code,
.md-post-content .md-editor-v3-code-head {
  position: relative;
  z-index: 0;
}

/* ── Reset CSS custom properties (light + dark) ── */
.md-post-content .md-editor-v3-preview {
  --md-theme-bg-color: transparent !important;
  --md-theme-bg-color-inset: transparent !important;
  --md-theme-border-color: transparent !important;
  --md-theme-border-color-reverse: transparent !important;
  --md-theme-border-color-inset: transparent !important;
}

/* ── Word-wrap for all text content ── */
.md-post-content .md-editor-v3-preview {
  word-break: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  overflow-x: hidden;
}

/* ── Code blocks: scroll horizontally, no forced breaks ── */
.md-post-content pre {
  word-break: normal;
  overflow-wrap: normal;
  white-space: pre;
  overflow-x: auto;
  max-width: 100%;
}

.md-post-content pre code {
  word-break: normal;
  overflow-wrap: normal;
  white-space: pre;
}

/* ── Inline code: allow wrapping ── */
.md-post-content p code,
.md-post-content li code,
.md-post-content td code {
  word-break: break-all;
  white-space: normal;
}

/* ── Tables: horizontal scroll on small screens ── */
.md-post-content table {
  display: block;
  overflow-x: auto;
  max-width: 100%;
}
</style>
