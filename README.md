<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=26&duration=3000&pause=1000&color=8B5CF6&center=true&vCenter=true&width=680&lines=darkvus.dev;Personal+portfolio+%26+blog;FastAPI+%2B+Vue+3;Built+from+scratch" alt="typing animation" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue-3-41B883?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-8b5cf6?style=for-the-badge)](LICENSE)

<p>
  Personal portfolio and blog — dark terminal aesthetic, bilingual (EN/ES),<br/>
  self-hosted admin panel and newsletter. No CMS, no bloat.
</p>

**[Live →](https://darkvus.dev)**

</div>

---

## 🛠️ Tech Stack

<div align="center">

[![Tech Stack](https://skillicons.dev/icons?i=python,fastapi,vue,vite,postgres,docker&theme=dark)](https://skillicons.dev)

</div>

<div align="center">

![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Turso](https://img.shields.io/badge/Turso-libSQL-4FF8D2?style=flat-square)
![UnoCSS](https://img.shields.io/badge/UnoCSS-333333?style=flat-square&logo=unocss&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Fly.io](https://img.shields.io/badge/Fly.io-7C3AED?style=flat-square)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

**✍️ Blog**
Markdown posts with slug routing · reading time · multilingual (EN/ES) · admin CRUD panel

</td>
<td width="50%">

**📁 Projects**
Auto-fetched from GitHub API · filtered by language · ordered newest-first · no maintenance required

</td>
</tr>
<tr>
<td>

**💌 Newsletter**
Email subscription with duplicate detection · subscriber list management from admin panel

</td>
<td>

**🔐 Admin Panel**
JWT-protected hidden route · post editor with image upload · subscriber management

</td>
</tr>
<tr>
<td>

**🌍 i18n**
Full EN/ES translation via `vue-i18n` · persisted language preference

</td>
<td>

**🖥️ Terminal Widget**
Interactive easter egg — `help`, `whoami`, `stack` and more

</td>
</tr>
</table>

---

## 📁 Project Structure

```
portfolio/
├── frontend/                    → Vue 3 + UnoCSS (Vercel)
│   ├── src/
│   │   ├── pages/               → Home · Blog · BlogPost · Projects · About · Admin
│   │   ├── components/          → NavBar · Terminal · NewsletterSignup
│   │   ├── api/                 → fetch client for backend
│   │   └── i18n/                → EN / ES translations
│   ├── uno.config.js            → dark mode · Inter + Fira Code fonts
│   └── vercel.json              → SPA rewrite rules
│
├── backend/                     → FastAPI + SQLAlchemy (Fly.io)
│   ├── app/
│   │   ├── main.py              → CORS · lifespan
│   │   ├── models.py            → Post · Subscriber
│   │   ├── database.py          → SQLite (dev) / Turso libSQL (prod)
│   │   ├── auth.py              → JWT · bcrypt
│   │   └── routers/             → posts · auth · newsletter · uploads
│   └── generate_hash.py         → bcrypt password hash helper
│
├── render.yaml                  → Render static site config (frontend)
└── .env.example                 → backend secrets template
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt

# Generate admin password hash
python generate_hash.py yourpassword

# Configure environment
cp .env.example .env
# Fill ADMIN_PASSWORD_HASH and SECRET_KEY in .env

uvicorn app.main:app --reload
# API  → http://localhost:8000
# Docs → http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install

echo "VITE_API_URL=http://localhost:8000" > .env.local

npm run dev
# App → http://localhost:5173
```

> Admin panel: `http://localhost:5173/admin` (hidden route, not in the navbar)

---

## ⚙️ Environment Variables

### Backend — `backend/.env`

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✓ | JWT signing key — generate with `secrets.token_hex(32)` |
| `ADMIN_USERNAME` | ✓ | Admin login username |
| `ADMIN_PASSWORD_HASH` | ✓ | bcrypt hash — generate with `generate_hash.py` |
| `DATABASE_URL` | — | SQLite path (default: `sqlite:///./portfolio.db`) |
| `TURSO_DATABASE_URL` | — | Turso libSQL URL (production) |
| `TURSO_AUTH_TOKEN` | — | Turso auth token (production) |
| `ALLOWED_ORIGINS` | ✓ | Comma-separated CORS origins |

### Frontend — `frontend/.env.local`

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend base URL |

---

## 🌐 Deploy

### Backend — Fly.io

```bash
cd backend
fly deploy
# Set secrets:
# fly secrets set SECRET_KEY=... ADMIN_PASSWORD_HASH=... TURSO_DATABASE_URL=... TURSO_AUTH_TOKEN=... ALLOWED_ORIGINS=...
```

### Frontend — Vercel

1. Import repo → set **Root Directory** to `frontend`
2. Add environment variable: `VITE_API_URL` = your Fly.io backend URL

The `render.yaml` at the root is also included for deploying the frontend as a Render static site.

---

## 🗺️ Routes

| Route | Visibility | Description |
|-------|-----------|-------------|
| `/` | Public | Home — bio, stack, recent posts |
| `/blog` | Public | Post list |
| `/blog/:slug` | Public | Post detail |
| `/projects` | Public | GitHub repos (live from API) |
| `/about` | Public | Extended bio and contact |
| `/admin` | Hidden | JWT-protected panel |

---

## 📋 License

[MIT](LICENSE) © [Alejandro Caraballo](https://github.com/Darkvus)
