<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { api } from '../api'
import { useQuickCapture } from '../composables/useQuickCapture'
import { useWindowDropZone } from '../composables/useWindowDropZone'
import type { ApiDirectory, ApiItem } from '../types'
import AddLink from './AddLink.vue'
import AddNote from './AddNote.vue'
import Breadcrumb from './Breadcrumb.vue'
import DirectoryList from './DirectoryList.vue'
import DropOverlay from './DropOverlay.vue'
import Footer from './Footer.vue'
import MediaViewer from './MediaViewer.vue'
import NewFolder from './NewFolder.vue'
import Search from './Search.vue'
import Surface from './Surface.vue'
import Upload from './Upload.vue'

const path = defineModel<string>('path', { default: '/' })

const directory = ref<ApiDirectory | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const surface = ref<'list' | 'new-link' | 'new-note' | 'upload' | 'new-folder' | 'media'>('list')
const mediaItem = ref<ApiItem | null>(null)
const searchOpen = ref(false)

const mediaTitle = computed(() => mediaItem.value?.title ?? 'file')
const captureEnabled = computed(() => surface.value === 'list' && !searchOpen.value)

async function refresh() {
  loading.value = true
  error.value = null
  try {
    directory.value = await api.directory(path.value)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'could not load this folder.'
    directory.value = null
  } finally {
    loading.value = false
  }
}

watch(path, refresh, { immediate: true })

function openFolder(next: string) {
  surface.value = 'list'
  path.value = next
}

function openMedia(item: ApiItem) {
  mediaItem.value = item
  surface.value = 'media'
}

function onSaved() {
  surface.value = 'list'
  void refresh()
}

const { captureFiles } = useQuickCapture(path, () => void refresh(), captureEnabled)
const { dragging } = useWindowDropZone(captureFiles, captureEnabled)

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape' && surface.value !== 'list') {
    surface.value = 'list'
    return
  }
  if (searchOpen.value || surface.value !== 'list') return
  if (event.altKey || event.ctrlKey || event.metaKey) return
  if (!/^[ntuf/]$/.test(event.key)) return
  const target = event.target as HTMLElement
  if (target.closest('input, textarea')) return
  event.preventDefault()
  if (event.key === '/') searchOpen.value = true
  else if (event.key === 'n') surface.value = 'new-link'
  else if (event.key === 't') surface.value = 'new-note'
  else if (event.key === 'u') surface.value = 'upload'
  else surface.value = 'new-folder'
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div class="browser">
    <Breadcrumb v-if="path !== '/'" :path="path" @navigate="openFolder" />

    <Transition name="surface-swap" mode="out-in">
      <div :key="surface" class="browser__canvas">
        <Surface v-if="surface === 'new-link'" title="new link" @close="surface = 'list'">
          <AddLink :path="path" @close="surface = 'list'" @saved="onSaved" />
        </Surface>

        <Surface v-else-if="surface === 'new-note'" title="new note" @close="surface = 'list'">
          <AddNote :path="path" @close="surface = 'list'" @saved="onSaved" />
        </Surface>

        <Surface v-else-if="surface === 'upload'" title="upload" @close="surface = 'list'">
          <Upload :path="path" @close="surface = 'list'" @saved="onSaved" />
        </Surface>

        <Surface v-else-if="surface === 'new-folder'" title="new folder" @close="surface = 'list'">
          <NewFolder :path="path" @close="surface = 'list'" @saved="onSaved" />
        </Surface>

        <Surface v-else-if="surface === 'media'" :title="mediaTitle" @close="surface = 'list'">
          <MediaViewer v-if="mediaItem" :item="mediaItem" @close="surface = 'list'" />
        </Surface>

        <DirectoryList
          v-else
          :directory="directory"
          :loading="loading"
          :error="error"
          :path="path"
          @open-folder="openFolder"
          @view-media="openMedia"
          @changed="refresh"
          @new-link="surface = 'new-link'"
        />
      </div>
    </Transition>

    <Footer
      @add-link="surface = 'new-link'"
      @add-note="surface = 'new-note'"
      @upload="surface = 'upload'"
      @new-folder="surface = 'new-folder'"
      @search="searchOpen = true"
    />

    <Search
      v-if="searchOpen"
      @close="searchOpen = false"
      @open-folder="openFolder"
      @view-media="openMedia"
    />

    <DropOverlay v-if="dragging" :path="path" />
  </div>
</template>

<style scoped>
.browser {
  width: 100%;
  display: flex;
  flex-direction: column;
}

@media (prefers-reduced-motion: reduce) {
  .surface-swap-enter-active,
  .surface-swap-leave-active {
    transition: none;
  }
}
</style>
