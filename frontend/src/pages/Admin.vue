<script setup>
import { ref, inject, onMounted } from 'vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import {
  login, getAllPosts, createPost, updatePost, deletePost,
  getSubscribers, deleteSubscriber, uploadImage,
} from '../api/index.js'

const { isDark } = inject('theme')

// ── Auth ──────────────────────────────────────────────────────
const token      = ref(localStorage.getItem('admin_token') || '')
const loginForm  = ref({ username: '', password: '' })
const loginError = ref('')

async function handleLogin() {
  loginError.value = ''
  try {
    const data = await login(loginForm.value.username, loginForm.value.password)
    token.value = data.access_token
    localStorage.setItem('admin_token', data.access_token)
    loadPosts()
    loadSubscribers()
  } catch {
    loginError.value = 'Invalid credentials'
  }
}

function logout() {
  token.value = ''
  localStorage.removeItem('admin_token')
  posts.value = []
  subscribers.value = []
}

// ── Tabs ──────────────────────────────────────────────────────
const activeTab = ref('posts') // posts | newsletter

// ── Posts ─────────────────────────────────────────────────────
const posts      = ref([])
const showForm   = ref(false)
const editingPost = ref(null)
const formError  = ref('')
const formSuccess = ref('')

const emptyForm = () => ({
  title: '', slug: '', content: '', excerpt: '', tags: '', cover_image: '', published: false,
})

const coverPreview = ref('')
const coverUploading = ref(false)

