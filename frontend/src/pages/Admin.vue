<script setup>
import { ref, onMounted } from 'vue'
import { login, getAllPosts, createPost, updatePost, deletePost } from '../api/index.js'

const token = ref(localStorage.getItem('admin_token') || '')
const loginForm = ref({ username: '', password: '' })
const loginError = ref('')
const posts = ref([])
const showForm = ref(false)
const editingPost = ref(null)
const formError = ref('')
const formSuccess = ref('')

const emptyForm = () => ({
  title: '', slug: '', content: '', excerpt: '', tags: '', published: false,
})
const form = ref(emptyForm())

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

async function handleLogin() {
  loginError.value = ''
  try {
    const data = await login(loginForm.value.username, loginForm.value.password)
    token.value = data.access_token
    localStorage.setItem('admin_token', data.access_token)
    await loadPosts()
  } catch {
    loginError.value = 'Invalid credentials'
  }
}

function logout() {
  token.value = ''
  localStorage.removeItem('admin_token')
  posts.value = []
}

async function loadPosts() {
  try {
    posts.value = await getAllPosts(token.value)
  } catch (e) {
    if (e.message.includes('401') || e.message.includes('Unauthorized')) {
      logout()
    }
  }
}

function openNewForm() {
  editingPost.value = null
  form.value = emptyForm()
  showForm.value = true
  formError.value = ''
  formSuccess.value = ''
}

