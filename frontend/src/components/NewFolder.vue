<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../api'
import { useToast } from '../composables/useToast'
import type { ApiFolder } from '../types'
import FolderPicker from './FolderPicker.vue'
import UiButton from './ui/UiButton.vue'

const props = defineProps<{
  path: string
}>()

const emit = defineEmits<{
  close: []
  saved: [folder: ApiFolder]
}>()

const { push } = useToast()

const path = ref('')
const saving = ref(false)
const error = ref<string | null>(null)

const placeholder = computed(() => (props.path === '/' ? '/design/inspo' : `${props.path}/inspo`))

async function save() {
  error.value = null
  try {
    saving.value = true
    const folder = await api.createFolder(path.value.trim())
    push('created.')
    emit('saved', folder)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'could not create.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="form" @submit.prevent="save">
    <FolderPicker
      v-model="path"
      :placeholder="placeholder"
      autofocus
      mono
      hint="missing folders along the way are created"
      :error="error ?? undefined"
    />
    <div class="form__actions">
      <UiButton variant="ghost" @click="emit('close')">cancel</UiButton>
      <UiButton type="submit" :loading="saving" :disabled="!path.trim()">create</UiButton>
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
