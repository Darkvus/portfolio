<script setup>
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

const skills = [
  {
    category: '// languages',
    items: ['Python', 'Go', 'JavaScript', 'C/C++'],
  },
  {
    category: '// backend',
    items: ['FastAPI', 'Django', 'DRF', 'Pydantic', 'Celery', 'Kafka'],
  },
  {
    category: '// ai',
    items: ['OpenAI API', 'Anthropic Claude', 'LLMs', 'DSPy', 'MCP', 'AI Agents'],
  },
  {
    category: '// architecture',
    items: ['Microservices', 'Clean Architecture', 'CQRS', 'gRPC'],
  },
  {
    category: '// databases',
    items: ['PostgreSQL', 'MySQL', 'Redis'],
  },
  {
    category: '// cloud & devops',
    items: ['AWS', 'S3', 'Docker', 'GitHub Actions', 'CI/CD', 'Poetry', 'UV', 'Nexus'],
  },
  {
    category: '// observability',
    items: ['OpenTelemetry', 'Distributed tracing'],
  },
  {
    category: '// quality & security',
    items: ['Ruff', 'Mypy', 'Flake8', 'Bandit', 'Safety'],
  },
  {
    category: '// systems',
    items: ['Linux', 'Windows', 'macOS', 'Cisco networking'],
  },
]

const education = [
  {
    title:       { en: "Master's in Cybersecurity",          es: 'Máster en Ciberseguridad' },
    institution: 'UNIR',
    year:        null, // in progress
  },
  {
    title:       { en: 'Bachelor\'s in Computer Engineering', es: 'Grado en Ingeniería Informática' },
    institution: 'Universidad de Cádiz',
    year:        '2018',
  },
  {
    title:       { en: 'Cisco Certified Network Professional (CCNP)', es: 'Cisco Certified Network Professional (CCNP)' },
    institution: 'Cisco',
    year:        '2018',
  },
  {
    title:       { en: 'Cisco Certified Network Associate (CCNA 1)', es: 'Cisco Certified Network Associate (CCNA 1)' },
    institution: 'Cisco',
    year:        '2017',
  },
  {
    title:       { en: 'English B1 — APTIS', es: 'Inglés B1 — APTIS' },
    institution: 'British Council',
    year:        null,
  },
]

const experience = [
  {
    role:    { en: 'AI Engineer', es: 'Ingeniero de IA' },
    company: 'Tirant Lo Blanch',
    from:    'May 2026',
    to:      null,
    items: {
      en: [
        'Backend services and microservices within the Artificial Intelligence team.',
        'API design and development with Python and FastAPI; AI agents with DSPy.',
        'Integration of AI models via the OpenAI API and Anthropic Claude.',
        'Clean Architecture, async processing with Kafka and Redis, Pydantic v2.',
        'Observability and distributed tracing with OpenTelemetry.',
        'CI/CD with GitHub Actions and UV; AWS/S3; Ruff, Flake8, Mypy, Bandit, Safety.',
      ],
      es: [
        'Servicios backend y microservicios dentro del equipo de Inteligencia Artificial.',
        'Diseño y desarrollo de APIs con Python y FastAPI; agentes de IA con DSPy.',
        'Integración de modelos de IA mediante OpenAI API y Anthropic Claude.',
        'Clean Architecture, procesamiento asíncrono con Kafka y Redis, Pydantic v2.',
        'Observabilidad y trazabilidad distribuida con OpenTelemetry.',
        'CI/CD con GitHub Actions y UV; AWS/S3; Ruff, Flake8, Mypy, Bandit, Safety.',
      ],
    },
  },
  {
    role:    { en: 'Senior Python/Django Developer', es: 'Desarrollador Senior Python/Django' },
    company: 'Celering Smart Mobility Services',
    from:    'Dec 2022',
    to:      'Mar 2026',
    items: {
      en: [
        'Design, development and maintenance of microservices and APIs for a distributed, scalable platform.',
        'Stack: Python 3, Django, FastAPI, DRF, Celery, Ruff, Flake8, Safety, Poetry, Nexus.',
        'AWS cloud with S3 buckets, CI/CD automation.',
        'Clean Architecture, CQRS, gRPC.',
        'AI agents and MCPs for platform management and WhatsApp bookings.',
      ],
      es: [
        'Diseño, desarrollo y mantenimiento de microservicios y APIs para una plataforma distribuida y escalable.',
        'Stack: Python 3, Django, FastAPI, DRF, Celery, Ruff, Flake8, Safety, Poetry, Nexus.',
        'Cloud AWS con buckets en S3, automatización de CI/CD.',
        'Clean Architecture, CQRS, gRPC.',
        'Agentes de IA y MCPs para la gestión de la plataforma y reservas por WhatsApp.',
      ],
    },
  },
  {
    role:    { en: 'Python Developer', es: 'Desarrollador Python' },
    company: 'Acciona',
    from:    'Nov 2022',
    to:      'Dec 2022',
    items: {
      en: ['Backend development and maintenance of Python solutions.'],
      es: ['Desarrollo backend y mantenimiento de soluciones Python.'],
    },
  },
  {
    role:    { en: 'Python/Django Developer', es: 'Desarrollador Python/Django' },
    company: 'OpenWebinars',
    from:    'Mar 2021',
    to:      'Nov 2022',
    items: {
      en: [
        'Web application development for openwebinars.net.',
        'Stack: Python 3, Django 2.2, DRF 3.8, AWS S3, Unittest, VueJS, Ansible, CircleCI.',
      ],
      es: [
        'Desarrollo de aplicaciones web para openwebinars.net.',
        'Stack: Python 3, Django 2.2, DRF 3.8, AWS S3, Unittest, VueJS, Ansible, CircleCI.',
      ],
    },
  },
  {
    role:    { en: 'Python/Django Web Developer', es: 'Desarrollador Web Python/Django' },
    company: 'Opinno',
    from:    'Jul 2019',
    to:      'Mar 2021',
    items: {
      en: [
        'Web application development for opinno.io.',
        'Stack: Python 2/3, Django 1.10–2.2, DRF, AWS S3, Unittest, VueJS, React migration.',
      ],
      es: [
        'Desarrollo de aplicaciones web para opinno.io.',
        'Stack: Python 2/3, Django 1.10–2.2, DRF, AWS S3, Unittest, VueJS, migración a React.',
      ],
    },
  },
  {
    role:    { en: 'Web Developer', es: 'Desarrollador Web' },
    company: 'Universidad de Cádiz',
    from:    'Jul 2018',
    to:      'Jul 2019',
    items: {
      en: ['Web development with Python and Django (ORI web application).'],
      es: ['Desarrollo web con Python y Django (aplicación web ORI).'],
    },
  },
  {
    role:    { en: 'Web Developer', es: 'Desarrollador Web' },
    company: 'AYUDA-T',
    from:    'May 2018',
    to:      'Jul 2018',
    items: {
      en: ['Web development with PHP.'],
      es: ['Desarrollo web con PHP.'],
    },
  },
]
</script>