function editPost(post) {
  editingPost.value = post
  form.value = {
    title: post.title,
    slug: post.slug,
    content: post.content,
    excerpt: post.excerpt || '',
    tags: post.tags || '',
    published: post.published,
  }
  showForm.value = true
  formError.value = ''
  formSuccess.value = ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function cancelForm() {
  showForm.value = false
  editingPost.value = null
  form.value = emptyForm()
}

async function submitPost() {
  formError.value = ''
  formSuccess.value = ''
  if (!form.value.title || !form.value.content) {
    formError.value = 'Title and content are required'
    return
  }
  try {
    if (editingPost.value) {
      await updatePost(editingPost.value.id, form.value, token.value)
      formSuccess.value = 'Post updated!'
    } else {
      await createPost(form.value, token.value)
      formSuccess.value = 'Post created!'
    }
    await loadPosts()
    setTimeout(cancelForm, 1200)
  } catch (e) {
    formError.value = e.message
  }
}

async function removePost(id, title) {
  if (!confirm(`Delete "${title}"? This cannot be undone.`)) return
  try {
    await deletePost(id, token.value)
    await loadPosts()
  } catch (e) {
    alert(e.message)
  }
}

onMounted(() => {
  if (token.value) loadPosts()
})
</script>

<template>
  <section class="space-y-8">

    <!-- LOGIN -->
    <div v-if="!token" class="max-w-sm space-y-6 pt-6">
      <div class="space-y-2">
        <p class="font-mono text-sm text-violet-500 select-none">$ sudo login</p>
        <h1 class="text-2xl font-bold">Admin</h1>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div class="space-y-1">
          <label class="text-xs text-zinc-500 font-mono">username</label>
          <input
            v-model="loginForm.username"
            type="text"
            required
            autocomplete="username"
            class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm focus:outline-none focus:border-violet-400 transition-colors"
          />
        </div>
        <div class="space-y-1">
          <label class="text-xs text-zinc-500 font-mono">password</label>
          <input
            v-model="loginForm.password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm focus:outline-none focus:border-violet-400 transition-colors"
          />
        </div>
        <button
          type="submit"
          class="w-full py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors"
        >
          Login
        </button>
        <p v-if="loginError" class="text-xs text-red-400 font-mono">// {{ loginError }}</p>
      </form>
    </div>

    <!-- DASHBOARD -->
    <div v-else class="space-y-8">

      <!-- Header -->
      <div class="flex items-center justify-between pt-6">
        <div>
          <p class="font-mono text-sm text-violet-500 select-none">$ admin panel</p>
          <h1 class="text-2xl font-bold">Posts</h1>
        </div>
        <div class="flex gap-3">
          <button
            v-if="!showForm"
            @click="openNewForm"
            class="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors"
          >
            + New post
          </button>
          <button
            v-else
            @click="cancelForm"
            class="px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sm hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="logout"
            class="px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sm hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      <!-- Post Form -->
      <div
        v-if="showForm"
        class="p-5 rounded-xl border border-zinc-200 dark:border-zinc-700 space-y-4"
      >
        <h2 class="font-semibold text-sm font-mono text-violet-500">
          {{ editingPost ? '// edit post' : '// new post' }}
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="sm:col-span-2 space-y-1">
            <label class="text-xs text-zinc-500">Title *</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="Post title"
              class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm focus:outline-none focus:border-violet-400 transition-colors"
            />
          </div>
          <div class="space-y-1">
            <label class="text-xs text-zinc-500">Slug <span class="text-zinc-400">(auto if empty)</span></label>
            <input
              v-model="form.slug"
              type="text"
              placeholder="my-post-slug"
              class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm font-mono focus:outline-none focus:border-violet-400 transition-colors"
            />
          </div>
          <div class="space-y-1">
            <label class="text-xs text-zinc-500">Tags <span class="text-zinc-400">(comma-separated)</span></label>
            <input
              v-model="form.tags"
              type="text"
              placeholder="python, fastapi, tutorial"
              class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm focus:outline-none focus:border-violet-400 transition-colors"
            />
          </div>
          <div class="sm:col-span-2 space-y-1">
            <label class="text-xs text-zinc-500">Excerpt</label>
            <input
              v-model="form.excerpt"
              type="text"
              placeholder="Short description..."
              class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm focus:outline-none focus:border-violet-400 transition-colors"
            />
          </div>
          <div class="sm:col-span-2 space-y-1">
            <label class="text-xs text-zinc-500">Content * <span class="text-zinc-400">(Markdown)</span></label>
            <textarea
              v-model="form.content"
              rows="14"
              placeholder="# My Post&#10;&#10;Write your content in **Markdown**..."
              class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm font-mono leading-relaxed focus:outline-none focus:border-violet-400 transition-colors resize-y"
            ></textarea>
          </div>
        </div>
        <div class="flex items-center justify-between pt-1">
          <label class="flex items-center gap-2 text-sm cursor-pointer">
            <input v-model="form.published" type="checkbox" class="accent-violet-500 w-4 h-4" />
            <span class="text-zinc-600 dark:text-zinc-400">Publish immediately</span>
          </label>
          <button
            @click="submitPost"
            class="px-5 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors"
          >
            {{ editingPost ? 'Update' : 'Publish' }}
          </button>
        </div>
        <p v-if="formError" class="text-xs text-red-400 font-mono">// error: {{ formError }}</p>
        <p v-if="formSuccess" class="text-xs text-green-500 font-mono">// {{ formSuccess }}</p>
      </div>

      <!-- Posts list -->
      <div class="space-y-2">
        <div v-if="posts.length === 0" class="py-8 text-center">
          <p class="font-mono text-zinc-400 text-sm">// no posts yet — create your first one!</p>
        </div>
        <div
          v-for="post in posts"
          :key="post.id"
          class="flex items-center justify-between p-4 rounded-xl border border-zinc-100 dark:border-zinc-800/60 gap-4"
        >
          <div class="min-w-0 space-y-0.5">
            <p class="font-medium text-sm truncate">{{ post.title }}</p>
            <p class="text-xs text-zinc-400 font-mono">
              {{ formatDate(post.created_at) }}
              <span
                :class="post.published ? 'text-green-500' : 'text-zinc-400'"
                class="ml-2"
              >
                {{ post.published ? '● published' : '○ draft' }}
              </span>
            </p>
          </div>
          <div class="flex gap-2 shrink-0">
            <button
              @click="editPost(post)"
              class="text-xs px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:border-violet-400 transition-colors"
            >
              Edit
            </button>
            <button
              @click="removePost(post.id, post.title)"
              class="text-xs px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-900/60 text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>
