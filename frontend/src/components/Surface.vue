<script setup lang="ts">
import UiIcon from './ui/UiIcon.vue'

defineProps<{
  title: string
}>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <section class="surface" :aria-label="title">
    <header class="surface__head">
      <h2 class="surface__title">{{ title }}</h2>
      <button class="surface__close" type="button" aria-label="close" @click="emit('close')">
        <UiIcon name="close" :size="16" />
      </button>
    </header>
    <div class="surface__body">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.surface__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--line);
}

.surface__title {
  font-size: var(--text-lg);
  font-weight: 400;
  color: var(--ink);
  letter-spacing: 0.01em;
}

.surface__close {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border-radius: var(--radius-sm);
  color: var(--ink-tertiary);
  transition: color var(--dur-press) var(--ease-out),
    background-color var(--dur-press) var(--ease-out);
}

.surface__close::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: inherit;
}

.surface__close:hover {
  color: var(--ink);
  background: var(--surface-muted);
}

.surface__body {
  padding-top: 20px;
}
</style>
