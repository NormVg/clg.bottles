<script setup lang="ts">
const emit = defineEmits<{
  'add-link': []
  upload: []
  'new-folder': []
  search: []
}>()
</script>

<template>
  <Teleport to="body">
    <footer class="footer">
      <div class="footer__side">
        <span class="footer__space">bookmarks</span>
      </div>
      <nav class="footer__utils" aria-label="actions">
        <button class="footer__util" type="button" @click="emit('add-link')">
          new link <kbd>n</kbd>
        </button>
        <span class="footer__dot" aria-hidden="true">·</span>
        <button class="footer__util" type="button" @click="emit('upload')">
          upload <kbd>u</kbd>
        </button>
        <span class="footer__dot" aria-hidden="true">·</span>
        <button class="footer__util" type="button" @click="emit('new-folder')">
          new folder <kbd>f</kbd>
        </button>
        <span class="footer__dot" aria-hidden="true">·</span>
        <button class="footer__util footer__util--search" type="button" @click="emit('search')">
          search <kbd>/</kbd>
        </button>
      </nav>
    </footer>
  </Teleport>
</template>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: min(680px, calc(100% - 48px));
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 24px 0 28px;
  background: var(--bg);
  z-index: 20;
}

.footer__side {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footer__space {
  font-size: var(--text-sm);
  color: var(--ink);
  padding: 4px 1px;
}

.footer__utils {
  display: flex;
  align-items: center;
  gap: 3px;
  flex-wrap: wrap;
}

.footer__util {
  position: relative;
  font-size: var(--text-sm);
  color: var(--ink-tertiary);
  padding: 6px 7px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: color var(--dur-press) var(--ease-out);
}

.footer__util::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: inherit;
}

.footer__util:hover {
  color: var(--ink);
}

.footer__dot {
  color: var(--line-strong);
  font-size: var(--text-sm);
}

.footer__util kbd {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-secondary);
  line-height: 1.5;
  box-shadow: inset 0 -1px 0 var(--line-strong);
}

.footer__util:hover kbd {
  color: var(--ink);
}

@media (max-width: 900px) {
  .footer__util kbd {
    display: none;
  }
}

@media (max-width: 680px) {
  .footer {
    flex-wrap: wrap;
    padding: 18px 0 22px;
  }

  .footer__utils {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
