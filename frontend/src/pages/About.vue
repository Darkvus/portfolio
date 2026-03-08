<script setup>
const skills = [
  {
    category: '// backend',
    items: ['Python', 'FastAPI', 'Django', 'Typer', 'SQLAlchemy', 'Pytest'],
  },
  {
    category: '// databases',
    items: ['PostgreSQL', 'SQLite', 'MongoDB', 'Redis'],
  },
  {
    category: '// cloud & infra',
    items: ['AWS S3', 'Docker', 'GitHub Actions', 'Render', 'Vercel'],
  },
  {
    category: '// tools',
    items: ['Git', 'REST APIs', 'JWT', 'OpenAPI', 'Linux'],
  },
]
</script>

<template>
  <section class="space-y-12">

    <div class="space-y-2 pt-6">
      <p class="font-mono text-sm text-violet-500 select-none">$ cat about.md</p>
      <h1 class="text-3xl font-bold">About me</h1>
    </div>

    <!-- Bio -->
    <div class="space-y-4 text-zinc-600 dark:text-zinc-400 leading-relaxed">
      <p>
        Hi! I'm <strong class="text-zinc-900 dark:text-zinc-100">Alejandro Jose Caraballo Garcia</strong>,
        a backend developer with a deep focus on Python and building efficient, scalable systems.
      </p>
      <p>
        I specialize in designing RESTful APIs, working with both relational and non-relational databases,
        and optimizing queries for performance and maintainability. I also have experience integrating
        AWS cloud services and automating workflows with GitHub Actions.
      </p>
      <p>
        I'm passionate about writing clean code that solves real problems — and I'm always learning
        something new.
      </p>
    </div>

    <!-- Skills -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">// skills</p>
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
            >
              {{ s }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact -->
    <div class="space-y-4">
      <p class="font-mono text-xs text-zinc-400">// contact</p>
      <div class="flex flex-col gap-2">
        <a
          href="https://github.com/Darkvus"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400 hover:text-violet-500 transition-colors w-fit"
        >
          GitHub · github.com/Darkvus →
        </a>
      </div>
    </div>

  </section>
</template>
