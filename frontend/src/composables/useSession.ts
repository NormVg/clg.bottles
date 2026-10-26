import { ref } from 'vue'
import { api } from '../api'
import type { ApiUser } from '../types'

const user = ref<ApiUser | null>(null)
const loading = ref(true)

export function useSession() {
  async function load() {
    try {
      user.value = await api.me()
    } catch {
      user.value = null
    } finally {
      loading.value = false
    }
  }

  async function signup(input: { name: string; email: string; password: string }) {
    user.value = await api.signup(input)
  }

  async function login(input: { email: string; password: string }) {
    user.value = await api.login(input)
  }

  async function logout() {
    await api.logout()
    user.value = null
  }

  return { user, loading, load, signup, login, logout }
}
