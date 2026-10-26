<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<template>
  <div class="ui-empty fade-in" role="status">
    <p class="ui-empty__text">{{ text }}</p>
    <slot />
  </div>
</template>

<style scoped>
.ui-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 48px 24px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius-lg);
}

.ui-empty__text {
  color: var(--ink-secondary);
  font-size: var(--text-base);
  text-align: center;
}
</style>
