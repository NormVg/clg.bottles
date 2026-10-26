<script setup lang="ts">
import { computed, ref } from 'vue'
import { useSession } from '../composables/useSession'
import { useTheme } from '../composables/useTheme'
import UiButton from './ui/UiButton.vue'
import UiDither from './ui/UiDither.vue'
import UiInput from './ui/UiInput.vue'

const emit = defineEmits<{
  done: []
  back: []
}>()

const { login, signup } = useSession()
const { theme } = useTheme()

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
const ditherFront = computed(() => (theme.value === 'dark' ? '#f2f2f012' : '#1a1a1a12'))
const ditherSpeed = reducedMotion ? 0 : 0.3

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
    <div class="login__dither" aria-hidden="true">
      <UiDither
        color-back="#00000000"
        :color-front="ditherFront"
        shape="simplex"
        type="4x4"
        :size="2"
        :scale="0.6"
        :speed="ditherSpeed"
      />
    </div>

    <div class="login__panel">
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
  </div>
</template>

<style scoped>
.login { position: relative; width: 100%; max-width: 360px; margin: 0 auto; }
.login__dither {
  position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
  mask-image: radial-gradient(ellipse 720px 460px at 50% 44%, transparent 0 48%, #000 100%),
    radial-gradient(circle 150px at 36px 40px, transparent 0 55%, #000 100%),
    radial-gradient(circle 150px at calc(100% - 40px) 42px, transparent 0 55%, #000 100%),
    radial-gradient(circle 140px at 40px calc(100% - 46px), transparent 0 55%, #000 100%);
  mask-composite: intersect;
  -webkit-mask-image: radial-gradient(ellipse 720px 460px at 50% 44%, transparent 0 48%, #000 100%),
    radial-gradient(circle 150px at 36px 40px, transparent 0 55%, #000 100%),
    radial-gradient(circle 150px at calc(100% - 40px) 42px, transparent 0 55%, #000 100%),
    radial-gradient(circle 140px at 40px calc(100% - 46px), transparent 0 55%, #000 100%);
  -webkit-mask-composite: source-in;
}
.login__panel {
  position: relative; z-index: 1; display: flex; flex-direction: column;
  gap: 18px; text-align: center;
}
.login__eyebrow { font-size: var(--text-xs); color: var(--ink-tertiary); letter-spacing: 0.14em; }
.login__title {
  font-size: clamp(26px, 4.5vw, 34px); font-weight: 400; letter-spacing: -0.02em;
  line-height: 1.15; color: var(--ink); max-width: 16ch; margin: 0 auto;
}
.login__sub {
  font-size: var(--text-sm); line-height: 1.7; color: var(--ink-secondary);
  max-width: 38ch; margin: 0 auto;
}
.login__form { display: flex; flex-direction: column; gap: 16px; margin-top: 10px; text-align: left; }
.login__error { font-size: var(--text-xs); color: var(--danger-ink); }
.login__switch { display: flex; flex-direction: column; gap: 10px; margin-top: 4px; }
.login__link {
  font-size: var(--text-xs); color: var(--ink-secondary);
  transition: color var(--dur-press) var(--ease-out);
}
.login__link:hover { color: var(--ink); }
.login__link--quiet { color: var(--ink-tertiary); }
</style>
