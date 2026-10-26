import { onMounted, onUnmounted, ref, type Ref } from 'vue'

/**
 * One-shot viewport reveal: true once the element scrolls into view.
 * Content must never stay hidden, so a missing observer reveals at once.
 */
export function useInView(target: Ref<HTMLElement | null>, options: { threshold?: number } = {}) {
  const inView = ref(false)
  let observer: IntersectionObserver | undefined

  onMounted(() => {
    const element = target.value
    if (!element) return

    if (typeof IntersectionObserver === 'undefined') {
      inView.value = true
      return
    }

    observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          inView.value = true
          observer?.disconnect()
        }
      },
      { threshold: options.threshold ?? 0.15 },
    )
    observer.observe(element)
  })

  onUnmounted(() => observer?.disconnect())

  return inView
}
