<script setup>
import { ref, computed, watch, inject, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route  = useRoute()
const { isDark, toggleTheme } = inject('theme')

// ── Terminal state ────────────────────────────────────────────
const input   = ref('')
const history = ref([])
const inputEl = ref(null)
const open    = ref(false)

// ── Cookie consent ────────────────────────────────────────────
const cookiePending = ref(false)

const cookieLines = [
  { type: 'banner', text: '╔══════════════════════════════════════╗' },
  { type: 'banner', text: '║         cookies.consent v1.0         ║' },
  { type: 'banner', text: '╚══════════════════════════════════════╝' },
  { type: 'out',    text: '' },
  { type: 'out',    text: 'This site uses essential cookies only:' },
  { type: 'out',    text: '  · theme preference  (localStorage)' },
  { type: 'out',    text: '  · no tracking · no third parties' },
  { type: 'out',    text: '' },
  { type: 'cookie', text: '' },
]

function showCookiePrompt() { history.value = [...cookieLines] }

function acceptCookies() {
  localStorage.setItem('cookies_accepted', '1')
  cookiePending.value = false
  history.value = history.value.filter(l => l.type !== 'cookie')
  history.value.push({ type: 'ok', text: '✓ cookies accepted' })
  history.value.push({ type: 'out', text: '' })
  history.value.push(...helpLines.map(t => ({ type: 'out', text: t })))
  nextTick(scrollBottom)
}

function declineCookies() {
  localStorage.setItem('cookies_accepted', '0')
  cookiePending.value = false
  history.value = history.value.filter(l => l.type !== 'cookie')
  history.value.push({ type: 'err', text: '✗ cookies declined' })
  history.value.push({ type: 'out', text: '' })
  history.value.push({ type: 'out', text: 'Type help to get started.' })
  nextTick(scrollBottom)
}

const sessionStart = Date.now()

onMounted(() => {
  if (!localStorage.getItem('cookies_accepted')) {
    cookiePending.value = true
    open.value = true
    nextTick(() => showCookiePrompt())
  }
})

// ── Snake ─────────────────────────────────────────────────────
const COLS = 24, ROWS = 8, SPEED = 160
const gameActive = ref(false)
const gameOver   = ref(false)
const score      = ref(0)
const snakeBody  = ref([])
const foodPos    = ref({ x: 0, y: 0 })
let dir = { x: 1, y: 0 }, nextDir = { x: 1, y: 0 }, loopId = null

const grid = computed(() => {
  const bodySet = new Set(snakeBody.value.slice(1).map(s => `${s.x},${s.y}`))
  const head    = snakeBody.value[0]
  return Array.from({ length: ROWS }, (_, y) =>
    Array.from({ length: COLS }, (_, x) => {
      if (head?.x === x && head?.y === y)          return { ch: '◉', cls: 'text-green-400' }
      if (bodySet.has(`${x},${y}`))                return { ch: '█', cls: 'text-green-600' }
      if (foodPos.value.x === x && foodPos.value.y === y) return { ch: '◆', cls: 'text-yellow-400' }
      return { ch: '·', cls: 'text-zinc-800' }
    })
  )
})

function placeFood() {
  const occupied = new Set(snakeBody.value.map(s => `${s.x},${s.y}`))
  const empty = []
  for (let y = 0; y < ROWS; y++)
    for (let x = 0; x < COLS; x++)
      if (!occupied.has(`${x},${y}`)) empty.push({ x, y })
  if (empty.length) foodPos.value = empty[Math.floor(Math.random() * empty.length)]
}

function startSnake() {
  clearInterval(loopId)
  snakeBody.value  = [{ x: 6, y: 3 }, { x: 5, y: 3 }, { x: 4, y: 3 }]
  dir = nextDir   = { x: 1, y: 0 }
  score.value     = 0
  gameOver.value  = false
  gameActive.value = true
  stopMatrix()
  placeFood()
  loopId = setInterval(tick, SPEED)
}

function tick() {
  dir = { ...nextDir }
  const head = { x: snakeBody.value[0].x + dir.x, y: snakeBody.value[0].y + dir.y }
  if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS ||
      snakeBody.value.some(s => s.x === head.x && s.y === head.y)) {
    clearInterval(loopId); loopId = null; gameOver.value = true; return
  }
  const next = [head, ...snakeBody.value]
  if (head.x === foodPos.value.x && head.y === foodPos.value.y) { score.value++; placeFood() }
  else next.pop()
  snakeBody.value = next
}

function stopGame() {
  clearInterval(loopId); loopId = null
  gameActive.value = false; gameOver.value = false
}

// ── Matrix ────────────────────────────────────────────────────
const MAT_COLS = 32, MAT_ROWS = 10
const CHARS = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜabcdefghijklmnñopqrstuvwxyzáéíóúü0123456789¿¡€@#'
const matrixActive = ref(false)
const matrixGrid   = ref([])
let matDrops = [], matId = null

