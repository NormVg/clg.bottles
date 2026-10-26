import { ref } from 'vue'

export type ThemeName = 'light' | 'dark'

const STORAGE_KEY = 'bottles:theme'

const THEME_COLORS: Record<ThemeName, string> = {
  light: '#ffffff',
  dark: '#111111',
}

const theme = ref<ThemeName>('light')

function apply(next: ThemeName) {
  theme.value = next
  document.documentElement.dataset.theme = next
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', THEME_COLORS[next])
}

export function useTheme() {
  function restore() {
    apply(localStorage.getItem(STORAGE_KEY) === 'dark' ? 'dark' : 'light')
  }

  function toggle() {
    const next: ThemeName = theme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem(STORAGE_KEY, next)
    apply(next)
  }

  return { theme, restore, toggle }
}
