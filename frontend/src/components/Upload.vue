<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../api'
import { useToast } from '../composables/useToast'
import type { ApiItem } from '../types'
import FolderPicker from './FolderPicker.vue'
import UiButton from './ui/UiButton.vue'
import UiIcon from './ui/UiIcon.vue'
import UiInput from './ui/UiInput.vue'

const props = defineProps<{ path: string }>()
const emit = defineEmits<{ close: []; saved: [item: ApiItem] }>()
const { push } = useToast()

const file = ref<File | null>(null)
const path = ref('')
const title = ref('')
const dragging = ref(false)
const input = ref<HTMLInputElement | null>(null)
const saving = ref(false)
const error = ref<string | null>(null)
const progress = ref<number | null>(null)

const MAX_BYTES = 25 * 1024 * 1024

function pick(list: FileList | null) {
  const picked = list?.[0]
  if (!picked) return
  if (picked.size > MAX_BYTES) {
    error.value = 'files up to 25 mb are supported.'
    return
  }
  error.value = null
  file.value = picked
  if (!title.value) title.value = picked.name
}

function onDrop(event: DragEvent) {
  dragging.value = false
  pick(event.dataTransfer?.files ?? null)
}

function onDragLeave(event: DragEvent) {
  const zone = event.currentTarget
  if (zone instanceof Node && event.relatedTarget instanceof Node && zone.contains(event.relatedTarget)) {
    return
  }
  dragging.value = false
}

function browse() {
  input.value?.click()
}

async function save() {
  if (!file.value) {
    error.value = 'choose a file first.'
    return
  }
  const picked = file.value
  error.value = null
  progress.value = 0
  try {
    saving.value = true
    const result = await api.upload(
      picked,
      path.value.trim() || props.path,
      title.value.trim() || undefined,
      (fraction) => {
        progress.value = fraction
      },
    )
    push('uploaded.')
    emit('saved', result.item)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'could not upload.'
  } finally {
    saving.value = false
    progress.value = null
  }
}
</script>

<template>
  <form class="form" @submit.prevent="save">
    <button
      type="button"
      class="form__drop"
      :class="{ 'form__drop--active': dragging, 'form__drop--filled': file }"
      @click="browse"
      @dragover.prevent="dragging = true"
      @dragleave="onDragLeave"
      @drop.prevent="onDrop"
    >
      <UiIcon name="upload" :size="18" />
      <span v-if="file" class="form__filename">{{ file.name }}</span>
      <span v-else>drop a file here, or browse</span>
    </button>
    <input
      ref="input"
      type="file"
      class="form__file-input"
      aria-label="choose a file"
      @change="pick(($event.target as HTMLInputElement).files)"
    />

    <FolderPicker v-model="path" :placeholder="props.path" hint="missing folders are created" />
    <UiInput v-model="title" label="title" placeholder="taken from the filename" />

    <div v-if="progress !== null" class="form__progress">
      <div
        class="form__progress-track"
        role="progressbar"
        aria-label="upload progress"
        :aria-valuenow="Math.round(progress * 100)"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div class="form__progress-fill" :style="{ transform: `scaleX(${progress})` }"></div>
      </div>
      <span class="form__progress-label">{{ Math.round(progress * 100) }}%</span>
    </div>

    <p v-if="error" class="form__error" role="alert">{{ error }}</p>

    <div class="form__actions">
      <UiButton variant="ghost" @click="emit('close')">cancel</UiButton>
      <UiButton type="submit" :loading="saving" :disabled="!file">upload</UiButton>
    </div>
  </form>
</template>

<style scoped>
.form { display: flex; flex-direction: column; gap: 16px; }
.form__drop {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 36px 24px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius-lg);
  color: var(--ink-tertiary);
  font-size: var(--text-sm);
  background: transparent;
  transition: border-color var(--dur-press) var(--ease-out),
    background-color var(--dur-press) var(--ease-out),
    color var(--dur-press) var(--ease-out);
}
.form__drop:hover,
.form__drop--active { border-color: var(--ink-tertiary); color: var(--ink-secondary); }
.form__drop--active { background: var(--surface-muted); }
.form__drop--filled { border-style: solid; color: var(--ink); }
.form__filename { font-size: var(--text-sm); overflow-wrap: anywhere; }
.form__progress { display: flex; align-items: center; gap: 10px; }
.form__progress-track {
  flex: 1;
  height: 2px;
  background: var(--line);
  border-radius: 1px;
  overflow: hidden;
}
.form__progress-fill {
  height: 100%;
  background: var(--ink);
  transform-origin: left center;
  transform: scaleX(0);
  transition: transform 180ms var(--ease-out);
}
.form__progress-label {
  font-variant-numeric: tabular-nums;
  font-size: var(--text-xs);
  color: var(--ink-tertiary);
  min-width: 3ch;
  text-align: right;
}
.form__file-input { display: none; }
.form__error { font-size: var(--text-xs); color: var(--danger-ink); }
.form__actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
</style>
