<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '../api/index.js'

const posts = ref([])
const loading = ref(true)
const error = ref(null)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

onMounted(async () => {
  try {
    posts.value = await getPosts()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="space-y-10">

    <div class="space-y-2 pt-6">
      <p class="font-mono text-sm text-violet-500 select-none">$ ls ./blog</p>
      <h1 class="text-3xl font-bold">Blog</h1>
      <p class="text-zinc-500 dark:text-zinc-400">
        Thoughts on Python, backend development, and engineering.
      </p>
    </div>

    <div v-if="loading" class="text-sm text-zinc-400 font-mono">loading posts...</div>

    <div v-else-if="error" class="text-sm text-red-400 font-mono">// error: {{ error }}</div>

    <div v-else-if="posts.length === 0" class="py-16 text-center">
      <p class="font-mono text-zinc-400 text-sm">// no posts yet</p>
      <p class="text-zinc-400 text-xs mt-2">Come back soon!</p>
    </div>

    <div v-else class="space-y-3">
      <RouterLink
        v-for="post in posts"
        :key="post.id"
        :to="`/blog/${post.slug}`"
        class="block p-5 rounded-xl border border-zinc-100 dark:border-zinc-800/60 hover:border-violet-200 dark:hover:border-violet-800/60 hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-all group"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="space-y-1.5 min-w-0">
            <h2 class="font-semibold group-hover:text-violet-500 transition-colors">
              {{ post.title }}
            </h2>
            <p v-if="post.excerpt" class="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2">
              {{ post.excerpt }}
            </p>
            <div v-if="post.tags" class="flex flex-wrap gap-1.5 pt-0.5">
              <span
                v-for="tag in post.tags.split(',')"
                :key="tag"
                class="text-xs px-2 py-0.5 rounded-full bg-violet-50 dark:bg-violet-950/60 text-violet-600 dark:text-violet-400"
              >
                {{ tag.trim() }}
              </span>
            </div>
          </div>
          <span class="text-xs text-zinc-400 shrink-0 mt-0.5">{{ formatDate(post.created_at) }}</span>
        </div>
      </RouterLink>
    </div>

  </section>
</template>
