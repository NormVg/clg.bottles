<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '../composables/useToast'
import type { ApiFolder, ApiItem } from '../types'
import RowEditor from './RowEditor.vue'
import UiIcon from './ui/UiIcon.vue'

const props = defineProps<{
  folder?: ApiFolder
  item?: ApiItem
  index: number
}>()

const emit = defineEmits<{
  'open-folder': [path: string]
  'view-media': [item: ApiItem]
  changed: []
}>()

const { push } = useToast()

const expanded = ref(false)
const editing = ref(false)
const confirming = ref(false)

function startEdit() {
  confirming.value = false
  editing.value = true
}

function startDelete() {
  editing.value = false
  confirming.value = true
}

function closeEditor() {
  editing.value = false
  confirming.value = false
}

function copyLink() {
  const url = props.item?.url
  if (!url) return
  navigator.clipboard
    .writeText(url)
    .then(() => push('copied.'))
    .catch(() => push('select and copy it manually.', 'danger'))
}

function downloadMedia() {
  const media = props.item?.media
  if (!media) return
  window.location.href = `/api/media/${media.id}/download`
}
</script>

<template>
  <li class="row" :style="{ '--i': index }">
    <RowEditor
      v-if="editing || confirming"
      :folder="folder"
      :item="item"
      :confirming="confirming"
      @close="closeEditor"
      @changed="emit('changed')"
    />

    <div v-else-if="folder" class="row__inner">
      <button class="row__hit" type="button" @click="emit('open-folder', folder.path)">
        <span class="row__title">{{ folder.name }}</span>
        <span class="row__slash" aria-hidden="true">/</span>
      </button>
      <div class="row__side">
        <button class="row__action" type="button" aria-label="rename folder" @click.stop="startEdit">
          <UiIcon name="rename" :size="14" />
        </button>
        <button class="row__action" type="button" aria-label="delete folder" @click.stop="startDelete">
          <UiIcon name="delete" :size="14" />
        </button>
        <button
          class="row__arrow-button"
          type="button"
          aria-label="open folder"
          @click="emit('open-folder', folder.path)"
        >
          <UiIcon name="chevron-right" :size="16" class="row__arrow" />
        </button>
      </div>
    </div>

    <template v-else-if="item">
      <div v-if="item.type === 'note'" class="row__inner">
        <button
          class="row__hit"
          type="button"
          :aria-expanded="expanded"
          @click="expanded = !expanded"
        >
          <span class="row__title">{{ item.title }}</span>
        </button>
        <div class="row__side">
          <button class="row__action" type="button" aria-label="rename note" @click.stop="startEdit">
            <UiIcon name="rename" :size="14" />
          </button>
          <button class="row__action" type="button" aria-label="delete note" @click.stop="startDelete">
            <UiIcon name="delete" :size="14" />
          </button>
        </div>
      </div>
      <div v-if="item.type === 'note'" class="row__note" :class="{ 'row__note--open': expanded }">
        <div class="row__note-body">{{ item.note }}</div>
      </div>

      <div v-else class="row__inner">
        <button
          v-if="item.type === 'media'"
          class="row__hit"
          type="button"
          @click="emit('view-media', item)"
        >
          <span class="row__title">{{ item.title }}</span>
        </button>
        <a
          v-else
          class="row__hit"
          :href="item.url ?? undefined"
          target="_blank"
          rel="noopener noreferrer"
        >
          <span class="row__title">{{ item.title }}</span>
        </a>
        <div class="row__side">
          <button
            v-if="item.type === 'media'"
            class="row__action"
            type="button"
            aria-label="download file"
            @click.stop="downloadMedia"
          >
            <UiIcon name="download" :size="14" />
          </button>
          <button
            v-if="item.type === 'link'"
            class="row__action"
            type="button"
            aria-label="copy link"
            @click.stop="copyLink"
          >
            <UiIcon name="copy" :size="14" />
          </button>
          <button class="row__action" type="button" aria-label="rename item" @click.stop="startEdit">
            <UiIcon name="rename" :size="14" />
          </button>
          <button class="row__action" type="button" aria-label="delete item" @click.stop="startDelete">
            <UiIcon name="delete" :size="14" />
          </button>
          <a
            v-if="item.type === 'link'"
            class="row__arrow-button"
            :href="item.url ?? undefined"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="open link"
          >
            <UiIcon name="open-external" :size="16" class="row__arrow" />
          </a>
        </div>
      </div>
    </template>
  </li>
</template>

<style src="./row.css"></style>
