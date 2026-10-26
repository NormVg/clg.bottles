import { ref } from 'vue'

export type ToastTone = 'neutral' | 'danger'

export interface ToastMessage {
  id: number
  text: string
  tone: ToastTone
}

const toasts = ref<ToastMessage[]>([])
let nextId = 1

export function useToast() {
  function push(text: string, tone: ToastTone = 'neutral', durationMs = 4000): number {
    const id = nextId++
    toasts.value.push({ id, text, tone })
    if (durationMs > 0) setTimeout(() => dismiss(id), durationMs)
    return id
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  return { toasts, push, dismiss }
}