function startMatrix() {
  stopGame()
  matrixActive.value = true
  matDrops = Array.from({ length: MAT_COLS }, () => Math.floor(Math.random() * MAT_ROWS))
  matrixGrid.value   = Array.from({ length: MAT_ROWS }, () =>
    Array.from({ length: MAT_COLS }, () => ({ ch: ' ', head: false }))
  )
  matId = setInterval(tickMatrix, 80)
}

function tickMatrix() {
  const g = matrixGrid.value.map(r => r.map(c => ({ ...c, head: false })))
  matDrops = matDrops.map((row, col) => {
    const ch = CHARS[Math.floor(Math.random() * CHARS.length)]
    if (row < MAT_ROWS) { g[row][col] = { ch, head: true } }
    const next = row + 1
    return next > MAT_ROWS + Math.floor(Math.random() * 4) ? 0 : next
  })
  matrixGrid.value = g
}

function stopMatrix() {
  clearInterval(matId); matId = null
  matrixActive.value = false
}

// ── Keyboard ──────────────────────────────────────────────────
function onKeydown(e) {
  if (matrixActive.value) {
    if (e.key === 'Escape') stopMatrix()
    return
  }
  if (progressActive.value) {
    if (e.key === 'Escape') stopProgress()
    return
  }
  if (!gameActive.value) return
  const map = {
    ArrowUp: {x:0,y:-1}, w:{x:0,y:-1}, W:{x:0,y:-1},
    ArrowDown: {x:0,y:1}, s:{x:0,y:1}, S:{x:0,y:1},
    ArrowLeft: {x:-1,y:0}, a:{x:-1,y:0}, A:{x:-1,y:0},
    ArrowRight: {x:1,y:0}, d:{x:1,y:0}, D:{x:1,y:0},
  }
  const nd = map[e.key]
  if (nd) { if (!(nd.x === -dir.x && nd.y === -dir.y)) nextDir = nd; e.preventDefault() }
  if (e.key === 'Escape') stopGame()
  if ((e.key === 'r' || e.key === 'R') && gameOver.value) startSnake()
}

watch(open, val => {
  if (val) { document.addEventListener('keydown', onKeydown); nextTick(() => inputEl.value?.focus()) }
  else     { document.removeEventListener('keydown', onKeydown); stopGame(); stopMatrix(); stopProgress() }
})
onUnmounted(() => { stopGame(); stopMatrix(); stopProgress(); document.removeEventListener('keydown', onKeydown) })

// ── Commands ──────────────────────────────────────────────────
const routes = { home: '/', '/': '/', '~': '/', blog: '/blog', about: '/about' }

const helpLines = [
  '  Navigation',
  '  ─────────────────────────────────────',
  '  cd <page>         navigate: home · blog · about',
  '  ls                list pages',
  '  pwd               current path',
  '  ',
  '  Portfolio',
  '  ─────────────────────────────────────',
  '  whoami            who is darkvus?',
  '  skills            tech stack',
  '  social            links & contacts',
  '  neofetch          system info',
  '  projects          project list',
  '  blog              published posts',
  '  cv / resume       download CV (PDF)',
  '  contact           open email client',
  '  ',
  '  Utilities',
  '  ─────────────────────────────────────',
  '  date              current date & time',
  '  uptime            session duration',
  '  weather           local weather (GPS)',
  '  calc <expr>       calculator  (2+2, Math.PI)',
  '  base64 [-d] <x>   encode / decode base64',
  '  joke              random dev joke',
  '  ',
  '  Actions',
  '  ─────────────────────────────────────',
  '  open <site>       open github · linkedin',
  '  theme             toggle dark / light mode',
  '  echo <text>       print text',
  '  ',
  '  Visuals',
  '  ─────────────────────────────────────',
  '  ascii <text>      pixel font art',
  '  banner <text>     boxed banner',
  '  cowsay <text>     moo',
  '  color             theme palette',
  '  progress          skill bars',
  '  ',
  '  Fun',
  '  ─────────────────────────────────────',
  '  snake             play snake 🐍',
  '  matrix            enter the matrix',
  '  ping              ...',
  '  sudo              ...',
  '  ',
  '  history           command history',
  '  clear             clear terminal',
  '  help              show this message',
]

const whoamiLines = [
  '  Alejandro Caraballo',
  '  ─────────────────────────────────────',
  '  Role     Backend Developer',
  '  Based    Spain 🇪🇸',
  '  Focus    Python · FastAPI · Django',
  '           scalable systems & microservices',
  '  Open to  remote opportunities',
  '  ',
  '  Currently building pyms-django-chassis',
  '  and this portfolio ← you are here',
]

const skillsLines = [
  '  Backend',
  '  ─────────────────────────────────────',
  '  Python · FastAPI · Django · SQLAlchemy',
  '  PostgreSQL · SQLite · Turso (libSQL)',
  '  REST APIs · DDD · Microservices',
  '  ',
  '  Frontend',
  '  ─────────────────────────────────────',
  '  Vue 3 · Vite · UnoCSS · TypeScript',
  '  ',
  '  Infrastructure',
  '  ─────────────────────────────────────',
  '  Docker · Render · Fly.io · AWS',
  '  OpenTelemetry · GitHub Actions',
  '  ',
  '  Tools',
  '  ─────────────────────────────────────',
  '  Git · uv · Ruff · pytest · Pydantic',
]

