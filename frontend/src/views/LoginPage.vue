<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4">
    <div class="w-full max-w-sm bg-card rounded-2xl border border-border p-8 shadow-sm">
      <!-- Header -->
      <div class="text-center mb-6">
        <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
        </div>
        <h1 class="font-heading text-2xl font-bold">เข้าสู่ระบบ</h1>
      </div>

      <!-- Form -->
      <form @submit="handleSubmit" class="space-y-4">
        <!-- Username field -->
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          required
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <!-- Password field -->
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <!-- Error message -->
        <p v-if="error" class="text-sm text-rose text-center">{{ error }}</p>

        <!-- Submit button -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full px-4 py-2 rounded-xl bg-primary text-primary-foreground font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ loading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleSubmit = async (e) => {
  e.preventDefault()
  error.value = ''
  loading.value = true

  try {
    console.log('Attempting login with:', username.value)
    const success = await auth.login(username.value, password.value)

    if (success) {
      if (auth.isAdmin.value) {
        router.push('/admin/users')
      } else if (auth.isEditor.value) {
        router.push('/editor/series')
      } else {
        router.push('/profile')
      }
    } else {
      error.value = auth.error || 'เข้าสู่ระบบไม่สำเร็จ'
    }
  } catch (err) {
    console.error('Login exception:', err)
    error.value = err.message || 'เข้าสู่ระบบไม่สำเร็จ'
  } finally {
    loading.value = false
  }
}
</script>
