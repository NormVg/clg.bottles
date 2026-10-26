<script setup lang="ts">
import { ref } from 'vue'
import { useSession } from '../composables/useSession'
import UiButton from './ui/UiButton.vue'
import UiInput from './ui/UiInput.vue'

const emit = defineEmits<{
  done: []
  back: []
}>()

const { login, signup } = useSession()

const mode = ref<'login' | 'signup'>('login')
const name = ref('')
const email = ref('')
const password = ref('')
const saving = ref(false)
const error = ref<string | null>(null)

function switchMode() {
  mode.value = mode.value === 'login' ? 'signup' : 'login'
  error.value = null
}

async function submit() {
  error.value = null
  if (!email.value.trim() || !password.value) {
    error.value = 'email and password, please.'
    return
  }
  if (mode.value === 'signup' && !name.value.trim()) {
    error.value = 'a name, please.'
    return
  }

  try {
    saving.value = true
    if (mode.value === 'signup') {
      await signup({
        name: name.value.trim(),
        email: email.value.trim(),
        password: password.value,
      })
    } else {
      await login({ email: email.value.trim(), password: password.value })
    }
    emit('done')
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'could not sign in.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="login">
    <p class="login__eyebrow label rise" style="--i: 0">
      {{ mode === 'login' ? 'sign in' : 'create account' }}
    </p>
    <h1 class="login__title rise" style="--i: 1">
      {{ mode === 'login' ? 'welcome back.' : 'make a bottle.' }}
    </h1>
    <p class="login__sub rise" style="--i: 2">
      {{
        mode === 'login'
          ? 'your bottles open exactly as you left them.'
          : 'one account, your own quiet shelf.'
      }}
    </p>

    <form class="login__form rise" style="--i: 3" @submit.prevent="submit">
      <UiInput
        v-if="mode === 'signup'"
        v-model="name"
        label="name"
        placeholder="your name"
        autofocus
      />
      <UiInput
        v-model="email"
        label="email"
        type="email"
        placeholder="you@example.com"
        autocomplete="email"
        :autofocus="mode === 'login'"
      />
      <UiInput
        v-model="password"
        label="password"
        type="password"
        placeholder="at least 6 characters"
        autocomplete="current-password"
      />
      <p v-if="error" class="login__error" role="alert">{{ error }}</p>
      <UiButton type="submit" block :loading="saving">
        {{ mode === 'login' ? 'sign in' : 'create account' }}
      </UiButton>
    </form>

    <div class="login__switch rise" style="--i: 4">
      <button class="login__link" type="button" @click="switchMode">
        {{ mode === 'login' ? 'new here? create an account' : 'already have one? sign in' }}
      </button>
      <button class="login__link login__link--quiet" type="button" @click="emit('back')">
        back to the landing
      </button>
    </div>
  </div>
</template>

<style scoped>
.login {
  width: 100%;
  max-width: 360px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
  text-align: center;
}

.login__eyebrow {
  font-size: var(--text-xs);
  color: var(--ink-tertiary);
  letter-spacing: 0.14em;
}

.login__title {
  font-size: clamp(26px, 4.5vw, 34px);
  font-weight: 400;
  letter-spacing: -0.02em;
  line-height: 1.15;
  color: var(--ink);
  max-width: 16ch;
  margin: 0 auto;
}

.login__sub {
  font-size: var(--text-sm);
  line-height: 1.7;
  color: var(--ink-secondary);
  max-width: 38ch;
  margin: 0 auto;
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 10px;
  text-align: left;
}

.login__error {
  font-size: var(--text-xs);
  color: var(--danger-ink);
}

.login__switch {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 4px;
}

.login__link {
  font-size: var(--text-xs);
  color: var(--ink-secondary);
  transition: color var(--dur-press) var(--ease-out);
}

.login__link:hover {
  color: var(--ink);
}

.login__link--quiet {
  color: var(--ink-tertiary);
}
</style>
