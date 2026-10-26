<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    path: string
    root?: string
  }>(),
  {
    root: 'bottles',
  },
)

const emit = defineEmits<{
  navigate: [path: string]
}>()

interface Crumb {
  label: string
  path: string
  current: boolean
}

const crumbs = computed<Crumb[]>(() => {
  const segments = props.path.split('/').filter(Boolean)
  const trail: Crumb[] = [{ label: props.root, path: '/', current: segments.length === 0 }]
  let accumulated = ''
  segments.forEach((segment, index) => {
    accumulated += `/${segment}`
    trail.push({ label: segment, path: accumulated, current: index === segments.length - 1 })
  })
  return trail
})
</script>

<template>
  <nav class="crumbs fade-in" aria-label="location">
    <template v-for="(crumb, index) in crumbs" :key="crumb.path">
      <span v-if="index > 0" class="crumbs__sep">/</span>
      <button
        v-if="!crumb.current"
        class="crumbs__link"
        type="button"
        @click="emit('navigate', crumb.path)"
      >
        {{ crumb.label }}
      </button>
      <span v-else class="crumbs__current">{{ crumb.label }}</span>
    </template>
  </nav>
</template>

<style scoped>
.crumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: var(--text-sm);
  color: var(--ink-tertiary);
  margin-bottom: 24px;
  min-height: 20px;
  overflow-wrap: anywhere;
}

.crumbs__sep {
  color: var(--line-strong);
}

.crumbs__link {
  color: var(--ink-tertiary);
  transition: color var(--dur-press) var(--ease-out);
}

.crumbs__link:hover {
  color: var(--ink);
}

.crumbs__current {
  color: var(--ink-secondary);
}
</style>
