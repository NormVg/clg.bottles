<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Browser from './components/Browser.vue'
import UiIcon from './components/ui/UiIcon.vue'
import UiToast from './components/ui/UiToast.vue'
import { useTheme } from './composables/useTheme'

const { theme, restore, toggle } = useTheme()
const path = ref('/')

onMounted(restore)
</script>

<template>
  <div class="shell">
    <button class="shell__brand" type="button" aria-label="bottles" @click="path = '/'">
      <img class="shell__brand-mark" src="/logo-nobg.svg" alt="" width="11" height="27" />
    </button>

    <span class="shell__word" aria-hidden="true">bottles</span>

    <button
      class="shell__theme"
      type="button"
      :aria-label="theme === 'dark' ? 'switch to the light theme' : 'switch to the dark theme'"
      @click="toggle"
    >
      <UiIcon :name="theme === 'dark' ? 'sun' : 'moon'" :size="15" />
    </button>

    <div class="shell-column">
      <main class="shell-main">
        <Browser v-model:path="path" />
      </main>
    </div>

    <div class="shell-phone">
      <img
        class="shell__brand-mark shell-phone__mark"
        src="/logo-nobg.svg"
        alt=""
        width="11"
        height="27"
      />
      <p class="shell-phone__title">bottles is a desk thing.</p>
      <p class="shell-phone__sub">
        open this app on a desktop to use it — the keyboard, the canvas: none of it is made for
        the phone.
      </p>
    </div>

    <UiToast />
  </div>
</template>

<style scoped>
.shell__brand {
  position: fixed;
  top: 24px;
  left: 24px;
  z-index: 30;
  display: inline-flex;
  align-items: center;
  color: var(--ink);
  padding: 2px 4px;
  margin-left: -4px;
  border-radius: var(--radius-sm);
  transition: opacity var(--dur-press) var(--ease-out);
  animation: fade var(--dur-state) var(--ease-out) both;
}

.shell__brand-mark {
  display: block;
  width: auto;
  height: 27px;
}

.shell__brand::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: inherit;
}

.shell__brand:hover {
  opacity: 0.72;
}

.shell__word {
  position: fixed;
  bottom: 34px;
  left: 24px;
  z-index: 30;
  font-size: var(--text-sm);
  color: var(--ink-tertiary);
  pointer-events: none;
  animation: fade var(--dur-state) var(--ease-out) both;
}

.shell__theme {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 30;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  color: var(--ink-tertiary);
  border-radius: var(--radius-sm);
  transition: color var(--dur-press) var(--ease-out);
  animation: fade var(--dur-state) var(--ease-out) both;
}

.shell__theme::after {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: inherit;
}

.shell__theme:hover,
.shell__theme:focus-visible {
  color: var(--ink);
}

@media (max-width: 820px) {
  .shell__word {
    display: none;
  }
}

@media (max-width: 640px) {
  .shell__brand {
    top: 20px;
    left: 20px;
  }

  .shell__theme {
    top: 21px;
    right: 20px;
  }
}

.shell-phone {
  display: none;
}

@media (max-width: 720px) {
  .shell > :not(.shell-phone) {
    display: none;
  }

  .shell {
    display: block;
  }

  .shell-phone {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 14px;
    padding: 32px;
    text-align: center;
    background: var(--bg);
  }

  .shell-phone__mark {
    height: 34px;
    margin-bottom: 6px;
  }

  .shell-phone__title {
    font-size: 22px;
    letter-spacing: -0.01em;
    color: var(--ink);
  }

  .shell-phone__sub {
    font-size: var(--text-sm);
    line-height: 1.7;
    color: var(--ink-secondary);
    max-width: 30ch;
  }
}
</style>
