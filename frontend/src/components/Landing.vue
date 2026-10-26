<script setup lang="ts">
import { useTheme } from '../composables/useTheme'
import UiButton from './ui/UiButton.vue'
import UiIcon from './ui/UiIcon.vue'

const emit = defineEmits<{
  open: []
}>()

const { theme, toggle } = useTheme()
</script>

<template>
  <div class="landing">
    <header class="landing__bar">
      <span class="landing__word">
        <img class="landing__word-mark" src="/logo-nobg.svg" alt="" width="12" height="30" />
        bottles
      </span>
      <div class="landing__bar-side">
        <button
          class="landing__theme"
          type="button"
          :aria-label="theme === 'dark' ? 'switch to the light theme' : 'switch to the dark theme'"
          @click="toggle"
        >
          <UiIcon :name="theme === 'dark' ? 'sun' : 'moon'" :size="15" />
        </button>
        <button class="landing__enter" type="button" @click="emit('open')">open</button>
      </div>
    </header>

    <main class="landing__hero">
      <div class="landing__mark rise" style="--i: 0" aria-hidden="true">
        <img src="/logo-nobg.svg" alt="" width="24" height="60" />
      </div>
      <p class="landing__eyebrow label rise" style="--i: 1">bookmarks, filed properly</p>
      <h1 class="landing__title rise" style="--i: 2">
        a quiet place for your links, notes and files.
      </h1>
      <p class="landing__sub rise" style="--i: 3">
        no feed, no noise. one space for what you keep.
      </p>
      <div class="landing__cta rise" style="--i: 4">
        <UiButton @click="emit('open')">open bottles</UiButton>
      </div>
    </main>

    <section class="landing__features" aria-label="how bottles works">
      <div class="landing__feature">
        <span class="landing__feature-label label">links</span>
        <p class="landing__feature-text">save a url, open it later. the title comes from the page.</p>
      </div>
      <div class="landing__feature">
        <span class="landing__feature-label label">notes</span>
        <p class="landing__feature-text">paste text and keep it. no editor, no ceremony.</p>
      </div>
      <div class="landing__feature">
        <span class="landing__feature-label label">files</span>
        <p class="landing__feature-text">drop a file anywhere. it lives in the same database.</p>
      </div>
    </section>

    <footer class="landing__foot">
      <span class="landing__foot-mark">bottles</span>
      <span class="landing__foot-note">a college project</span>
    </footer>
  </div>
</template>

<style scoped>
.landing { min-height: 100dvh; display: flex; flex-direction: column; padding: 0 24px; }
.landing__bar { display: flex; align-items: center; justify-content: space-between; padding: 28px 0; }
.landing__word { display: inline-flex; align-items: center; gap: 8px; font-size: 15px; color: var(--ink); letter-spacing: 0.06em; }
.landing__word-mark { display: block; width: auto; height: 30px; }
.landing__bar-side { display: flex; align-items: center; gap: 18px; }
.landing__theme {
  display: inline-flex; align-items: center; justify-content: center;
  width: 26px; height: 26px; color: var(--ink-tertiary); border-radius: var(--radius-sm);
  transition: color var(--dur-press) var(--ease-out);
}
.landing__theme:hover { color: var(--ink); }
.landing__enter {
  position: relative; font-size: var(--text-sm); color: var(--ink-tertiary);
  padding: 4px 6px; margin: -4px -6px; border-radius: var(--radius-sm);
  transition: color var(--dur-press) var(--ease-out);
}
.landing__enter:hover { color: var(--ink); }
.landing__hero {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; gap: 18px;
  padding: clamp(48px, 10vh, 120px) 0;
}
.landing__mark img { display: block; width: auto; height: 60px; opacity: 0.9; }
.landing__eyebrow { font-size: var(--text-xs); color: var(--ink-tertiary); letter-spacing: 0.14em; }
.landing__title {
  font-size: clamp(30px, 5vw, 44px); font-weight: 400; letter-spacing: -0.02em;
  line-height: 1.12; color: var(--ink); max-width: 18ch;
}
.landing__sub { font-size: var(--text-sm); line-height: 1.7; color: var(--ink-secondary); max-width: 40ch; }
.landing__cta { margin-top: 10px; }
.landing__features {
  display: grid; grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);
  max-width: 680px; width: 100%; margin: 0 auto;
}
.landing__feature { padding: 28px 24px; border-right: 1px solid var(--line); }
.landing__feature:last-child { border-right: none; }
.landing__feature-label {
  display: block; font-size: var(--text-xs); color: var(--ink-tertiary);
  letter-spacing: 0.14em; margin-bottom: 10px;
}
.landing__feature-text { font-size: var(--text-sm); line-height: 1.7; color: var(--ink-secondary); }
.landing__foot {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 32px 0; font-size: var(--text-xs); color: var(--ink-tertiary);
}
.landing__foot-mark { letter-spacing: 0.06em; }
@media (max-width: 680px) {
  .landing__features { grid-template-columns: 1fr; }
  .landing__feature { border-right: none; border-bottom: 1px solid var(--line); }
  .landing__feature:last-child { border-bottom: none; }
}
</style>
