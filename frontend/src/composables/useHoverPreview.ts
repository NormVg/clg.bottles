import { computed, onBeforeUnmount, ref, type Ref } from 'vue'
import { api } from '../api'
import type { ApiItem } from '../types'

/**
 * The floating hover thumbnail: media images and videos preview from
 * their own bytes, links resolve their og:image through the api. Link
 * previews are cached in localStorage so a hover never refetches.
 */

const STORE_KEY = 'bottle:link-previews'
const TTL_MS = 6 * 60 * 60 * 1000
const STORE_MAX = 200

interface StoredPreview {
  image: string | null
  at: number
}

const cache = new Map<string, StoredPreview>()

function hydrate() {
  try {
    const raw = localStorage.getItem(STORE_KEY)
    if (!raw) return
    const parsed = JSON.parse(raw) as Record<string, StoredPreview>
    const now = Date.now()
    for (const [id, entry] of Object.entries(parsed)) {
      const image = entry?.image
      if (typeof image !== 'string' && image !== null) continue
      if (now - (entry.at ?? 0) < TTL_MS) cache.set(id, { image, at: entry.at })
    }
  } catch {
    // corrupt or unavailable storage — the memory cache still works
  }
}

function persist(id: string, image: string | null) {
  cache.set(id, { image, at: Date.now() })
  try {
    const payload: Record<string, StoredPreview> = {}
    for (const [key, value] of [...cache.entries()].slice(-STORE_MAX)) {
      payload[key] = value
    }
    localStorage.setItem(STORE_KEY, JSON.stringify(payload))
  } catch {
    // storage full or unavailable — nothing to do
  }
}

if (typeof window !== 'undefined') hydrate()

export function useHoverPreview(item: Ref<ApiItem | undefined>) {
  const preview = ref<HTMLDivElement | null>(null)
  const linkImage = ref<string | null>(null)
  let hovering = false
  let timer: ReturnType<typeof setTimeout> | undefined
  let cursor = { x: 0, y: 0 }

  const isMedia = computed(() => item.value?.type === 'media')
  const isVideo = computed(() => (item.value?.media?.mime_type ?? '').startsWith('video/'))
  const isImage = computed(() => (item.value?.media?.mime_type ?? '').startsWith('image/'))
  const isLink = computed(() => item.value?.type === 'link')

  const source = computed(() => {
    if (isMedia.value && item.value?.media) return `/api/media/${item.value.media.id}/raw`
    return linkImage.value
  })

  const canPreview = computed(
    () => (isMedia.value && (isImage.value || isVideo.value)) || isLink.value,
  )

  function place(x: number, y: number) {
    if (!preview.value) return
    const left = Math.min(x + 20, window.innerWidth - 240)
    const top = Math.min(Math.max(y - 100, 12), window.innerHeight - 190)
    preview.value.style.transform = `translate3d(${left}px, ${top}px, 0)`
  }

  function reveal() {
    if (!hovering || !preview.value || !source.value) return
    place(cursor.x, cursor.y)
    preview.value.style.opacity = '1'
  }

  function hide() {
    if (preview.value) preview.value.style.opacity = '0'
  }

  function setPreview(element: unknown) {
    preview.value = element instanceof HTMLDivElement ? element : null
  }

  function onEnter() {
    if (!canPreview.value) return
    hovering = true
    timer = setTimeout(async () => {
      if (!hovering) return
      if (isMedia.value) {
        reveal()
        return
      }
      await loadLink()
      reveal()
    }, 180)
  }

  async function loadLink() {
    const current = item.value
    if (!current || current.type !== 'link') return

    const cached = cache.get(String(current.id))
    if (cached !== undefined) {
      linkImage.value = cached.image
      return
    }
    try {
      const { image } = await api.getLinkPreview(current.id)
      persist(String(current.id), image)
      linkImage.value = image
    } catch {
      persist(String(current.id), null)
    }
  }

  function onMove(event: MouseEvent) {
    cursor = { x: event.clientX, y: event.clientY }
    if (preview.value && preview.value.style.opacity === '1') place(cursor.x, cursor.y)
  }

  function onLeave() {
    hovering = false
    clearTimeout(timer)
    hide()
  }

  onBeforeUnmount(() => clearTimeout(timer))

  return { setPreview, source, isVideo, onEnter, onMove, onLeave, hide }
}
