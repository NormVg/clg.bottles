<script setup lang="ts">
withDefaults(
  defineProps<{
    height?: string
    width?: string
  }>(),
  {
    height: '19px',
    width: '100%',
  },
)
</script>

<template>
  <div class="ui-skeleton" :style="{ height, width }" aria-hidden="true" />
</template>

<style scoped>
.ui-skeleton {
  background: linear-gradient(
    90deg,
    var(--line) 25%,
    var(--line-strong) 50%,
    var(--line) 75%
  );
  background-size: 200% 100%;
  animation: ui-skeleton-shimmer 1.5s infinite linear;
  border-radius: var(--radius-md);
}

@keyframes ui-skeleton-shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ui-skeleton {
    animation: none;
    opacity: 0.6;
  }
}
</style>
