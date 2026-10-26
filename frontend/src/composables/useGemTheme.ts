import { computed } from 'vue'
import { useTheme } from './useTheme'

/**
 * The gemstone bottle, themed once: every surface that shows the living
 * mark shares the same ink per theme, the same stillness under reduced
 * motion, and a fully transparent backdrop.
 */
export function useGemTheme() {
  const { theme } = useTheme()

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  const gemColors = computed(() =>
    theme.value === 'dark' ? ['#f2f2f0', '#3a3a38'] : ['#333333', '#e7e6df'],
  )

  const gemBack = '#00000000'

  const gemInner = computed(() => (theme.value === 'dark' ? '#1c1c1b' : '#fafaf5'))

  const gemSpeed = reducedMotion ? 0 : 0.6

  return { gemColors, gemBack, gemInner, gemSpeed }
}
