<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../api'
import { useToast } from '../composables/useToast'
import type { ApiFolder, ApiItem } from '../types'
import UiButton from './ui/UiButton.vue'
import UiInput from './ui/UiInput.vue'

const props = defineProps<{
  folder?: ApiFolder
  item?: ApiItem
  confirming: boolean
}>()

const emit = defineEmits<{
  close: []
  changed: []
}>()

const { push } = useToast()

const editTitle = ref((props.item?.title ?? props.folder?.name ?? '').trim())
const editUrl = ref(props.item?.url ?? '')
const saving = ref(false)
const deleting = ref(false)
const editError = ref<string | null>(null)

const isLink = computed(() => props.item?.type === 'link')

const normalizedEditUrl = computed(() => {
  const value = editUrl.value.trim()
  return value && !/^https?:\/\//i.test(value) ? `https://${value}` : value
})

const canSave = computed(
  () => editTitle.value.trim() !== '' && (!isLink.value || normalizedEditUrl.value !== ''),
)

const confirmText = computed(() => {
  const name = props.folder?.name ?? props.item?.title ?? ''
  return props.folder ? `delete "${name}" and everything inside it?` : `delete "${name}"?`
})

async function save() {
  editError.value = null
  const title = editTitle.value.trim()
  if (!title) {
    editError.value = 'give it a name.'
    return
  }
  if (isLink.value) {
    try {
      new URL(normalizedEditUrl.value)
    } catch {
      editError.value = 'that does not look like a url.'
      return
    }
  }

  try {
    saving.value = true
    if (props.folder) {
      await api.renameFolder(props.folder.id, title)
    } else if (props.item) {
      await api.updateItem(props.item.id, {
        title,
        ...(isLink.value ? { url: normalizedEditUrl.value } : {}),
      })
    }
    push('renamed.')
    emit('changed')
    emit('close')
  } catch (cause) {
    editError.value = cause instanceof Error ? cause.message : 'could not rename.'
  } finally {
    saving.value = false
  }
}

async function remove() {
  try {
    deleting.value = true
    if (props.folder) {
      await api.deleteFolder(props.folder.id)
    } else if (props.item) {
      await api.deleteItem(props.item.id)
    }
    push('deleted.')
    emit('changed')
    emit('close')
  } catch (cause) {
    push(cause instanceof Error ? cause.message : 'could not delete.', 'danger')
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <form
    v-if="!confirming"
    class="row__edit"
    @submit.prevent="save"
    @keydown.escape.stop="emit('close')"
  >
    <UiInput
      v-model="editTitle"
      label="title"
      autofocus
      :error="editError && !isLink ? editError : undefined"
    />
    <UiInput
      v-if="isLink"
      v-model="editUrl"
      label="url"
      :error="editError && isLink ? editError : undefined"
    />
    <div class="row__edit-actions">
      <UiButton variant="ghost" size="sm" type="button" @click="emit('close')">cancel</UiButton>
      <UiButton type="submit" size="sm" :loading="saving" :disabled="!canSave">save</UiButton>
    </div>
  </form>

  <div v-else class="row__confirm" @keydown.escape.stop="emit('close')">
    <span class="row__confirm-text">{{ confirmText }}</span>
    <div class="row__confirm-actions">
      <UiButton variant="ghost" size="sm" @click="emit('close')">cancel</UiButton>
      <UiButton variant="danger" size="sm" :loading="deleting" @click="remove">delete</UiButton>
    </div>
  </div>
</template>
