<script setup lang="ts">
import { computed } from 'vue'
import type { ApiDirectory, ApiItem } from '../types'
import Row from './Row.vue'
import UiButton from './ui/UiButton.vue'
import UiEmpty from './ui/UiEmpty.vue'
import UiSkeleton from './ui/UiSkeleton.vue'

const props = defineProps<{
  directory: ApiDirectory | null
  loading: boolean
  error: string | null
  path: string
}>()

const emit = defineEmits<{
  'open-folder': [path: string]
  'view-media': [item: ApiItem]
  changed: []
  'new-link': []
}>()

const isEmpty = computed(
  () =>
    props.directory !== null &&
    props.directory.folders.length === 0 &&
    props.directory.items.length === 0,
)

const skeletons = [58, 42, 66, 50, 62]
</script>

<template>
  <div v-if="loading" class="browser__skeletons fade-in" aria-busy="true" aria-label="loading">
    <div v-for="(width, index) in skeletons" :key="index" class="browser__skeleton-row">
      <UiSkeleton height="17px" :width="`${width}%`" />
    </div>
  </div>

  <UiEmpty v-else-if="error" :text="error">
    <UiButton variant="ghost" @click="emit('changed')">try again</UiButton>
  </UiEmpty>

  <UiEmpty
    v-else-if="isEmpty"
    :text="path === '/' ? 'nothing saved yet.' : 'this folder is empty.'"
  >
    <UiButton @click="emit('new-link')">new link</UiButton>
  </UiEmpty>

  <ul v-else-if="directory" class="browser__list stagger" aria-label="folder contents">
    <Row
      v-for="(folder, index) in directory.folders"
      :key="folder.id"
      :folder="folder"
      :index="index"
      @open-folder="emit('open-folder', $event)"
      @changed="emit('changed')"
    />
    <Row
      v-for="(item, index) in directory.items"
      :key="item.id"
      :item="item"
      :index="directory.folders.length + index"
      @view-media="emit('view-media', $event)"
      @changed="emit('changed')"
    />
  </ul>
</template>

<style scoped>
.browser__list {
  list-style: none;
  border-top: 1px solid var(--line);
}

.browser__skeletons {
  display: flex;
  flex-direction: column;
}

.browser__skeleton-row {
  display: flex;
  align-items: center;
  min-height: 60px;
  border-bottom: 1px solid var(--line);
}
</style>
