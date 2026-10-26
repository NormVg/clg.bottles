<script setup lang="ts">
import { useToast } from '../../composables/useToast'
import UiIcon from './UiIcon.vue'

const { toasts, dismiss } = useToast()
</script>

<template>
  <Teleport to="body">
    <div class="ui-toast" aria-live="polite">
      <TransitionGroup name="ui-toast">
        <button
          v-for="toast in toasts"
          :key="toast.id"
          class="ui-toast__item"
          :class="{ 'ui-toast__item--danger': toast.tone === 'danger' }"
          :role="toast.tone === 'danger' ? 'alert' : 'status'"
          type="button"
          @click="dismiss(toast.id)"
        >
          <UiIcon :name="toast.tone === 'danger' ? 'close' : 'check'" :size="13" />
          <span>{{ toast.text }}</span>
        </button>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.ui-toast {
  position: fixed;
  right: 24px;
  bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  z-index: 80;
  pointer-events: none;
}

.ui-toast__item {
  pointer-events: auto;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 420px;
  padding: 9px 14px;
  background: var(--accent);
  color: var(--bg);
  border: none;
  border-radius: var(--radius-md);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.04);
  font-size: var(--text-sm);
  cursor: pointer;
  contain: content;
  transition: background-color var(--dur-press) var(--ease-out);
}

.ui-toast__item:hover {
  background: var(--accent-hover);
}

.ui-toast__item--danger {
  background: var(--danger-bg);
  color: var(--danger-ink);
  border: 1px solid var(--danger-border);
}

.ui-toast__item--danger:hover {
  background: #fbdfdf;
}

html[data-theme='dark'] .ui-toast__item--danger:hover {
  background: hsla(0, 72%, 60%, 0.26);
}

.ui-toast-enter-active {
  transition: transform 300ms var(--ease-out), opacity 300ms var(--ease-out);
}

.ui-toast-leave-active {
  transition: transform 200ms var(--ease-in), opacity 200ms var(--ease-in);
}

.ui-toast-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.ui-toast-leave-to {
  opacity: 0;
  transform: translateY(4px);
}
</style>
