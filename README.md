Estructura del proyecto

  portfolio/
  ├── frontend/          → Vue 3 + UnoCSS (deploy en Vercel)
  │   ├── src/
  │   │   ├── pages/     → Home, Blog, BlogPost, About, Admin
  │   │   ├── components/→ NavBar (con dark/light toggle)
  │   │   └── api/       → cliente fetch para el backend
  │   ├── uno.config.js  → dark mode por clase, fuentes Inter/Fira Code
  │   └── vercel.json    → SPA routing para Vercel
  │
  ├── backend/           → FastAPI + SQLite (deploy en Render)
  │   ├── app/
  │   │   ├── main.py    → CORS configurable por env
  │   │   ├── models.py  → Post (title, slug, content, tags, published...)
  │   │   ├── routers/   → /posts (público) + /posts/all (admin) + /auth/token
  │   │   └── auth.py    → JWT con bcrypt
  │   └── generate_hash.py → genera el hash de tu contraseña
  │
  └── render.yaml        → config de deploy para Render

  ---
  Primeros pasos para arrancar

  Backend:
  cd portfolio/backend
  pip install -r requirements.txt

  # Genera el hash de tu contraseña de admin
  python generate_hash.py tupassword

  # Crea .env con el hash generado
  cp .env.example .env
  # Edita .env: pon el hash en ADMIN_PASSWORD_HASH

  uvicorn app.main:app --reload
  # API disponible en http://localhost:8000
  # Docs en http://localhost:8000/docs

  Frontend:
  cd portfolio/frontend
  npm install

  # Crea .env.local
  echo "VITE_API_URL=http://localhost:8000" > .env.local

  npm run dev
  # App en http://localhost:5173

  Admin panel: visita http://localhost:5173/admin (ruta oculta, no está en el nav)

  ---
  Deploy

  Render (backend):
  1. Nuevo Web Service → conecta el repo → Root Dir: backend
  2. En Environment Variables pon: ADMIN_PASSWORD_HASH, ALLOWED_ORIGINS (URL de Vercel)

  Vercel (frontend):
  1. Import repo → Root Dir: frontend
  2. Environment Variable: VITE_API_URL = URL de Render