const socialLines = [
  '  GitHub    github.com/Darkvus',
  '  LinkedIn  linkedin.com/in/alejandro-jose-c-66010aa1',
  '  ',
  '  → open github    to visit GitHub',
  '  → open linkedin  to visit LinkedIn',
]

const neofetchLines = [
  '  ██████╗  ╔═══════════════════════════════╗',
  '  ██╔══██╗ ║ darkvus @ portfolio            ║',
  '  ██║  ██║ ╠═══════════════════════════════╣',
  '  ██║  ██║ ║ OS      Portfolio v1.0         ║',
  '  ██████╔╝ ║ Shell   terminal (custom)      ║',
  '  ╚═════╝  ║ Role    Backend Developer      ║',
  '           ║ Based   Spain 🇪🇸              ║',
  '           ║ Lang    Python · JS · SQL      ║',
  '           ║ Stack   FastAPI · Django · Vue ║',
  '           ║ GitHub  github.com/Darkvus     ║',
  '           ╚═══════════════════════════════╝',
]

const openTargets = {
  github:   'https://github.com/Darkvus',
  linkedin: 'https://www.linkedin.com/in/alejandro-jose-c-66010aa1/',
}

// ── Projects ──────────────────────────────────────────────────
async function fetchProjects() {
  push({ type: 'out', text: '  fetching repos...' })
  try {
    const repos = await fetch(
      'https://api.github.com/users/Darkvus/repos?sort=updated&per_page=10&type=public'
    ).then(r => r.json())
    if (!Array.isArray(repos) || !repos.length) { push({ type: 'out', text: '  no public repos' }); return }
    push({ type: 'out', text: '' })
    for (const r of repos) {
      push(
        { type: 'ok',  text: `  ${r.name}` },
        { type: 'out', text: `  ${r.description ?? '(no description)'}` },
        { type: 'out', text: `  ★ ${r.stargazers_count}  ${r.language ?? ''}  github.com/Darkvus/${r.name}` },
        { type: 'out', text: '' },
      )
    }
  } catch {
    push({ type: 'err', text: '  could not reach GitHub API' })
  }
}

// ── Pixel font (5×3) ──────────────────────────────────────────
const PIXEL_FONT = {
  ' ': ['   ','   ','   ','   ','   '],
  'A': [' █ ','█ █','███','█ █','█ █'],
  'B': ['██ ','█ █','██ ','█ █','██ '],
  'C': [' ██','█  ','█  ','█  ',' ██'],
  'D': ['██ ','█ █','█ █','█ █','██ '],
  'E': ['███','█  ','██ ','█  ','███'],
  'F': ['███','█  ','██ ','█  ','█  '],
  'G': [' ██','█  ','█ █','█ █',' ██'],
  'H': ['█ █','█ █','███','█ █','█ █'],
  'I': ['███',' █ ',' █ ',' █ ','███'],
  'J': [' ██','  █','  █','█ █',' █ '],
  'K': ['█ █','█▄ ','██ ','█ █','█ █'],
  'L': ['█  ','█  ','█  ','█  ','███'],
  'M': ['█ █','███','█ █','█ █','█ █'],
  'N': ['█ █','██ ','█ █','█ █','█ █'],
  'O': [' █ ','█ █','█ █','█ █',' █ '],
  'P': ['██ ','█ █','██ ','█  ','█  '],
  'Q': [' █ ','█ █','█ █','█▄█',' ██'],
  'R': ['██ ','█ █','██ ','█▄ ','█ █'],
  'S': [' ██','█  ',' █ ','  █','██ '],
  'T': ['███',' █ ',' █ ',' █ ',' █ '],
  'U': ['█ █','█ █','█ █','█ █',' █ '],
  'V': ['█ █','█ █','█ █',' █ ',' █ '],
  'W': ['█ █','█ █','█▄█','███','█ █'],
  'X': ['█ █','█ █',' █ ','█ █','█ █'],
  'Y': ['█ █','█ █',' █ ',' █ ',' █ '],
  'Z': ['███','  █',' █ ','█  ','███'],
  '0': [' █ ','█ █','█ █','█ █',' █ '],
  '1': [' █ ','██ ',' █ ',' █ ','███'],
  '2': ['██ ','  █',' ██','█  ','███'],
  '3': ['██ ','  █','██ ','  █','██ '],
  '4': ['█ █','█ █','███','  █','  █'],
  '5': ['███','█  ','██ ','  █','██ '],
  '6': [' ██','█  ','██ ','█ █',' █ '],
  '7': ['███','  █',' █ ',' █ ',' █ '],
  '8': [' █ ','█ █',' █ ','█ █',' █ '],
  '9': [' █ ','█ █',' ██','  █',' █ '],
  '!': [' █ ',' █ ',' █ ','   ',' █ '],
  '?': ['██ ','  █',' █ ','   ',' █ '],
  '.': ['   ','   ','   ','   ',' █ '],
  '-': ['   ','   ','███','   ','   '],
  '_': ['   ','   ','   ','   ','███'],
}

