<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useSession } from '../composables/useSession'
import UiIcon from './ui/UiIcon.vue'

const { user, logout } = useSession()

const open = ref(false)
const trigger = ref<HTMLButtonElement | null>(null)
const menu = ref<HTMLDivElement | null>(null)
const position = ref({ bottom: 0, left: 0 })

function toggle() {
  if (open.value) {
    close()
    return
  }
  const rect = trigger.value?.getBoundingClientRect()
  if (rect) {
    position.value = {
      bottom: window.innerHeight - rect.top + 8,
      left: Math.min(rect.left, window.innerWidth - 200),
    }
  }
  open.value = true
}

function close() {
  open.value = false
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') close()
}

function onPointerdown(event: PointerEvent) {
  if (!open.value) return
  const target = event.target as Node
  if (menu.value?.contains(target) || trigger.value?.contains(target)) return
  close()
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  document.addEventListener('pointerdown', onPointerdown)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.removeEventListener('pointerdown', onPointerdown)
})

async function signOut() {
  close()
  await logout()
}
</script>

<template>
  <div v-if="user" class="account">
    <button ref="trigger" class="account__trigger" type="button" @click="toggle">
      <span class="account__email">{{ user.email }}</span>
      <UiIcon
        name="chevron-down"
        :size="13"
        class="account__chevron"
        :class="{ 'account__chevron--open': open }"
      />
    </button>

    <Teleport to="body">
      <Transition name="account-menu">
        <div
          v-if="open"
          ref="menu"
          class="account__menu"
          role="menu"
          :style="{ bottom: `${position.bottom}px`, left: `${position.left}px` }"
        >
          <button class="account__item" role="menuitem" type="button" @click="signOut">
            <UiIcon name="sign-out" :size="14" />
            sign out
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.account__trigger {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-sm);
  color: var(--ink-tertiary);
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  transition: color var(--dur-press) var(--ease-out);
}

.account__trigger::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: inherit;
}

.account__trigger:hover {
  color: var(--ink);
}

.account__email {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-transform: lowercase;
}

.account__chevron {
  transition: transform var(--dur-state) var(--ease-out);
}

.account__chevron--open {
  transform: rotate(180deg);
}

.account__menu {
  position: fixed;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-modal);
  padding: 6px 0;
  z-index: 70;
}

.account__item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  font-size: var(--text-sm);
  color: var(--ink);
  border-radius: var(--radius-sm);
  margin: 0 6px;
  line-height: 1;
  transition: background-color var(--dur-press) var(--ease-out);
}

.account__item:hover {
  background: var(--surface-muted);
}

.account-menu-leave-active {
  transition: opacity 120ms var(--ease-in);
}

.account-menu-leave-to {
  opacity: 0;
}
</style>
