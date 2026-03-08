<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ── Terminal state ────────────────────────────────────────────
const input    = ref('')
const history  = ref([])
const inputEl  = ref(null)
const open     = ref(false)

// ── Snake game ────────────────────────────────────────────────
const COLS = 24
const ROWS = 8
const SPEED = 160 // ms per tick

const gameActive = ref(false)
const gameOver   = ref(false)
const score      = ref(0)
const snakeBody  = ref([])
const foodPos    = ref({ x: 0, y: 0 })

let dir     = { x: 1, y: 0 }
let nextDir = { x: 1, y: 0 }
let loopId  = null

const grid = computed(() => {
  const bodySet = new Set(snakeBody.value.slice(1).map(s => `${s.x},${s.y}`))
  const head    = snakeBody.value[0]
  const rows    = []
  for (let y = 0; y < ROWS; y++) {
    const row = []
    for (let x = 0; x < COLS; x++) {
      if (head?.x === x && head?.y === y) {
        row.push({ ch: '◉', cls: 'text-green-400' })
      } else if (bodySet.has(`${x},${y}`)) {
        row.push({ ch: '█', cls: 'text-green-600' })
      } else if (foodPos.value.x === x && foodPos.value.y === y) {
        row.push({ ch: '◆', cls: 'text-yellow-400' })
      } else {
        row.push({ ch: '·', cls: 'text-zinc-800' })
      }
    }
    rows.push(row)
  }
  return rows
})

function placeFood() {
  const occupied = new Set(snakeBody.value.map(s => `${s.x},${s.y}`))
  const empty = []
  for (let y = 0; y < ROWS; y++)
    for (let x = 0; x < COLS; x++)
      if (!occupied.has(`${x},${y}`)) empty.push({ x, y })
  if (empty.length)
    foodPos.value = empty[Math.floor(Math.random() * empty.length)]
}

function startSnake() {
  clearInterval(loopId)
  snakeBody.value = [{ x: 6, y: 3 }, { x: 5, y: 3 }, { x: 4, y: 3 }]
  dir     = { x: 1, y: 0 }
  nextDir = { x: 1, y: 0 }
  score.value    = 0
  gameOver.value = false
  gameActive.value = true
  placeFood()
  loopId = setInterval(tick, SPEED)
}

function tick() {
  dir = { ...nextDir }
  const head = { x: snakeBody.value[0].x + dir.x, y: snakeBody.value[0].y + dir.y }

  if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS ||
      snakeBody.value.some(s => s.x === head.x && s.y === head.y)) {
    clearInterval(loopId)
    loopId = null
    gameOver.value = true
    return
  }

  const next = [head, ...snakeBody.value]
  if (head.x === foodPos.value.x && head.y === foodPos.value.y) {
    score.value++
    placeFood()
  } else {
    next.pop()
  }
  snakeBody.value = next
}

function stopGame() {
  clearInterval(loopId)
  loopId = null
  gameActive.value = false
  gameOver.value   = false
}

// ── Keyboard handler ──────────────────────────────────────────
function onKeydown(e) {
  if (!gameActive.value) return

  const map = {
    ArrowUp:    { x: 0, y: -1 }, w: { x: 0, y: -1 }, W: { x: 0, y: -1 },
    ArrowDown:  { x: 0, y:  1 }, s: { x: 0, y:  1 }, S: { x: 0, y:  1 },
    ArrowLeft:  { x: -1, y: 0 }, a: { x: -1, y: 0 }, A: { x: -1, y: 0 },
    ArrowRight: { x:  1, y: 0 }, d: { x:  1, y: 0 }, D: { x:  1, y: 0 },
  }
  const nd = map[e.key]
  if (nd) {
    if (!(nd.x === -dir.x && nd.y === -dir.y)) nextDir = nd
    e.preventDefault()
  }
  if (e.key === 'Escape') stopGame()
  if ((e.key === 'r' || e.key === 'R') && gameOver.value) startSnake()
}

watch(open, val => {
  if (val) {
    document.addEventListener('keydown', onKeydown)
    nextTick(() => inputEl.value?.focus())
  } else {
    document.removeEventListener('keydown', onKeydown)
    stopGame()
  }
})

onUnmounted(() => {
  stopGame()
  document.removeEventListener('keydown', onKeydown)
})

// ── Navigation commands ───────────────────────────────────────
const routes = {
  home: '/', '/': '/', '~': '/',
  blog: '/blog',
  about: '/about',
}

const helpLines = [
  '  cd <page>  — navigate: home · blog · about',
  '  ls         — list pages',
  '  snake      — play snake 🐍',
  '  clear      — clear terminal',
  '  help       — show this message',
]

