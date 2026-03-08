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

function readingTime(content) {
  const words = content?.trim().split(/\s+/).length ?? 0
  const mins  = Math.max(1, Math.round(words / 200))
  return `${mins} min read`
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
      <h1 class="text-3xl font-bold">Blog</h1>
      <p class="text-zinc-500 dark:text-zinc-400">
        Thoughts on Python, backend development, and engineering.
      </p>
    </div>

    <div v-if="loading" class="text-sm text-zinc-400 font-mono">loading posts...</div>

    <div v-else-if="error || posts.length === 0" class="py-20 flex flex-col items-center gap-4 text-center">
      <span class="i-lucide-scroll-text w-12 h-12 text-zinc-300 dark:text-zinc-700" />
      <div class="space-y-1">
        <p class="font-mono text-sm text-zinc-500 dark:text-zinc-400">// nothing here yet</p>
        <p class="text-xs text-zinc-400 dark:text-zinc-600">Posts are on the way — check back soon.</p>
      </div>
    </div>

    <!-- Cards grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-5">
      <RouterLink
        v-for="post in posts"
        :key="post.id"
        :to="`/blog/${post.slug}`"
        class="group relative flex flex-col rounded-2xl overflow-hidden border border-zinc-200 dark:border-zinc-800 hover:border-violet-400 dark:hover:border-violet-700 transition-all duration-300 hover:shadow-xl hover:shadow-violet-500/10 hover:-translate-y-0.5"
        style="min-height: 220px"
      >
        <!-- Cover image or fallback gradient -->
        <div class="absolute inset-0">
          <img
            v-if="post.cover_image"
            :src="post.cover_image"
            :alt="post.title"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <div
            v-else
            class="w-full h-full bg-gradient-to-br from-violet-950 via-zinc-900 to-zinc-950"
          />
          <!-- Gradient overlay for readability -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-black/10" />
        </div>

        <!-- Content -->
        <div class="relative flex flex-col justify-end h-full p-5 space-y-2">
          <!-- Tags -->
          <div v-if="post.tags" class="flex flex-wrap gap-1.5">
            <span
              v-for="tag in post.tags.split(',')"
              :key="tag"
              class="text-[10px] px-2 py-0.5 rounded-full bg-violet-500/30 text-violet-200 backdrop-blur-sm border border-violet-400/20"
            >{{ tag.trim() }}</span>
          </div>

          <h2 class="font-bold text-white text-base leading-snug group-hover:text-violet-200 transition-colors">
            {{ post.title }}
          </h2>

          <p v-if="post.excerpt" class="text-xs text-zinc-300/80 line-clamp-2 leading-relaxed">
            {{ post.excerpt }}
          </p>

          <div class="flex items-center justify-between pt-1">
            <div class="flex items-center gap-2 text-xs text-zinc-400">
              <span>{{ formatDate(post.created_at) }}</span>
              <span class="text-zinc-600">·</span>
              <span class="flex items-center gap-1">
                <span class="i-lucide-clock w-3 h-3" />
                {{ readingTime(post.content) }}
              </span>
            </div>
            <span class="text-xs text-violet-300 group-hover:text-violet-200 transition-colors flex items-center gap-1">
              Read
              <span class="i-lucide-arrow-right w-3 h-3 transition-transform group-hover:translate-x-0.5" />
            </span>
          </div>
        </div>
      </RouterLink>
    </div>

  </section>
</template>
