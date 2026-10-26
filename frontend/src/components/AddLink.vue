<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../api'
import { useToast } from '../composables/useToast'
import type { ApiItem } from '../types'
import FolderPicker from './FolderPicker.vue'
import UiButton from './ui/UiButton.vue'
import UiInput from './ui/UiInput.vue'

const props = defineProps<{
  path: string
}>()

const emit = defineEmits<{
  close: []
  saved: [item: ApiItem]
}>()

const { push } = useToast()

const url = ref('')
const path = ref('')
const title = ref('')
const saving = ref(false)
const error = ref<string | null>(null)

async function save() {
  error.value = null

  try {
    const normalized = url.value.startsWith('http') ? url.value : `https://${url.value}`
    new URL(normalized)

    saving.value = true
    const item = await api.createLink({
      url: normalized,
      path: path.value.trim() || props.path,
      title: title.value.trim() || undefined,
    })
    push('saved.')
    emit('saved', item)
  } catch (cause) {
    if (cause instanceof TypeError) {
      error.value = 'that does not look like a url.'
    } else {
      error.value = cause instanceof Error ? cause.message : 'could not save.'
    }
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="form" @submit.prevent="save">
    <UiInput
      v-model="url"
      label="url"
      placeholder="piedpiper.com/handbook"
      autofocus
      :required="true"
      :error="error ?? undefined"
    />
    <FolderPicker v-model="path" :placeholder="props.path" hint="missing folders are created" />
    <UiInput v-model="title" label="title" placeholder="taken from the url" />

    <div class="form__actions">
      <UiButton variant="ghost" @click="emit('close')">cancel</UiButton>
      <UiButton type="submit" :loading="saving" :disabled="!url.trim()">save</UiButton>
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
