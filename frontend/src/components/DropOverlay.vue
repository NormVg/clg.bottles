<script setup lang="ts">
import { computed } from 'vue'
import UiIcon from './ui/UiIcon.vue'

const props = defineProps<{
  path: string
}>()

const folder = computed(() => props.path.split('/').filter(Boolean).pop() ?? 'bottles')
</script>

<template>
  <Teleport to="body">
    <div class="drop" aria-hidden="true">
      <div class="drop__tile">
        <UiIcon name="upload" :size="20" class="drop__icon" />
        <span class="drop__label">drop to save</span>
        <span class="drop__sub">into {{ folder }}</span>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.drop {
  position: fixed;
  inset: 0;
  z-index: 55;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  pointer-events: none;
  animation: fade 120ms var(--ease-out) both;
}

.drop__tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 44px 64px;
  background: var(--surface);
  border: 1.5px dashed var(--line-strong);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-panel);
}

.drop__icon {
  color: var(--ink-secondary);
  animation: drop-float 1.4s var(--ease-in-out) infinite alternate;
}

.drop__label {
  font-size: var(--text-lg);
  color: var(--ink);
}

.drop__sub {
  font-size: var(--text-sm);
  color: var(--ink-tertiary);
}

@keyframes drop-float {
  from {
    transform: translateY(-2px);
  }
  to {
    transform: translateY(2px);
  }
}
</style>
