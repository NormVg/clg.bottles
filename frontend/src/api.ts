import type {
  ApiDirectory,
  ApiFolder,
  ApiItem,
  ApiMedia,
  ApiSearchResult,
  ApiUser,
} from './types'

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail ?? 'request failed.')
  }

  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export const api = {
  me(): Promise<ApiUser> {
    return request('/auth/me')
  },

  signup(input: { name: string; email: string; password: string }): Promise<ApiUser> {
    return request('/auth/signup', { method: 'POST', body: JSON.stringify(input) })
  },

  login(input: { email: string; password: string }): Promise<ApiUser> {
    return request('/auth/login', { method: 'POST', body: JSON.stringify(input) })
  },

  logout(): Promise<void> {
    return request('/auth/logout', { method: 'POST' })
  },

  directory(path: string): Promise<ApiDirectory> {
    return request(`/fs?path=${encodeURIComponent(path)}`)
  },

  folders(): Promise<ApiFolder[]> {
    return request('/folders')
  },

  createFolder(path: string): Promise<ApiFolder> {
    return request('/folders', { method: 'POST', body: JSON.stringify({ path }) })
  },

  renameFolder(id: number, name: string): Promise<ApiFolder> {
    return request(`/folders/${id}`, { method: 'PATCH', body: JSON.stringify({ name }) })
  },

  deleteFolder(id: number): Promise<void> {
    return request(`/folders/${id}`, { method: 'DELETE' })
  },

  createLink(input: { url: string; path?: string; title?: string }): Promise<ApiItem> {
    return request('/items', {
      method: 'POST',
      body: JSON.stringify({ type: 'link', ...input }),
    })
  },

  createNote(input: { note: string; path?: string; title?: string }): Promise<ApiItem> {
    return request('/items', {
      method: 'POST',
      body: JSON.stringify({ type: 'note', ...input }),
    })
  },

  updateItem(
    id: number,
    input: { title?: string; url?: string; note?: string },
  ): Promise<ApiItem> {
    return request(`/items/${id}`, { method: 'PATCH', body: JSON.stringify(input) })
  },

  deleteItem(id: number): Promise<void> {
    return request(`/items/${id}`, { method: 'DELETE' })
  },

  upload(
    file: File,
    path: string,
    title?: string,
    onProgress?: (fraction: number) => void,
  ): Promise<{ media: ApiMedia; item: ApiItem }> {
    const form = new FormData()
    form.append('file', file)
    form.append('path', path)
    if (title) form.append('title', title)

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', '/api/media')
      xhr.responseType = 'json'

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable && onProgress) onProgress(event.loaded / event.total)
      }
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(xhr.response as { media: ApiMedia; item: ApiItem })
        } else {
          const body = xhr.response as { detail?: string } | null
          reject(new Error(body?.detail ?? 'could not upload.'))
        }
      }
      xhr.onerror = () => reject(new Error('could not upload.'))
      xhr.send(form)
    })
  },

  search(q: string): Promise<ApiSearchResult> {
    return request(`/search?q=${encodeURIComponent(q)}`)
  },
}
