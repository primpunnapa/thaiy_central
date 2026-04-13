<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { UserPen } from '@lucide/vue';
import api from '@/lib/api'

const auth = useAuthStore()
const users = ref([])
const showForm = ref(false)
const editingId = ref(null)
const error = ref('')

const roles = ['admin', 'editor', 'normal']
const roleLabelMap = {
  admin: 'Admin',
  editor: 'Content Editor',
  normal: 'User',
}
const roleColorMap = {
  admin: 'bg-rose/10 text-rose',
  editor: 'bg-primary/10 text-primary',
  normal: 'bg-muted text-foreground/60',
}

const form = ref({
  username: '',
  email: '',
  password: '',
  role: 'normal',
  is_active: true,
})

const emptyForm = {
  username: '',
  email: '',
  password: '',
  role: 'normal',
  is_active: true,
}

onMounted(async () => {
  if (!auth.isAdmin) {
    alert('Only admins can access this page')
    return
  }
  fetchUsers()
})

const fetchUsers = async () => {
  try {
    const response = await api.getUsers()
    users.value = response.data
  } catch (e) {
    console.error('Failed to fetch users', e)
    error.value = 'Failed to fetch users'
  }
}

const openCreate = () => {
  form.value = { ...emptyForm }
  editingId.value = null
  showForm.value = true
  error.value = ''
}

const openEdit = (u) => {
  form.value = {
    username: u.username,
    email: u.email,
    password: '',
    role: u.role,
    is_active: u.is_active,
  }
  editingId.value = u.id
  showForm.value = true
  error.value = ''
}

const handleSubmit = async (e) => {
  e.preventDefault()
  error.value = ''

  try {
    const body = { ...form.value }
    if (editingId.value && !body.password) {
      delete body.password
    }

    if (editingId.value) {
      await api.updateUser(editingId.value, body)
    } else {
      await api.createUser(body)
    }

    showForm.value = false
    fetchUsers()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error saving user'
  }
}

const handleDelete = async (id) => {
  if (!confirm('ต้องการลบผู้ใช้นี้?')) return

  try {
    await api.deleteUser(id)
    fetchUsers()
  } catch (e) {
    error.value = 'Failed to delete user'
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="flex justify-between mb-6">
      <h1 class="font-heading text-3xl font-bold flex items-center gap-2">
        <UserPen class="w-6 h-6 text-primary" />
        จัดการผู้ใช้
      </h1>
      <button
        @click="openCreate"
        class="px-4 py-2 bg-primary text-primary-foreground rounded-xl font-medium hover:bg-primary/90 flex items-center gap-2 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        เพิ่มผู้ใช้
      </button>
    </div>

    <!-- Form Modal -->
    <template v-if="showForm">
      <div class="fixed inset-0 z-50 flex items-center justify-center bg-foreground/20 backdrop-blur-sm">
        <div class="bg-card rounded-2xl border border-border p-6 w-full max-w-md shadow-lg">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-heading text-xl font-bold">
              {{ editingId ? 'แก้ไขผู้ใช้' : 'เพิ่มผู้ใช้ใหม่' }}
            </h2>
            <button
              @click="showForm = false"
              class="p-1 rounded-lg hover:bg-muted transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit="handleSubmit" class="space-y-3">
            <input
              v-model="form.username"
              type="text"
              placeholder="Username"
              required
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <input
              v-model="form.email"
              type="email"
              placeholder="Email"
              required
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <input
              v-model="form.password"
              type="password"
              :placeholder="editingId ? 'Password (ว่างไว้ถ้าไม่เปลี่ยน)' : 'Password'"
              :required="!editingId"
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <div>
              <label class="text-sm font-medium text-foreground/60 mb-1 block">Role</label>
              <div class="flex gap-2">
                <button
                  v-for="r in roles"
                  :key="r"
                  type="button"
                  @click="form.role = r"
                  :class="[
                    'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
                    form.role === r
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-foreground/60 hover:bg-muted/80',
                  ]"
                >
                  {{ roleLabelMap[r] }}
                </button>
              </div>
            </div>

            <label class="flex items-center gap-2 text-sm">
              <input
                v-model="form.is_active"
                type="checkbox"
                class="w-4 h-4 accent-primary"
              />
              <span>Active</span>
            </label>

            <div v-if="error" class="text-sm text-rose">{{ error }}</div>

            <button
              type="submit"
              class="w-full px-4 py-2 bg-primary text-primary-foreground rounded-xl font-medium hover:bg-primary/90 transition-colors"
            >
              {{ editingId ? 'บันทึก' : 'สร้าง' }}
            </button>
          </form>
        </div>
      </div>
    </template>

    <!-- Users Table -->
    <div class="bg-card rounded-2xl border border-border overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border bg-muted/50">
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Username</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Email</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Role</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Status</th>
              <th class="text-right px-4 py-3 font-medium text-foreground/60">Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="users.length > 0">
              <tr
                v-for="u in users"
                :key="u.id"
                class="border-b border-border last:border-0 hover:bg-muted/30 transition-colors"
              >
                <td class="px-4 py-3 font-medium">{{ u.username }}</td>
                <td class="px-4 py-3 text-foreground/60">{{ u.email }}</td>
                <td class="px-4 py-3">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xs font-medium',
                      roleColorMap[u.role],
                    ]"
                  >
                    {{ roleLabelMap[u.role] }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xs font-medium',
                      u.is_active
                        ? 'bg-green-500/10 text-green-600'
                        : 'bg-muted text-foreground/60',
                    ]"
                  >
                    {{ u.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      @click="openEdit(u)"
                      class="p-2 rounded-lg hover:bg-muted transition-colors"
                    >
                      <svg class="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      @click="handleDelete(u.id)"
                      class="p-2 rounded-lg hover:bg-rose/10 transition-colors"
                    >
                      <svg class="w-4 h-4 text-rose" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-else>
              <td colspan="5" class="text-center py-8 text-foreground/60">ไม่พบข้อมูลผู้ใช้</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
