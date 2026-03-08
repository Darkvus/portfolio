<script setup>
import { ref, onMounted, provide } from 'vue'
import NavBar from './components/NavBar.vue'
import Terminal from './components/Terminal.vue'

const isDark = ref(false)

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

provide('theme', { isDark, toggleTheme })
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 transition-colors duration-300 font-sans">
    <NavBar />
    <main class="max-w-3xl mx-auto px-6 pt-24 pb-20">
      <RouterView />
    </main>
    <Terminal />
  </div>
</template>