<template>
  <section class="space-y-12">

    <div class="space-y-2 pt-6">
      <h1 class="text-3xl font-bold">{{ t('about.title') }}</h1>
    </div>

    <!-- Bio -->
    <div class="space-y-4 text-zinc-600 dark:text-zinc-400 leading-relaxed">
      <p v-html="t('about.bio1')" />
      <p v-html="t('about.bio2')" />
      <p v-html="t('about.bio3')" />
    </div>

    <!-- Experience -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">{{ t('about.experience') }}</p>
      <div class="space-y-0">
        <div
          v-for="(job, i) in experience"
          :key="i"
          class="relative pl-6 pb-8 last:pb-0"
        >
          <!-- Timeline line -->
          <div v-if="i < experience.length - 1" class="absolute left-0 top-2 bottom-0 w-px bg-zinc-800" />
          <!-- Timeline dot -->
          <div
            class="absolute left-[-3px] top-2 w-1.5 h-1.5 rounded-full"
            :class="job.to === null ? 'bg-violet-500' : 'bg-zinc-600'"
          />

          <div class="space-y-1">
            <div class="flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
              <span class="font-semibold text-sm text-zinc-200">{{ job.role[locale] ?? job.role.en }}</span>
              <span class="text-zinc-500 text-xs">@</span>
              <span class="text-violet-400 text-sm font-mono">{{ job.company }}</span>
            </div>
            <p class="font-mono text-[10px] text-zinc-500">
              {{ job.from }} → {{ job.to ?? t('about.present') }}
            </p>
            <ul
              v-if="(job.items[locale] ?? job.items.en).length"
              class="mt-2 space-y-1"
            >
              <li
                v-for="(item, j) in (job.items[locale] ?? job.items.en)"
                :key="j"
                class="text-xs text-zinc-500 leading-relaxed flex gap-2"
              >
                <span class="text-zinc-600 shrink-0">·</span>{{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Education & Certifications -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">{{ t('about.education') }}</p>
      <div class="space-y-2">
        <div
          v-for="(item, i) in education"
          :key="i"
          class="flex items-start justify-between gap-4 p-4 rounded-xl border border-zinc-100 dark:border-zinc-800/60"
        >
          <div class="space-y-0.5 min-w-0">
            <p class="text-sm font-medium text-zinc-200 truncate">{{ item.title[locale] ?? item.title.en }}</p>
            <p class="text-xs font-mono text-zinc-500">{{ item.institution }}</p>
          </div>
          <span class="text-xs font-mono text-zinc-500 shrink-0 mt-0.5">
            <span v-if="item.year === null && item.title.en.includes('Master')" class="text-violet-400">{{ t('about.inProgress') }}</span>
            <span v-else-if="item.year">{{ item.year }}</span>
          </span>
        </div>
      </div>
    </div>

    <!-- Skills -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">{{ t('about.skills') }}</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div
          v-for="cat in skills"
          :key="cat.category"
          class="p-4 rounded-xl border border-zinc-100 dark:border-zinc-800/60"
        >
          <p class="text-xs font-mono text-violet-500 mb-2.5">{{ cat.category }}</p>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="s in cat.items"
              :key="s"
              class="text-xs px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400"
            >{{ s }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">{{ t('about.contact') }}</p>
      <div class="flex flex-col gap-3">
        <a
          href="mailto:alexcaraballo96@gmail.com"
          class="inline-flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400 hover:text-violet-500 transition-colors w-fit"
        >
          <span class="i-lucide-mail w-4 h-4" />
          alexcaraballo96@gmail.com
        </a>
        <a
          href="https://github.com/Darkvus"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400 hover:text-violet-500 transition-colors w-fit"
        >
          <span class="i-simple-icons-github w-4 h-4" />
          github.com/Darkvus
        </a>
        <a
          href="https://www.linkedin.com/in/alejandro-jose-c-66010aa1/"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400 hover:text-[#0077b5] transition-colors w-fit"
        >
          <span class="i-simple-icons-linkedin w-4 h-4" />
          linkedin.com/in/alejandro-jose-c-66010aa1
        </a>
        <a
          href="/Alejandro_J_Caraballo_Garcia_CV.pdf"
          download
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors w-fit mt-1"
        >
          <span class="i-lucide-download w-4 h-4" />
          {{ t('about.downloadCV') }}
        </a>
      </div>
    </div>

  </section>
</template>
