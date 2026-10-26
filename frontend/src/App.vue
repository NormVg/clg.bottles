<script setup lang="ts">
import { onMounted, ref } from 'vue'

type BackendStatus = 'checking' | 'up' | 'down'

const status = ref<BackendStatus>('checking')

onMounted(async () => {
  try {
    const response = await fetch('/api/health')
    const data = (await response.json()) as { status?: string }
    status.value = response.ok && data.status === 'ok' ? 'up' : 'down'
  } catch {
    status.value = 'down'
  }
})
</script>

<template>
  <main>
    <h1>clg.bottles</h1>
    <p>
      Backend:
      <span class="status" :class="status" />
      <strong>
        {{ status === 'checking' ? 'checking' : status === 'up' ? 'connected' : 'not reachable' }}
      </strong>
    </p>
    <p class="hint">
      Start the API from <code>backend/</code> with
      <code>uvicorn app.main:app --reload</code>.
    </p>
  </main>
</template>

<style scoped>
h1 {
  color: var(--text-h);
  margin: 0 0 12px;
}

.status {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 6px;
  border-radius: 50%;
  background: var(--text);
}

.status.up {
  background: #3ecf8e;
}

.status.down {
  background: #e5484d;
}

.hint {
  color: var(--text);
}

code {
  font-family: ui-monospace, Consolas, monospace;
  background: var(--code-bg);
  border-radius: 4px;
  padding: 2px 6px;
}
</style>
