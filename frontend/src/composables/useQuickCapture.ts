import { onBeforeUnmount, onMounted, type Ref } from 'vue'
import { api } from '../api'
import { normalizeUrl } from '../utils/url'
import { useToast } from './useToast'

/**
 * Paste anything to save it: a url becomes a link, other text becomes a
 * note, and pasted files are uploaded. Pasting into a field is left alone.
 */
export function useQuickCapture(
  path: Ref<string>,
  onSaved: () => void,
  enabled: Ref<boolean>,
) {
  const { push } = useToast()

  function onPaste(event: ClipboardEvent) {
    if (!enabled.value) return
    const target = event.target as HTMLElement | null
    const editing =
      target instanceof HTMLInputElement ||
      target instanceof HTMLTextAreaElement ||
      target?.isContentEditable
    if (editing) return

    const files = clipboardFiles(event)
    if (files.length > 0) {
      event.preventDefault()
      void captureFiles(files)
      return
    }

    const text = event.clipboardData?.getData('text/plain').trim()
    if (!text) return
    event.preventDefault()
    void captureText(text)
  }

  async function captureFiles(files: File[]) {
    for (const file of files) {
      try {
        await api.upload(file, path.value)
      } catch (cause) {
        push(cause instanceof Error ? cause.message : 'could not upload.', 'danger')
      }
    }
    push('uploaded.')
    onSaved()
  }

  async function captureText(text: string) {
    const url = normalizeUrl(text)
    try {
      if (url) {
        await api.createLink({ url, path: path.value })
        push('saved.')
      } else {
        await api.createNote({ note: text, path: path.value })
        push('noted.')
      }
      onSaved()
    } catch (cause) {
      push(cause instanceof Error ? cause.message : 'could not save.', 'danger')
    }
  }

  onMounted(() => window.addEventListener('paste', onPaste))
  onBeforeUnmount(() => window.removeEventListener('paste', onPaste))

  return { captureFiles }
}

function clipboardFiles(event: ClipboardEvent): File[] {
  const data = event.clipboardData
  if (!data) return []

  const direct = [...data.files]
  if (direct.length > 0) return direct

  return [...data.items]
    .filter((item) => item.kind === 'file')
    .map((item) => item.getAsFile())
    .filter((file): file is File => file !== null)
}