function run() {
  const raw = input.value.trim()
  if (!raw) return
  const [cmd, arg] = raw.split(/\s+/)

  history.value.push({ type: 'cmd', text: raw })

  switch (cmd.toLowerCase()) {
    case 'clear':
      history.value = []
      break
    case 'help':
      history.value.push(...helpLines.map(t => ({ type: 'out', text: t })))
      break
    case 'ls':
      history.value.push({ type: 'out', text: '  home   blog   about' })
      break
    case 'snake':
      startSnake()
      break
    case 'cd': {
      const dest = routes[arg?.toLowerCase() ?? '']
      if (dest !== undefined) {
        history.value.push({ type: 'ok', text: `→ ${arg ?? 'home'}` })
        router.push(dest)
        open.value = false
      } else {
        history.value.push({ type: 'err', text: `bash: cd: ${arg}: No such page` })
      }
      break
    }
    default:
      history.value.push({ type: 'err', text: `bash: ${cmd}: command not found` })
  }

  input.value = ''
  nextTick(() => {
    const el = inputEl.value?.closest('.t-body')
    if (el) el.scrollTop = el.scrollHeight
  })
}
</script>

<template>
  <!-- Toggle button -->
  <button
    @click="open = !open"
    class="fixed bottom-5 right-5 z-50 w-10 h-10 flex items-center justify-center rounded-xl bg-zinc-900 dark:bg-zinc-100 text-zinc-100 dark:text-zinc-900 shadow-lg hover:opacity-80 transition-opacity"
    title="Terminal"
  >
    <span class="i-lucide-terminal w-5 h-5" />
  </button>

  <!-- Window -->
  <Transition name="slide">
    <div
      v-if="open"
      class="fixed bottom-18 right-5 z-50 w-80 sm:w-96 rounded-xl overflow-hidden shadow-2xl border border-zinc-800 bg-zinc-950 text-zinc-100 font-mono text-xs select-none"
    >
      <!-- Title bar -->
      <div class="flex items-center gap-1.5 px-3 py-2 bg-zinc-900 border-b border-zinc-800">
        <span class="w-2.5 h-2.5 rounded-full bg-red-500 cursor-pointer" @click="open = false" />
        <span class="w-2.5 h-2.5 rounded-full bg-yellow-500" />
        <span class="w-2.5 h-2.5 rounded-full bg-green-500" />
        <span class="ml-auto text-zinc-500 text-[10px]">darkvus@portfolio</span>
      </div>

      <!-- Body -->
      <div class="t-body h-52 overflow-y-auto px-3 py-2">

        <!-- ── SNAKE GAME ── -->
        <template v-if="gameActive">
          <div class="flex justify-between text-[10px] mb-1">
            <span class="text-green-400 font-bold">🐍 SNAKE</span>
            <span class="text-zinc-400">score <span class="text-yellow-400 font-bold">{{ score }}</span></span>
          </div>

          <div class="text-zinc-700 leading-none">┌{{ '─'.repeat(COLS) }}┐</div>
          <div v-for="(row, y) in grid" :key="y" class="leading-none">
            <span class="text-zinc-700">│</span>
            <span v-for="(cell, x) in row" :key="x" :class="cell.cls">{{ cell.ch }}</span>
            <span class="text-zinc-700">│</span>
          </div>
          <div class="text-zinc-700 leading-none">└{{ '─'.repeat(COLS) }}┘</div>

          <div v-if="!gameOver" class="text-zinc-600 text-[10px] mt-1 text-center">
            WASD / ↑↓←→ &nbsp;·&nbsp; ESC to exit
          </div>
          <div v-else class="mt-1 text-center space-x-1 text-[10px]">
            <span class="text-red-400 font-bold">GAME OVER</span>
            <span class="text-zinc-500">·</span>
            <span class="text-zinc-400">score <span class="text-yellow-400">{{ score }}</span></span>
            <span class="text-zinc-500">·</span>
            <span class="text-violet-400 cursor-pointer" @click="startSnake">[ R ] restart</span>
            <span class="text-zinc-500">·</span>
            <span class="text-zinc-500 cursor-pointer" @click="stopGame">[ ESC ] exit</span>
          </div>
        </template>

        <!-- ── HISTORY ── -->
        <template v-else>
          <div v-if="history.length === 0" class="text-zinc-600">
            Type <span class="text-violet-400">help</span> to get started.
          </div>
          <div
            v-for="(line, i) in history"
            :key="i"
            :class="{
              'text-zinc-300': line.type === 'cmd',
              'text-zinc-500': line.type === 'out',
              'text-violet-400': line.type === 'ok',
              'text-red-400':  line.type === 'err',
            }"
          >
            <span v-if="line.type === 'cmd'" class="text-violet-500 mr-1">$</span>{{ line.text }}
          </div>
        </template>

      </div>

      <!-- Input (hidden during game) -->
      <div v-if="!gameActive" class="flex items-center gap-2 px-3 py-2 border-t border-zinc-800 bg-zinc-950">
        <span class="text-violet-500 shrink-0">$</span>
        <input
          ref="inputEl"
          v-model="input"
          @keydown.enter="run"
          @keydown.escape="open = false"
          class="flex-1 bg-transparent outline-none caret-violet-400 text-zinc-100 placeholder-zinc-700"
          placeholder="help"
          autocomplete="off"
          spellcheck="false"
        />
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.slide-enter-from, .slide-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
