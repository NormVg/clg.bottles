import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

/**
 * The window-level drop zone: the whole page is one drop target.
 * Depth-counted enter/leave keeps the overlay from flickering when the
 * pointer crosses child elements.
 */
export function useWindowDropZone(
  onFiles: (files: File[]) => void,
  enabled: Ref<boolean> = ref(true),
) {
  const dragging = ref(false)
  let depth = 0

  function hasFiles(event: DragEvent): boolean {
    const types = [...(event.dataTransfer?.types ?? [])]
    // Safari can report an empty type list during the first dragenter
    return types.includes('Files') || types.length === 0
  }

  function onDragEnter(event: DragEvent) {
    if (!enabled.value) return
    event.preventDefault()
    if (!hasFiles(event)) return
    depth += 1
    dragging.value = true
  }

  function onDragOver(event: DragEvent) {
    if (!enabled.value) return
    // always allow the drop — the browser must never open the file
    event.preventDefault()
  }

  function onDragLeave() {
    if (depth === 0) return
    depth -= 1
    if (depth === 0) dragging.value = false
  }

  function onDrop(event: DragEvent) {
    if (!enabled.value) return
    event.preventDefault()
    depth = 0
    dragging.value = false

    const files = [...(event.dataTransfer?.files ?? [])]
    if (files.length === 0) return
    onFiles(files)
  }

  onMounted(() => {
    window.addEventListener('dragenter', onDragEnter)
    window.addEventListener('dragover', onDragOver)
    window.addEventListener('dragleave', onDragLeave)
    window.addEventListener('drop', onDrop)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('dragenter', onDragEnter)
    window.removeEventListener('dragover', onDragOver)
    window.removeEventListener('dragleave', onDragLeave)
    window.removeEventListener('drop', onDrop)
  })

  return { dragging }
}
