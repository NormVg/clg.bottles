<script setup lang="ts">
import { computed } from 'vue'
import { useToast } from '../composables/useToast'
import type { ApiItem } from '../types'
import { formatBytes } from '../utils/format'
import UiButton from './ui/UiButton.vue'
import UiIcon from './ui/UiIcon.vue'

const props = defineProps<{
  item: ApiItem
}>()

const emit = defineEmits<{
  close: []
}>()

const { push } = useToast()

const media = computed(() => props.item.media)
const isImage = computed(() => (media.value?.mime_type ?? '').startsWith('image/'))
const rawUrl = computed(() => (media.value ? `/api/media/${media.value.id}/raw` : null))
const downloadUrl = computed(() => (media.value ? `/api/media/${media.value.id}/download` : null))

function copyUrl() {
  if (!rawUrl.value) return
  navigator.clipboard
    .writeText(window.location.origin + rawUrl.value)
    .then(() => push('copied.'))
    .catch(() => push('select and copy it manually.', 'danger'))
}

function download() {
  if (downloadUrl.value) window.location.href = downloadUrl.value
}
</script>

<template>
  <div class="viewer">
    <p v-if="!media" class="viewer__missing" role="alert">could not load the file.</p>

    <figure v-else-if="isImage" class="viewer__figure">
      <img class="viewer__image" :src="rawUrl ?? undefined" :alt="props.item.title" />
      <figcaption class="viewer__meta">
        {{ media.filename }} · {{ formatBytes(media.size) }}
      </figcaption>
    </figure>

    <div v-else class="viewer__file">
      <UiIcon name="file" :size="20" class="viewer__file-icon" />
      <span class="viewer__filename">{{ media.filename }}</span>
      <span class="viewer__filesize">{{ formatBytes(media.size) }}</span>
    </div>

    <div class="viewer__actions">
      <UiButton variant="ghost" :disabled="!rawUrl" @click="copyUrl">
        <UiIcon name="copy" :size="13" />
        copy url
      </UiButton>
      <UiButton :disabled="!downloadUrl" @click="download">
        <UiIcon name="download" :size="13" />
        download
      </UiButton>
    </div>
  </div>
</template>

<style scoped>
.viewer__missing {
  font-size: var(--text-sm);
  color: var(--ink-secondary);
}

.viewer__figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.viewer__image {
  display: block;
  max-width: 100%;
  max-height: 60vh;
  border-radius: var(--radius-md);
  object-fit: contain;
}

.viewer__meta {
  font-size: var(--text-xs);
  color: var(--ink-tertiary);
}

.viewer__file {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px 24px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius-lg);
  color: var(--ink-secondary);
}

.viewer__file-icon {
  color: var(--ink-tertiary);
}

.viewer__filename {
  font-size: var(--text-sm);
  color: var(--ink);
  overflow-wrap: anywhere;
}

.viewer__filesize {
  font-size: var(--text-xs);
  color: var(--ink-tertiary);
}

.viewer__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 20px;
}
</style>
