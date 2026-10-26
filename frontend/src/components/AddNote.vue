<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../api'
import { useToast } from '../composables/useToast'
import type { ApiItem } from '../types'
import FolderPicker from './FolderPicker.vue'
import UiButton from './ui/UiButton.vue'
import UiInput from './ui/UiInput.vue'
import UiTextarea from './ui/UiTextarea.vue'

const props = defineProps<{
  path: string
}>()

const emit = defineEmits<{
  close: []
  saved: [item: ApiItem]
}>()

const { push } = useToast()

const title = ref('')
const note = ref('')
const path = ref('')
const saving = ref(false)
const error = ref<string | null>(null)

async function save() {
  error.value = null
  if (!note.value.trim()) {
    error.value = 'write something first.'
    return
  }

  try {
    saving.value = true
    const item = await api.createNote({
      note: note.value.trim(),
      path: path.value.trim() || props.path,
      title: title.value.trim() || undefined,
    })
    push('noted.')
    emit('saved', item)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'could not save.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="form" @submit.prevent="save">
    <UiInput v-model="title" label="title" placeholder="a short name" autofocus />
    <UiTextarea
      v-model="note"
      label="text"
      placeholder="paste or write the text to keep"
      :error="error ?? undefined"
      :rows="6"
    />
    <FolderPicker v-model="path" :placeholder="props.path" hint="missing folders are created" />

    <div class="form__actions">
      <UiButton variant="ghost" @click="emit('close')">cancel</UiButton>
      <UiButton type="submit" :loading="saving" :disabled="!note.trim()">save</UiButton>
    </div>
  </form>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>
