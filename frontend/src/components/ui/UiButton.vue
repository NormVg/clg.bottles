<script setup lang="ts">
import UiIcon from './UiIcon.vue'

withDefaults(
  defineProps<{
    variant?: 'solid' | 'ghost' | 'quiet' | 'danger'
    size?: 'sm' | 'md'
    type?: 'button' | 'submit'
    disabled?: boolean
    loading?: boolean
    block?: boolean
  }>(),
  {
    variant: 'solid',
    size: 'md',
    type: 'button',
    disabled: false,
    loading: false,
    block: false,
  },
)
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    class="ui-button"
    :class="[`ui-button--${variant}`, `ui-button--${size}`, { 'ui-button--block': block }]"
    :aria-busy="loading || undefined"
    :aria-disabled="disabled || undefined"
  >
    <span class="ui-button__label" :class="{ 'ui-button__label--loading': loading }">
      <slot />
    </span>

    <span v-if="loading" class="ui-button__spinner" aria-hidden="true">
      <UiIcon name="loading" :size="size === 'sm' ? 13 : 14" class="ui-button__spin" />
    </span>
  </button>
</template>

<style scoped>
.ui-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: var(--radius-md);
  font-weight: 400;
  letter-spacing: 0.01em;
  white-space: nowrap;
  line-height: 1;
  transition: background-color var(--dur-press) var(--ease-out),
    color var(--dur-press) var(--ease-out),
    border-color var(--dur-press) var(--ease-out),
    transform 100ms var(--spring-bounce);
  contain: content;
}

.ui-button:active:not(:disabled) {
  transform: scale(0.96);
}

.ui-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.ui-button--md {
  min-height: 36px;
  padding: 0 16px;
  font-size: var(--text-sm);
}

.ui-button--sm {
  min-height: 32px;
  padding: 0 10px;
  font-size: var(--text-xs);
}

.ui-button--sm::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: inherit;
}

.ui-button--solid {
  background: var(--accent);
  color: var(--bg);
}

.ui-button--solid:hover:not(:disabled) {
  background: var(--accent-hover);
}

.ui-button--ghost {
  background: transparent;
  color: var(--ink);
  border: 1px solid var(--line-strong);
}

.ui-button--ghost:hover:not(:disabled) {
  background: var(--surface-muted);
}

.ui-button--quiet {
  background: transparent;
  color: var(--ink-tertiary);
  padding: 6px 8px;
  border-radius: var(--radius-sm);
}

.ui-button--quiet::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: inherit;
}

.ui-button--quiet:hover:not(:disabled) {
  color: var(--ink);
}

.ui-button--danger {
  background: var(--danger-bg);
  color: var(--danger-ink);
  border: 1px solid var(--danger-border);
}

.ui-button--danger:hover:not(:disabled) {
  filter: brightness(0.97);
}

.ui-button--block {
  width: 100%;
}

.ui-button__label--loading {
  visibility: hidden;
}

.ui-button__spinner {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.ui-button__spin {
  animation: ui-button-spin 0.8s linear infinite;
}

@keyframes ui-button-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