function asciiRender(text) {
  const chars = text.toUpperCase().split('').map(c => PIXEL_FONT[c] ?? PIXEL_FONT[' '])
  return Array.from({ length: 5 }, (_, row) =>
    '  ' + chars.map(c => c[row]).join(' ')
  )
}

// ── Cowsay ────────────────────────────────────────────────────
function cowsay(text) {
  const w   = Math.min(text.length, 30)
  const top = ` ${'_'.repeat(w + 2)}`
  const mid = `< ${text.slice(0, w)} >`
  const bot = ` ${'‾'.repeat(w + 2)}`
  return [
    top, mid, bot,
    '        \\',
    '         \\   ^__^',
    '          \\  (oo)\\_______',
    '             (__)\\       )\\/\\',
    '                 ||----w |',
    '                 ||     ||',
  ]
}

// ── Calc ──────────────────────────────────────────────────────
function safeCalc(expr) {
  try {
    const sanitized = expr.replace(/\^/g, '**')
    // only allow math-safe chars
    if (/[^0-9+\-*/.()% ,eE\s]/.test(sanitized.replace(/Math\.\w+/g, '0'))) {
      return 'unsafe expression'
    }
    const fn = new Function('Math', `"use strict"; return (${sanitized})`)
    const result = fn(Math)
    return String(result)
  } catch {
    return 'syntax error'
  }
}

// ── Base64 ────────────────────────────────────────────────────
function base64Cmd(arg, flag) {
  if (flag === '-d' || flag === '--decode') {
    try { return ['  ' + atob(arg)] }
    catch { return ['  error: invalid base64 string'] }
  }
  try { return ['  ' + btoa(unescape(encodeURIComponent(arg)))] }
  catch { return ['  error: could not encode'] }
}

// ── Weather codes ─────────────────────────────────────────────
const WMO = {
  0:'☀️  Clear sky', 1:'🌤️  Mainly clear', 2:'⛅ Partly cloudy', 3:'☁️  Overcast',
  45:'🌫️  Fog', 48:'🌫️  Icy fog',
  51:'🌦️  Light drizzle', 53:'🌦️  Drizzle', 55:'🌧️  Heavy drizzle',
  61:'🌧️  Light rain', 63:'🌧️  Rain', 65:'🌧️  Heavy rain',
  71:'🌨️  Light snow', 73:'❄️  Snow', 75:'❄️  Heavy snow',
  80:'🌦️  Rain showers', 81:'🌧️  Showers', 82:'⛈️  Violent showers',
  95:'⛈️  Thunderstorm', 96:'⛈️  Thunderstorm + hail', 99:'⛈️  Heavy thunderstorm',
}

