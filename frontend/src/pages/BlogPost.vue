<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { getPost } from '../api/index.js'

const route = useRoute()
const post = ref(null)
const loading = ref(true)
const notFound = ref(false)

const renderedContent = computed(() =>
  post.value ? marked.parse(post.value.content) : ''
)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

onMounted(async () => {
  try {
    post.value = await getPost(route.params.slug)
  } catch {
    notFound.value = true
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <div v-if="loading" class="pt-6 text-sm text-zinc-400 font-mono">loading...</div>

    <div v-else-if="notFound" class="pt-6 text-center py-16">
      <p class="font-mono text-zinc-400">// 404 — post not found</p>
      <RouterLink to="/blog" class="text-sm text-violet-500 hover:text-violet-400 mt-4 inline-block">
        ← Back to blog
      </RouterLink>
    </div>

    <article v-else class="space-y-8">
      <header class="space-y-4 pt-6">
        <RouterLink to="/blog" class="text-sm text-zinc-400 hover:text-violet-500 transition-colors">
          ← Blog
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
                >
                  {{ tag.trim() }}
                </span>
              </div>
            </template>
          </div>
        </div>
        <div class="border-b border-zinc-100 dark:border-zinc-800/60"></div>
      </header>

      <!-- Rendered Markdown -->
      <div
        class="prose prose-zinc dark:prose-invert prose-a:text-violet-500 prose-a:no-underline hover:prose-a:underline prose-code:text-violet-500 prose-code:bg-zinc-100 dark:prose-code:bg-zinc-800 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-pre:bg-zinc-900 prose-pre:border prose-pre:border-zinc-800 max-w-none"
        v-html="renderedContent"
      ></div>
    </article>
  </div>
</template>