async function onCoverChange(e) {
  const file = e.target.files[0]
  if (!file) return
  coverUploading.value = true
  try {
    const result = await uploadImage(file, token.value)
    const url = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${result.url}`
    form.value.cover_image = url
    coverPreview.value = url
  } catch (err) {
    formError.value = 'Cover upload failed: ' + err.message
  } finally {
    coverUploading.value = false
  }
}
const form = ref(emptyForm())

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

async function loadPosts() {
  try {
    posts.value = await getAllPosts(token.value)
  } catch (e) {
    if (e.message.includes('401') || e.message.includes('Unauthorized')) logout()
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
    title:       post.title,
    slug:        post.slug,
    content:     post.content,
    excerpt:     post.excerpt || '',
    tags:        post.tags || '',
    cover_image: post.cover_image || '',
    published:   post.published,
  }
  coverPreview.value = post.cover_image || ''
  showForm.value = true
  formError.value = ''
  formSuccess.value = ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function cancelForm() {
  showForm.value = false
  editingPost.value = null
  form.value = emptyForm()
  coverPreview.value = ''
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

// ── Newsletter ────────────────────────────────────────────────
const subscribers  = ref([])
const emailsCopied = ref(false)

async function copyEmails() {
  const list = subscribers.value.map(s => s.email).join(', ')
  await navigator.clipboard.writeText(list)
  emailsCopied.value = true
  setTimeout(() => { emailsCopied.value = false }, 2500)
}

async function loadSubscribers() {
  try {
    subscribers.value = await getSubscribers(token.value)
  } catch {}
}

async function removeSubscriber(id, email) {
  if (!confirm(`Remove ${email} from subscribers?`)) return
  try {
    await deleteSubscriber(id, token.value)
    await loadSubscribers()
  } catch (e) {
    alert(e.message)
  }
}

async function onUploadImg(files, callback) {
  const results = await Promise.all(
    files.map(f => uploadImage(f, token.value))
  )
  callback(results.map(r => ({ url: `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${r.url}`, alt: '' })))
}

onMounted(() => {
  if (token.value) { loadPosts(); loadSubscribers() }
})
</script>

<template>
  <section class="space-y-8">

    <!-- ── LOGIN ── -->
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
            type="text" required autocomplete="username"
            class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-violet-400 transition-colors"
          />
        </div>
        <div class="space-y-1">
          <label class="text-xs text-zinc-500 font-mono">password</label>
          <input
            v-model="loginForm.password"
            type="password" required autocomplete="current-password"
            class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-violet-400 transition-colors"
          />
        </div>
        <button type="submit" class="w-full py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors">
          Login
        </button>
        <p v-if="loginError" class="text-xs text-red-400 font-mono">// {{ loginError }}</p>
      </form>
    </div>

    <!-- ── DASHBOARD ── -->
    <div v-else class="space-y-6">

      <!-- Header -->
      <div class="flex items-center justify-between pt-6">
        <div>
          <p class="font-mono text-sm text-violet-500 select-none">$ admin panel</p>
          <h1 class="text-2xl font-bold">Dashboard</h1>
        </div>
        <div class="flex gap-2">
          <button
            v-if="activeTab === 'posts' && !showForm"
            @click="openNewForm"
            class="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors"
          >
            + New post
          </button>
          <button
            v-if="activeTab === 'posts' && showForm"
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

      <!-- Tabs — terminal style -->
      <div class="flex items-end gap-0 bg-zinc-900 dark:bg-zinc-950 rounded-t-xl px-3 pt-2 -mx-0 border border-zinc-800">
        <button
          v-for="tab in [
            { id: 'posts',      label: '📄 posts',      count: posts.length },
            { id: 'newsletter', label: '✉ newsletter',  count: subscribers.length },
          ]"
          :key="tab.id"
          @click="activeTab = tab.id; cancelForm()"
          :class="[
            'relative flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-t-lg transition-all select-none',
            activeTab === tab.id
              ? 'bg-zinc-800 text-zinc-100 border border-b-0 border-zinc-700 -mb-px pb-[9px]'
              : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50',
          ]"
        >
          {{ tab.label }}
          <span
            :class="[
              'px-1.5 py-0.5 rounded font-mono text-[10px]',
              activeTab === tab.id ? 'bg-violet-600/30 text-violet-400' : 'bg-zinc-800 text-zinc-600',
            ]"
          >{{ tab.count }}</span>
        </button>
      </div>
      <div class="-mt-px border-t border-zinc-800" />

      <!-- ── TAB: POSTS ── -->
      <div v-if="activeTab === 'posts'" class="space-y-6">

        <!-- Post form -->
        <div v-if="showForm" class="rounded-xl border border-zinc-200 dark:border-zinc-700 overflow-hidden">
          <div class="px-5 py-3 border-b border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900/50">
            <p class="font-mono text-sm text-violet-500">{{ editingPost ? '// edit post' : '// new post' }}</p>
          </div>
          <div class="p-5 space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="sm:col-span-2 space-y-1">
                <label class="text-xs text-zinc-500">Title *</label>
                <input
                  v-model="form.title"
                  type="text" placeholder="Post title"
                  class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-violet-400 transition-colors"
                />
              </div>
              <div class="space-y-1">
                <label class="text-xs text-zinc-500">Slug <span class="text-zinc-400">(auto if empty)</span></label>
                <input
                  v-model="form.slug"
                  type="text" placeholder="my-post-slug"
                  class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm font-mono text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-violet-400 transition-colors"
                />
              </div>
              <div class="space-y-1">
                <label class="text-xs text-zinc-500">Tags <span class="text-zinc-400">(comma-separated)</span></label>
                <input
                  v-model="form.tags"
                  type="text" placeholder="python, fastapi, tutorial"
                  class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-violet-400 transition-colors"
                />
              </div>
              <div class="sm:col-span-2 space-y-1">
                <label class="text-xs text-zinc-500">Excerpt</label>
                <input
                  v-model="form.excerpt"
                  type="text" placeholder="Short description..."
                  class="w-full px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-transparent text-sm text-zinc-900 dark:text-zinc-100 focus:outline-none focus:border-violet-400 transition-colors"
                />
              </div>

              <!-- Cover image -->
              <div class="sm:col-span-2 space-y-2">
                <label class="text-xs text-zinc-500">Cover image <span class="text-zinc-400">(card background)</span></label>
                <div class="flex items-center gap-3">
                  <label class="flex items-center gap-2 px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:border-violet-400 cursor-pointer text-sm text-zinc-500 dark:text-zinc-400 transition-colors">
                    <span class="i-lucide-image w-4 h-4" />
                    <span>{{ coverUploading ? 'Uploading...' : 'Upload image' }}</span>
                    <input type="file" accept="image/*" class="hidden" @change="onCoverChange" :disabled="coverUploading" />
                  </label>
                  <span v-if="form.cover_image" class="text-xs text-green-500 font-mono">✓ image set</span>
                  <button
                    v-if="form.cover_image"
                    type="button"
                    @click="form.cover_image = ''; coverPreview = ''"
                    class="text-xs text-red-400 hover:text-red-300"
                  >remove</button>
                </div>
                <div v-if="coverPreview" class="relative h-32 rounded-lg overflow-hidden border border-zinc-200 dark:border-zinc-700">
                  <img :src="coverPreview" class="w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                </div>
              </div>
            </div>

            <!-- Markdown editor -->
            <div class="space-y-1">
              <label class="text-xs text-zinc-500">Content * <span class="text-zinc-400">(Markdown)</span></label>
              <MdEditor
                v-model="form.content"
                :theme="isDark ? 'dark' : 'light'"
                language="en-US"
                preview-theme="github"
                :on-upload-img="onUploadImg"
                style="height: 500px; border-radius: 0.5rem; overflow: hidden;"
              />
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
            <p v-if="formError"   class="text-xs text-red-400 font-mono">// error: {{ formError }}</p>
            <p v-if="formSuccess" class="text-xs text-green-500 font-mono">// {{ formSuccess }}</p>
          </div>
        </div>

        <!-- Posts list -->
        <div class="space-y-2">
          <div v-if="posts.length === 0" class="py-12 text-center">
            <span class="i-lucide-file-text w-10 h-10 text-zinc-300 dark:text-zinc-700 mx-auto block mb-3" />
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
                <span :class="post.published ? 'text-green-500' : 'text-zinc-400'" class="ml-2">
                  {{ post.published ? '● published' : '○ draft' }}
                </span>
              </p>
            </div>
            <div class="flex gap-2 shrink-0">
              <button
                @click="editPost(post)"
                class="text-xs px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:border-violet-400 transition-colors"
              >Edit</button>
              <button
                @click="removePost(post.id, post.title)"
                class="text-xs px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-900/60 text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors"
              >Delete</button>
            </div>
          </div>
        </div>
      </div>

      <!-- ── TAB: NEWSLETTER ── -->
      <div v-if="activeTab === 'newsletter'" class="space-y-4">
        <div v-if="subscribers.length === 0" class="py-12 text-center">
          <span class="i-lucide-mail w-10 h-10 text-zinc-300 dark:text-zinc-700 mx-auto block mb-3" />
          <p class="font-mono text-zinc-400 text-sm">// no subscribers yet</p>
        </div>
        <div v-else class="space-y-4">
          <!-- Copy all emails button -->
          <div class="flex items-center justify-between p-4 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-800">
            <div class="space-y-0.5">
              <p class="text-sm font-medium">Copy all emails</p>
              <p class="text-xs text-zinc-400 font-mono">Comma-separated — paste in BCC field</p>
            </div>
            <button
              @click="copyEmails"
              :class="[
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all',
                emailsCopied
                  ? 'bg-green-600 text-white'
                  : 'bg-violet-600 hover:bg-violet-500 text-white',
              ]"
            >
              <span v-if="emailsCopied" class="i-lucide-check w-4 h-4" />
              <span v-else class="i-lucide-copy w-4 h-4" />
              {{ emailsCopied ? 'Copied!' : 'Copy emails' }}
            </button>
          </div>
          <div class="space-y-2">
          <div
            v-for="sub in subscribers"
            :key="sub.id"
            class="flex items-center justify-between p-3 rounded-xl border border-zinc-100 dark:border-zinc-800/60 gap-4"
          >
            <div class="min-w-0 space-y-0.5">
              <p class="text-sm truncate">{{ sub.email }}</p>
              <p class="text-xs text-zinc-400 font-mono">{{ formatDate(sub.created_at) }}</p>
            </div>
            <button
              @click="removeSubscriber(sub.id, sub.email)"
              class="text-xs px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-900/60 text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors shrink-0"
            >Remove</button>
          </div>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>
