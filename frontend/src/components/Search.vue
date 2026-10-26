<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import { api } from '../api'
import type { ApiItem, ApiSearchResult } from '../types'
import Row from './Row.vue'
import UiIcon from './ui/UiIcon.vue'

const emit = defineEmits<{
  close: []
  'open-folder': [path: string]
  'view-media': [item: ApiItem]
}>()

const query = ref('')
const results = shallowRef<ApiSearchResult | null>(null)
const searching = ref(false)
const input = ref<HTMLInputElement | null>(null)

let timer: ReturnType<typeof setTimeout> | undefined

watch(query, (value) => {
  clearTimeout(timer)
  const q = value.trim()
  if (!q) {
    results.value = null
    return
  }
  timer = setTimeout(async () => {
    searching.value = true
    try {
      results.value = await api.search(q)
    } catch {
      results.value = { items: [], folders: [] }
    } finally {
      searching.value = false
    }
  }, 200)
})

onMounted(() => {
  input.value?.focus()
  window.addEventListener('keydown', onKeydown)
})
onBeforeUnmount(() => {
  clearTimeout(timer)
  window.removeEventListener('keydown', onKeydown)
})

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') emit('close')
}

function openFolder(path: string) {
  emit('close')
  emit('open-folder', path)
}
function openMedia(item: ApiItem) {
  emit('close')
  emit('view-media', item)
}

const total = computed(() =>
  results.value ? results.value.folders.length + results.value.items.length : 0,
)
</script>

<template>
  <Teleport to="body">
    <Transition name="search">
      <div class="search" role="dialog" aria-modal="true" aria-label="search">
        <div class="search__column">
          <div class="search__bar slide-up">
            <UiIcon name="search" :size="16" class="search__icon" />
            <input
              ref="input"
              v-model="query"
              class="search__input"
              type="search"
              placeholder="search everything..."
              aria-label="search"
              autocomplete="off"
              spellcheck="false"
            />
            <kbd class="search__esc">esc</kbd>
          </div>

          <div class="search__results">
            <p v-if="searching" class="search__status">searching...</p>
            <p v-else-if="query.trim() && results && total === 0" class="search__status">
              nothing found.
            </p>

            <ul v-if="results" class="stagger search__list">
              <Row
                v-for="(folder, index) in results.folders"
                :key="`f-${folder.id}`"
                :folder="folder"
                :index="index"
                @open-folder="openFolder"
              />
              <Row
                v-for="(item, index) in results.items"
                :key="`i-${item.id}`"
                :item="item"
                :index="results.folders.length + index"
                @view-media="openMedia"
              />
            </ul>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.search {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: var(--bg);
  overflow-y: auto;
}

.search__column {
  width: 100%;
  max-width: 680px;
  margin: 0 auto;
  padding: 15vh 24px 48px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.search__bar {
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--line-strong);
  padding: 8px 0;
}

.search__icon {
  color: var(--ink-tertiary);
}

.search__input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: var(--text-lg);
  padding: 4px 0;
}

.search__input:focus {
  outline: none;
}

.search__input::placeholder {
  color: var(--ink-tertiary);
}

.search__input::-webkit-search-cancel-button {
  display: none;
}

.search__esc {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-tertiary);
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface-muted);
  padding: 0 5px;
  line-height: 1.5;
}

.search__status {
  color: var(--ink-tertiary);
  font-size: var(--text-base);
}

.search__list {
  list-style: none;
  border-top: 1px solid var(--line);
}

.search-enter-active {
  transition: opacity var(--dur-state) var(--ease-out);
}

.search-leave-active {
  transition: opacity 150ms var(--ease-in);
}

.search-enter-from,
.search-leave-to {
  opacity: 0;
}
</style>