async function fetchWeather() {
  push({ type: 'out', text: '  locating...' })
  try {
    const pos = await new Promise((res, rej) =>
      navigator.geolocation.getCurrentPosition(res, rej, { timeout: 8000 })
    )
    const { latitude: lat, longitude: lon } = pos.coords
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat.toFixed(4)}&longitude=${lon.toFixed(4)}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m&forecast_days=1`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`API error ${res.status}`)
    const data = await res.json()
    const cur  = data.current_weather
    if (!cur) throw new Error('no data from Open-Meteo')
    const desc = WMO[cur.weathercode] ?? '🌡️  Unknown'
    push(
      { type: 'out', text: '' },
      { type: 'out', text: `  ${desc}` },
      { type: 'out', text: `  Temp   ${cur.temperature} °C` },
      { type: 'out', text: `  Wind   ${cur.windspeed} km/h` },
      { type: 'out', text: `  Coords ${lat.toFixed(2)}, ${lon.toFixed(2)}` },
    )
  } catch (e) {
    push({ type: 'err', text: `  weather: ${e.message ?? 'geolocation denied'}` })
  }
}

// ── Joke ──────────────────────────────────────────────────────
async function fetchJoke() {
  push({ type: 'out', text: '  fetching joke...' })
  try {
    const data = await fetch('https://v2.jokeapi.dev/joke/Programming?type=single&lang=en').then(r => r.json())
    push({ type: 'out', text: `  ${data.joke}` })
  } catch {
    push({ type: 'err', text: '  could not fetch joke' })
  }
}

// ── Blog fetch ────────────────────────────────────────────────
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function fetchBlogPosts() {
  push({ type: 'out', text: '  loading posts...' })
  try {
    const posts = await fetch(`${API_BASE}/posts/`).then(r => r.json())
    if (!posts.length) { push({ type: 'out', text: '  no posts yet' }); return }
    push({ type: 'out', text: '' })
    for (const p of posts) {
      push(
        { type: 'ok',  text: `  ${p.title}` },
        { type: 'out', text: `  /blog/${p.slug}` },
        { type: 'out', text: '' },
      )
    }
  } catch {
    push({ type: 'err', text: '  could not reach API' })
  }
}

// ── Progress bars ─────────────────────────────────────────────
const progressActive = ref(false)
const SKILL_BARS = [
  { label: 'Python  ', target: 90 },
  { label: 'FastAPI ', target: 85 },
  { label: 'Django  ', target: 80 },
  { label: 'Vue 3   ', target: 65 },
  { label: 'Docker  ', target: 70 },
  { label: 'AWS     ', target: 55 },
  { label: 'SQL     ', target: 75 },
]
const progressVals = ref(SKILL_BARS.map(() => 0))
let progId = null

function startProgress() {
  progressActive.value = true
  progressVals.value = SKILL_BARS.map(() => 0)
  progId = setInterval(() => {
    let done = true
    progressVals.value = progressVals.value.map((v, i) => {
      if (v < SKILL_BARS[i].target) { done = false; return Math.min(v + 2, SKILL_BARS[i].target) }
      return v
    })
    if (done) { clearInterval(progId); progId = null }
  }, 30)
}

function stopProgress() {
  clearInterval(progId); progId = null
  progressActive.value = false
  progressVals.value = SKILL_BARS.map(() => 0)
}

// ── Color palette ─────────────────────────────────────────────
const COLOR_PALETTE = [
  { label: 'violet  ', hex: '#8b5cf6', cls: 'text-violet-400' },
  { label: 'green   ', hex: '#4ade80', cls: 'text-green-400'  },
  { label: 'yellow  ', hex: '#facc15', cls: 'text-yellow-400' },
  { label: 'red     ', hex: '#f87171', cls: 'text-red-400'    },
  { label: 'blue    ', hex: '#60a5fa', cls: 'text-blue-400'   },
  { label: 'zinc    ', hex: '#a1a1aa', cls: 'text-zinc-400'   },
]

// ── Autocomplete ──────────────────────────────────────────────
const ALL_CMDS = [
  'cd', 'ls', 'pwd',
  'whoami', 'skills', 'social', 'neofetch', 'date',
  'open', 'theme', 'echo',
  'cv', 'resume', 'contact', 'projects', 'blog',
  'uptime', 'weather', 'calc', 'base64', 'joke',
  'ascii', 'banner', 'cowsay', 'color', 'progress',
  'snake', 'matrix', 'ping', 'sudo',
  'history', 'clear', 'help',
]
const CD_ARGS   = ['home', 'blog', 'about']
const OPEN_ARGS = ['github', 'linkedin']

const suggestions = ref([])
const suggIndex   = ref(-1)

// ── Command history navigation ────────────────────────────────
const cmdHistory  = ref([])   // executed commands, oldest → newest
const histIndex   = ref(-1)   // -1 = not navigating
const savedInput  = ref('')   // snapshot of input before navigating

function onArrowUp(e) {
  if (suggestions.value.length) return  // let suggestions handle it
  e.preventDefault()
  if (!cmdHistory.value.length) return
  if (histIndex.value === -1) savedInput.value = input.value
  histIndex.value = Math.min(histIndex.value + 1, cmdHistory.value.length - 1)
  input.value = cmdHistory.value[cmdHistory.value.length - 1 - histIndex.value]
}

function onArrowDown(e) {
  if (suggestions.value.length) return
  e.preventDefault()
  if (histIndex.value === -1) return
  histIndex.value--
  input.value = histIndex.value === -1
    ? savedInput.value
    : cmdHistory.value[cmdHistory.value.length - 1 - histIndex.value]
}

watch(input, val => {
  const parts = val.split(/\s+/)
  const cmd   = parts[0]
  const hasSpace = val.includes(' ')

  if (!val) {
    suggestions.value = []
    suggIndex.value = -1
    return
  }

  if (!hasSpace) {
    // completing the command itself
    suggestions.value = ALL_CMDS.filter(c => c.startsWith(cmd) && c !== cmd)
  } else if (parts[0] === 'cd') {
    const arg = parts[1] ?? ''
    suggestions.value = CD_ARGS.filter(a => a.startsWith(arg) && a !== arg).map(a => `cd ${a}`)
  } else if (parts[0] === 'open') {
    const arg = parts[1] ?? ''
    suggestions.value = OPEN_ARGS.filter(a => a.startsWith(arg) && a !== arg).map(a => `open ${a}`)
  } else {
    suggestions.value = []
  }
  suggIndex.value = -1
})

function onTab(e) {
  e.preventDefault()
  if (!suggestions.value.length) return

  if (suggestions.value.length === 1) {
    // single match — complete immediately
    const completed = suggestions.value[0]
    input.value = completed.includes(' ') ? completed : completed + ' '
    suggestions.value = []
  } else {
    // cycle through matches
    suggIndex.value = (suggIndex.value + 1) % suggestions.value.length
    const s = suggestions.value[suggIndex.value]
    input.value = s.includes(' ') ? s : s + ' '
  }
}

function applySuggestion(s) {
  input.value = s.includes(' ') ? s : s + ' '
  suggestions.value = []
  inputEl.value?.focus()
}

function scrollBottom() {
  nextTick(() => {
    const el = inputEl.value?.closest('.t-body') ?? document.querySelector('.t-body')
    if (el) el.scrollTop = el.scrollHeight
  })
}

function push(...lines) {
  history.value.push(...lines)
  scrollBottom()
}

function run() {
  const raw = input.value.trim()
  if (!raw) return
  const parts = raw.split(/\s+/)
  const cmd   = parts[0].toLowerCase()
  const arg   = parts[1]?.toLowerCase()
  const rest  = parts.slice(1).join(' ')

  history.value.push({ type: 'cmd', text: raw })
  cmdHistory.value.push(raw)
  histIndex.value = -1
  savedInput.value = ''

  switch (cmd) {
    case 'clear':
      history.value = []
      break

    case 'help':
      push(...helpLines.map(t => ({ type: 'out', text: t })))
      break

    case 'ls':
      push({ type: 'out', text: '  home   blog   about' })
      break

    case 'pwd':
      push({ type: 'ok', text: `  ${route.path}` })
      break

    case 'whoami':
      push(...whoamiLines.map(t => ({ type: 'out', text: t })))
      break

    case 'skills':
      push(...skillsLines.map(t => ({ type: 'out', text: t })))
      break

    case 'social':
      push(...socialLines.map(t => ({ type: 'out', text: t })))
      break

    case 'neofetch':
      push(...neofetchLines.map(t => ({ type: 'neofetch', text: t })))
      break

    case 'date': {
      const now = new Date()
      push(
        { type: 'ok', text: `  ${now.toDateString()}` },
        { type: 'out', text: `  ${now.toLocaleTimeString()}` },
      )
      break
    }

    case 'echo':
      push({ type: 'out', text: rest || '' })
      break

    case 'theme':
      toggleTheme()
      push({ type: 'ok', text: `  switched to ${isDark.value ? 'dark' : 'light'} mode` })
      break

    case 'open': {
      const url = openTargets[arg]
      if (url) {
        window.open(url, '_blank', 'noopener')
        push({ type: 'ok', text: `  opening ${arg}...` })
      } else {
        push({ type: 'err', text: `  open: unknown target "${arg}" — try: github · linkedin` })
      }
      break
    }

    case 'cd': {
      const dest = routes[arg ?? '']
      if (dest !== undefined) {
        push({ type: 'ok', text: `→ ${arg ?? 'home'}` })
        router.push(dest)
        open.value = false
      } else {
        push({ type: 'err', text: `bash: cd: ${arg}: No such page` })
      }
      break
    }

    case 'cv':
    case 'resume': {
      const a = document.createElement('a')
      a.href = '/Alejandro_J_Caraballo_Garcia_CV.pdf'
      a.download = 'Alejandro_J_Caraballo_Garcia_CV.pdf'
      a.click()
      push({ type: 'ok', text: '  ↓ downloading CV...' })
      break
    }

    case 'contact':
      if (arg === '-d' || arg === '--display') {
        push({ type: 'ok', text: '  alexcarballo96@gmail.com' })
      } else {
        window.open('mailto:alexcarballo96@gmail.com', '_blank')
        push({ type: 'ok', text: '  opening mail client...' })
      }
      break

    case 'projects':
      fetchProjects()
      break

    case 'blog':
      fetchBlogPosts()
      break

    case 'uptime': {
      const ms  = Date.now() - sessionStart
      const m   = Math.floor(ms / 60000)
      const s   = Math.floor((ms % 60000) / 1000)
      push({ type: 'ok', text: `  ${m}m ${s}s  in this session` })
      break
    }

    case 'weather':
      fetchWeather()
      break

    case 'calc': {
      if (!rest) { push({ type: 'err', text: '  usage: calc <expression>' }); break }
      push({ type: 'ok', text: `  = ${safeCalc(rest)}` })
      break
    }

    case 'base64': {
      const isFlag = arg === '-d' || arg === '--decode'
      const target = isFlag ? parts.slice(2).join(' ') : rest
      if (!target) { push({ type: 'err', text: '  usage: base64 [-d] <text>' }); break }
      push(...base64Cmd(target, isFlag ? '-d' : '').map(t => ({ type: 'ok', text: t })))
      break
    }

    case 'joke':
      fetchJoke()
      break

    case 'ascii':
    case 'banner':
      if (!rest) { push({ type: 'err', text: `  usage: ${cmd} <text>` }); break }
      if (cmd === 'banner') {
        const w = rest.length + 4
        push(
          { type: 'ok', text: `  ╔${'═'.repeat(w)}╗` },
          { type: 'ok', text: `  ║  ${rest}  ║` },
          { type: 'ok', text: `  ╚${'═'.repeat(w)}╝` },
        )
      } else {
        push(...asciiRender(rest).map(t => ({ type: 'ok', text: t })))
      }
      break

    case 'cowsay':
      if (!rest) { push({ type: 'err', text: '  usage: cowsay <text>' }); break }
      push(...cowsay(rest).map(t => ({ type: 'out', text: '  ' + t })))
      break

    case 'color':
      push(
        { type: 'out', text: '  Theme palette' },
        { type: 'out', text: '  ─────────────────────────────────────' },
        ...COLOR_PALETTE.map(c => ({ type: 'color', label: c.label, hex: c.hex, cls: c.cls })),
      )
      break

    case 'progress':
      startProgress()
      break

    case 'history':
      if (!cmdHistory.value.length) { push({ type: 'out', text: '  (empty)' }); break }
      push(...cmdHistory.value.map((c, i) => ({ type: 'out', text: `  ${String(i + 1).padStart(3)}  ${c}` })))
      break

    case 'snake':
      stopProgress()
      startSnake()
      break

    case 'matrix':
      stopProgress()
      push({ type: 'out', text: '  ESC to exit the matrix...' })
      nextTick(() => startMatrix())
      break

    case 'ping':
      push({ type: 'ok', text: '  pong 🏓' })
      break

    case 'sudo':
      push({ type: 'err', text: '  nice try 😏' })
      break

    default:
      push({ type: 'err', text: `bash: ${cmd}: command not found  (try help)` })
  }

  input.value = ''
  suggestions.value = []
  suggIndex.value = -1
}

// ── Resize ────────────────────────────────────────────────────
const MIN_W = 280, MIN_H = 180
const MAX_W = () => window.innerWidth  * 0.92
const MAX_H = () => window.innerHeight * 0.85

const PRESETS = {
  S: { w: 320,  h: 220 },
  M: { w: 448,  h: 320 },
  L: { w: 680,  h: 480 },
}

function loadSize() {
  try {
    const s = JSON.parse(localStorage.getItem('terminal_size') ?? 'null')
    if (s?.w && s?.h) return s
  } catch {}
  return { ...PRESETS.M }
}

const termSize     = ref(loadSize())
const maximized    = ref(false)
const preMaxSize   = ref(null)

const termStyle = computed(() => maximized.value
  ? { width: '92vw', height: '85vh', right: '4vw', bottom: '5rem' }
  : { width: `${termSize.value.w}px`, height: `${termSize.value.h}px` }
)

function saveSize() {
  localStorage.setItem('terminal_size', JSON.stringify(termSize.value))
}

function applyPreset(key) {
  maximized.value = false
  termSize.value  = { ...PRESETS[key] }
  saveSize()
}

function toggleMaximize() {
  if (maximized.value) {
    maximized.value = false
    if (preMaxSize.value) termSize.value = preMaxSize.value
  } else {
    preMaxSize.value = { ...termSize.value }
    maximized.value  = true
  }
}

// Drag-to-resize from the top-left grip
let resizing = false, rsX = 0, rsY = 0, rsW = 0, rsH = 0

function onResizeStart(e) {
  if (maximized.value) return
  resizing = true
  rsX = e.clientX; rsY = e.clientY
  rsW = termSize.value.w; rsH = termSize.value.h
  window.addEventListener('mousemove', onResizeMove)
  window.addEventListener('mouseup',   onResizeEnd)
  e.preventDefault()
}

function onResizeMove(e) {
  if (!resizing) return
  const dw = rsX - e.clientX   // dragging left  → wider
  const dh = rsY - e.clientY   // dragging up    → taller
  termSize.value = {
    w: Math.min(MAX_W(), Math.max(MIN_W, rsW + dw)),
    h: Math.min(MAX_H(), Math.max(MIN_H, rsH + dh)),
  }
}

function onResizeEnd() {
  resizing = false
  window.removeEventListener('mousemove', onResizeMove)
  window.removeEventListener('mouseup',   onResizeEnd)
  saveSize()
}

const bodyHeight = computed(() =>
  maximized.value
    ? 'calc(85vh - 6.5rem)'
    : `${termSize.value.h - 80}px`
)
</script>

<template>
  <!-- Toggle button -->
  <button
    @click="open = !open"
    class="fixed bottom-6 right-5 z-50 flex items-center gap-2 px-4 py-2.5 rounded-xl font-mono text-xs font-semibold shadow-lg transition-all duration-200"
    :class="open
      ? 'bg-violet-500 text-white shadow-violet-500/30'
      : 'bg-zinc-900 dark:bg-zinc-100 text-zinc-100 dark:text-zinc-900 hover:bg-violet-500 hover:text-white hover:shadow-violet-500/40 dark:hover:bg-violet-500 dark:hover:text-white'"
    title="Open terminal"
  >
    <span class="i-lucide-terminal w-4 h-4 shrink-0" />
    <span>terminal</span>
    <span v-if="!open" class="relative flex h-2 w-2">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-violet-400 opacity-75" />
      <span class="relative inline-flex rounded-full h-2 w-2 bg-violet-500" />
    </span>
  </button>

  <!-- Window -->
  <Transition name="slide">
    <div
      v-if="open"
      class="fixed bottom-20 right-5 z-50 flex flex-col rounded-xl overflow-hidden shadow-2xl border border-zinc-800 bg-zinc-950 text-zinc-100 font-mono text-xs"
      :style="termStyle"
    >
      <!-- Resize grip — top-left corner -->
      <div
        v-if="!maximized"
        @mousedown="onResizeStart"
        class="absolute top-0 left-0 w-4 h-4 cursor-nw-resize z-10 flex items-center justify-center"
        title="Drag to resize"
      >
        <span class="text-zinc-700 hover:text-zinc-400 text-[10px] leading-none select-none">⠿</span>
      </div>

      <!-- Title bar -->
      <div class="flex items-center gap-1.5 px-3 py-2 bg-zinc-900 border-b border-zinc-800 shrink-0">
        <span class="w-2.5 h-2.5 rounded-full bg-red-500 cursor-pointer" @click="open = false" />
        <span class="w-2.5 h-2.5 rounded-full bg-yellow-500 cursor-pointer" @click="applyPreset('S')" title="Small" />
        <span class="w-2.5 h-2.5 rounded-full bg-green-500 cursor-pointer" @click="toggleMaximize" title="Maximize" />

        <!-- Size presets -->
        <div class="flex items-center gap-1 ml-2">
          <button
            v-for="p in ['S','M','L']" :key="p"
            @click="applyPreset(p)"
            class="text-[9px] px-1 rounded transition-colors leading-none py-0.5"
            :class="!maximized && termSize.w === PRESETS[p].w && termSize.h === PRESETS[p].h
              ? 'text-violet-400 bg-violet-950'
              : 'text-zinc-600 hover:text-zinc-300'"
          >{{ p }}</button>
        </div>

        <span class="ml-auto text-zinc-500 text-[10px]">darkvus@portfolio</span>
      </div>

      <!-- Body -->
      <div
        class="t-body overflow-y-auto px-3 py-2 space-y-px flex-1"
        :style="{ height: bodyHeight }"
      >

        <!-- MATRIX -->
        <template v-if="matrixActive">
          <div class="text-[10px] text-green-600 text-center mb-1">[ ESC to exit ]</div>
          <div v-for="(row, y) in matrixGrid" :key="y" class="leading-none whitespace-nowrap">
            <span
              v-for="(cell, x) in row"
              :key="x"
              :class="cell.head ? 'text-white font-bold' : 'text-green-700'"
            >{{ cell.ch }}</span>
          </div>
        </template>

        <!-- PROGRESS -->
        <template v-else-if="progressActive">
          <div class="text-[10px] text-zinc-500 text-center mb-2">skills · ESC to exit</div>
          <div v-for="(bar, i) in SKILL_BARS" :key="bar.label" class="mb-1.5">
            <div class="flex justify-between text-[10px] mb-0.5">
              <span class="text-zinc-400">{{ bar.label }}</span>
              <span class="text-violet-400">{{ progressVals[i] }}%</span>
            </div>
            <div class="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
              <div
                class="h-full bg-violet-500 rounded-full transition-none"
                :style="{ width: progressVals[i] + '%' }"
              />
            </div>
          </div>
        </template>

        <!-- SNAKE -->
        <template v-else-if="gameActive">
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

        <!-- HISTORY -->
        <template v-else>
          <div v-if="history.length === 0" class="text-zinc-600">
            Type <span class="text-violet-400">help</span> to get started.
          </div>
          <div
            v-for="(line, i) in history"
            :key="i"
            class="leading-relaxed"
            :class="{
              'text-zinc-300':             line.type === 'cmd',
              'text-zinc-500':             line.type === 'out',
              'text-violet-400 font-bold': line.type === 'banner',
              'text-green-400':            line.type === 'ok',
              'text-red-400':              line.type === 'err',
              'text-green-500':            line.type === 'neofetch',
            }"
          >
            <span v-if="line.type === 'cmd'" class="text-violet-500 mr-1">$</span>
            <template v-if="line.type === 'cookie'">
              <div class="flex gap-2 mt-1">
                <button
                  @click="acceptCookies"
                  class="px-3 py-1 rounded bg-violet-500 hover:bg-violet-400 text-white text-[11px] font-semibold transition-colors"
                >[ accept ]</button>
                <button
                  @click="declineCookies"
                  class="px-3 py-1 rounded border border-zinc-600 hover:border-zinc-400 text-zinc-400 hover:text-zinc-200 text-[11px] transition-colors"
                >[ decline ]</button>
              </div>
            </template>
            <template v-else-if="line.type === 'color'">
              <span :class="line.cls">██ </span>
              <span class="text-zinc-400">{{ line.label }}</span>
              <span class="text-zinc-600">{{ line.hex }}</span>
            </template>
            <template v-else>{{ line.text }}</template>
          </div>
        </template>

      </div>

      <!-- Autocomplete suggestions -->
      <div
        v-if="!gameActive && !matrixActive && !progressActive && !cookiePending && suggestions.length"
        class="flex flex-wrap gap-1 px-3 py-1.5 border-t border-zinc-800/60 bg-zinc-900/60"
      >
        <button
          v-for="(s, i) in suggestions"
          :key="s"
          @click="applySuggestion(s)"
          class="px-2 py-0.5 rounded text-[10px] transition-colors"
          :class="i === suggIndex
            ? 'bg-violet-500 text-white'
            : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200'"
        >{{ s }}</button>
      </div>

      <!-- Input -->
      <div v-if="!gameActive && !matrixActive && !progressActive && !cookiePending" class="flex items-center gap-2 px-3 py-2 border-t border-zinc-800 bg-zinc-950">
        <span class="text-violet-500 shrink-0">$</span>
        <input
          ref="inputEl"
          v-model="input"
          @keydown.enter="run"
          @keydown.tab="onTab"
          @keydown.up="onArrowUp"
          @keydown.down="onArrowDown"
          @keydown.escape="suggestions.length ? (suggestions = []) : (open = false)"
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
