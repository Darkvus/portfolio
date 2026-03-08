<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { subscribe } from '../api/index.js'

const { t } = useI18n()
const email   = ref('')
const status  = ref('idle') // idle | loading | success | error | duplicate
const message = ref('')

async function submit() {
  if (!email.value.trim()) return
  status.value = 'loading'
  try {
    await subscribe(email.value.trim())
    status.value = 'success'
    email.value  = ''
  } catch (e) {
    status.value = e.message.includes('409') || e.message.toLowerCase().includes('already')
      ? 'duplicate'
      : 'error'
    message.value = e.message
  }
}
</script>

<template>
  <div class="rounded-2xl border border-zinc-100 dark:border-zinc-800/60 bg-zinc-50 dark:bg-zinc-900/40 px-6 py-8 space-y-4">
    <div class="space-y-1">
      <p class="font-mono text-xs text-violet-500">{{ t('newsletter.label') }}</p>
      <h2 class="text-lg font-semibold">{{ t('newsletter.title') }}</h2>
      <p class="text-sm text-zinc-500 dark:text-zinc-400">
        {{ t('newsletter.description') }}
      </p>
    </div>

    <template v-if="status !== 'success'">
      <form @submit.prevent="submit" class="flex gap-2">
        <input
          v-model="email"
          type="email"
          required
          placeholder="you@example.com"
          :disabled="status === 'loading'"
          class="flex-1 px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:border-violet-400 transition-colors disabled:opacity-50"
        />
        <button
          type="submit"
          :disabled="status === 'loading'"
          class="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors disabled:opacity-50 shrink-0"
        >
          <span v-if="status === 'loading'" class="i-lucide-loader-circle w-4 h-4 animate-spin" />
          <span v-else>{{ t('newsletter.subscribe') }}</span>
        </button>
      </form>

      <p v-if="status === 'duplicate'" class="text-xs text-amber-400 font-mono">
        {{ t('newsletter.duplicate') }}
      </p>
      <p v-else-if="status === 'error'" class="text-xs text-red-400 font-mono">
        {{ t('newsletter.error') }}
      </p>
    </template>

    <div v-else class="flex items-center gap-2 text-sm text-green-500 font-mono">
      <span class="i-lucide-check-circle w-4 h-4" />
      {{ t('newsletter.subscribed') }}
    </div>
  </div>
</template>
