const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function req(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

export const getPosts = () =>
  req('/posts/')

export const getPost = (slug) =>
  req(`/posts/${slug}`)

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
