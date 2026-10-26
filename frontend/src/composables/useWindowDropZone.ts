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
    return [...(event.dataTransfer?.types ?? [])].includes('Files')
  }

  function onDragEnter(event: DragEvent) {
    if (!enabled.value || !hasFiles(event)) return
    event.preventDefault()
    depth += 1
    dragging.value = true
  }

  function onDragOver(event: DragEvent) {
    if (!enabled.value || !hasFiles(event)) return
    event.preventDefault()
  }

  function onDragLeave() {
    if (depth === 0) return
    depth -= 1
    if (depth === 0) dragging.value = false
  }

  function onDrop(event: DragEvent) {
    if (!enabled.value) return
    depth = 0
    dragging.value = false

    const files = [...(event.dataTransfer?.files ?? [])]
    if (files.length === 0) return
    event.preventDefault()
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
