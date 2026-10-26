<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useId } from 'vue'
import { api } from '../api'
import type { ApiFolder } from '../types'
import UiIcon from './ui/UiIcon.vue'
import UiInput from './ui/UiInput.vue'

const props = withDefaults(
  defineProps<{
    modelValue: string
    label?: string
    placeholder?: string
    hint?: string
    error?: string
    mono?: boolean
    autofocus?: boolean
    limit?: number
  }>(),
  { label: 'path', limit: 8 },
)

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const root = ref<HTMLDivElement | null>(null)
const list = ref<HTMLUListElement | null>(null)
const open = ref(false)
const folders = ref<ApiFolder[]>([])
const loaded = ref(false)
const failed = ref(false)
const activeIndex = ref(0)
const position = ref({ top: 0, left: 0, width: 240 })
const listId = useId()

const trimmed = computed(() => props.modelValue.trim())
const matches = computed(() => {
  const query = trimmed.value.toLowerCase()
  const source = query
    ? folders.value.filter((folder) => folder.path.toLowerCase().includes(query))
    : folders.value
  return source.slice(0, props.limit)
})
const createsNew = computed(
  () => trimmed.value !== '' && !folders.value.some((folder) => folder.path === trimmed.value),
)
const options = computed(() => {
  const existing = matches.value.map((folder) => ({ value: folder.path, isNew: false }))
  return createsNew.value ? [...existing, { value: trimmed.value, isNew: true }] : existing
})
const expanded = computed(() => open.value && options.value.length > 0)
const activeId = computed(() => (expanded.value ? `${listId}-option-${activeIndex.value}` : undefined))
function place() {
  const rect = root.value?.getBoundingClientRect()
  if (rect) {
    position.value = { top: rect.bottom + 6, left: rect.left, width: Math.min(rect.width, 320) }
  }
}

async function onOpen() {
  if (failed.value) return
  open.value = true
  activeIndex.value = 0
  place()
  if (loaded.value) return
  try {
    folders.value = await api.folders()
    loaded.value = true
  } catch {
    failed.value = true
    open.value = false
  }
}

function close() {
  open.value = false
}

function select(value: string) {
  emit('update:modelValue', value)
  close()
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape' && expanded.value) {
    event.preventDefault()
    event.stopPropagation()
    close()
    return
  }
  if (!expanded.value || options.value.length === 0) return
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    activeIndex.value = (activeIndex.value + 1) % options.value.length
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    activeIndex.value = (activeIndex.value - 1 + options.value.length) % options.value.length
  } else if (event.key === 'Enter') {
    event.preventDefault()
    select(options.value[activeIndex.value]!.value)
  }
}

function onInput(value: string) {
  emit('update:modelValue', value)
  activeIndex.value = 0
  if (!open.value && !failed.value) void onOpen()
}

function onPointerdown(event: PointerEvent) {
  if (!open.value) return
  const target = event.target as Node
  if (root.value?.contains(target) || list.value?.contains(target)) return
  close()
}

onMounted(() => document.addEventListener('pointerdown', onPointerdown))
onBeforeUnmount(() => document.removeEventListener('pointerdown', onPointerdown))
</script>

<template>
  <div ref="root" class="picker">
    <UiInput
      :model-value="modelValue"
      :label="label"
      :placeholder="placeholder"
      :hint="hint"
      :error="error"
      :mono="mono"
      :autofocus="autofocus"
      role="combobox"
      aria-autocomplete="list"
      :aria-expanded="expanded"
      :aria-controls="listId"
      :aria-activedescendant="activeId"
      @update:model-value="onInput"
      @focus="onOpen"
      @keydown="onKeydown"
    />

    <Teleport to="body">
      <Transition name="picker-menu">
        <ul
          v-if="expanded"
          :id="listId"
          ref="list"
          class="picker__list"
          role="listbox"
          :aria-label="label"
          :style="{ top: `${position.top}px`, left: `${position.left}px`, width: `${position.width}px` }"
        >
          <li
            v-for="(option, index) in options"
            :id="`${listId}-option-${index}`"
            :key="option.value"
            class="picker__option"
            :class="{ 'picker__option--active': index === activeIndex }"
            role="option"
            :aria-selected="index === activeIndex"
            @mousedown.prevent
            @click="select(option.value)"
          >
            <UiIcon :name="option.isNew ? 'create' : 'folder'" :size="13" />
            <span class="picker__path mono">{{ option.value }}</span>
          </li>
        </ul>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.picker { position: relative; }
.picker__list {
  position: fixed;
  max-height: 264px;
  overflow-y: auto;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-modal);
  padding: 6px 0;
  z-index: 70;
}
.picker__option {
  display: flex;
  align-items: center;
  gap: 8px;
  width: calc(100% - 12px);
  padding: 8px 12px;
  font-size: var(--text-sm);
  color: var(--ink);
  border-radius: var(--radius-sm);
  margin: 0 6px;
  line-height: 1;
  cursor: pointer;
}
.picker__option--active { background: var(--surface-muted); }
.picker__path { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.picker-menu-leave-active { transition: opacity 120ms var(--ease-in); }
.picker-menu-leave-to { opacity: 0; }
</style>
