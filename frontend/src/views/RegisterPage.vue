<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4">
    <div class="w-full max-w-sm bg-card rounded-2xl border border-border p-8 shadow-sm">
      <div class="text-center mb-6">
        <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
          <UserPlus class="w-6 h-6 text-primary" />
        </div>
        <h1 class="font-heading text-2xl font-bold">สมัครสมาชิก</h1>
        <p class="text-sm text-muted-foreground mt-1">สร้างบัญชีใหม่</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <input
          v-model="form.username"
          placeholder="Username"
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <input
          v-model="form.email"
          placeholder="Email"
          type="email"
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <input
          v-model="form.full_name"
          placeholder="ชื่อ-นามสกุล"
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <input
          v-model="form.password"
          placeholder="Password"
          type="password"
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <input
          v-model="form.confirmPassword"
          placeholder="ยืนยัน Password"
          type="password"
          class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <p v-if="error" class="text-sm text-rose text-center">{{ error }}</p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full px-4 py-2 rounded-xl font-medium bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ loading ? 'Processing...' : 'Completed' }}
        </button>
      </form>

      <p class="text-center text-sm text-muted-foreground mt-4">
        มีบัญชีแล้ว?
        <router-link to="/login" class="text-primary hover:underline">เข้าสู่ระบบ</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus } from '@lucide/vue'
import api from '@/lib/api'

const router = useRouter()

const form = ref({
  username: '',
  email: '',
  full_name: '',
  password: '',
  confirmPassword: ''
})

const error = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  error.value = ''

  // Validate password match
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'รหัสผ่านไม่ตรงกัน'
    return
  }

  // Validate password length
  if (form.value.password.length < 6) {
    error.value = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
    return
  }

  loading.value = true
  try {
    const response = await api.register(
      form.value.username,
      form.value.email,
      form.value.password
    )
    console.log('Register success:', response)
    router.push('/login')
  } catch (err) {
    console.error('Register error:', err)
    error.value = err.response?.data?.detail || err.message || 'สมัครสมาชิกไม่สำเร็จ'
  } finally {
    loading.value = false
  }
}
</script>
