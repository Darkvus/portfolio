const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function req(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

export const getPosts = (lang = 'en') =>
  req(`/posts/?lang=${lang}`)

export const getPost = (slug, lang = 'en') =>
  req(`/posts/${slug}?lang=${lang}`)

export const getAllPosts = (token) =>
  req('/posts/all', { headers: { Authorization: `Bearer ${token}` } })

export const login = (username, password) =>
  req('/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })

export const createPost = (data, token) =>
  req('/posts/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(data),
  })

export const updatePost = (id, data, token) =>
  req(`/posts/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(data),
  })

export const deletePost = (id, token) =>
  req(`/posts/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })

export const uploadImage = async (file, token) => {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/uploads/image`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  })
  if (!res.ok) throw new Error('Upload failed')
  return res.json()
}

export const subscribe = (email) =>
  req('/newsletter/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })

export const getSubscribers = (token) =>
  req('/newsletter/subscribers', { headers: { Authorization: `Bearer ${token}` } })

export const deleteSubscriber = (id, token) =>
  req(`/newsletter/subscribers/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
