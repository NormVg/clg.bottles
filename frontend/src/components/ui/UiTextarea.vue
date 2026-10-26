<script setup lang="ts">
import { onMounted, ref, toRefs } from 'vue'

defineOptions({ inheritAttrs: false })

const props = withDefaults(
  defineProps<{
    modelValue: string
    label?: string
    placeholder?: string
    hint?: string
    error?: string
    autofocus?: boolean
    rows?: number
    required?: boolean
  }>(),
  {
    rows: 5,
    required: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const { autofocus } = toRefs(props)
const root = ref<HTMLTextAreaElement | null>(null)

onMounted(() => {
  if (autofocus.value) root.value?.focus()
})

function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLTextAreaElement).value)
}
</script>

<template>
  <label class="ui-field" :class="{ 'ui-field--invalid': error }">
    <span v-if="label" class="ui-field__label">{{ label }}</span>
    <textarea
      ref="root"
      v-bind="$attrs"
      class="ui-field__input"
      :value="modelValue"
      :placeholder="placeholder"
      :rows="rows"
      :required="required"
      :aria-invalid="error ? true : undefined"
      spellcheck="false"
      @input="onInput"
    />
    <span v-if="error" class="ui-field__error" role="alert">{{ error }}</span>
    <span v-else-if="hint" class="ui-field__hint">{{ hint }}</span>
  </label>
</template>

<style scoped>
.ui-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ui-field__label {
  font-size: var(--text-xs);
  color: var(--ink-secondary);
  letter-spacing: 0.02em;
}

.ui-field__input {
  border: none;
  border-bottom: 1px solid var(--line-strong);
  background: transparent;
  padding: 6px 0;
  font-size: var(--text-base);
  border-radius: 0;
  resize: vertical;
  min-height: 96px;
  line-height: 1.6;
  transition: border-color var(--dur-press) var(--ease-out);
}

.ui-field__input::placeholder {
  color: var(--ink-tertiary);
}

.ui-field__input:focus {
  outline: none;
  border-bottom-color: var(--ink);
}

.ui-field--invalid .ui-field__input {
  border-bottom-color: var(--danger-ink);
}

.ui-field__hint,
.ui-field__error {
  font-size: var(--text-xs);
  color: var(--ink-tertiary);
}

.ui-field__error {
  color: var(--danger-ink);
}
</style>
