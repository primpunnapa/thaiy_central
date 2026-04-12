<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'

const auth = useAuthStore()
const studios = ref([])
const showForm = ref(false)
const editingId = ref(null)
const error = ref('')


const form = ref({
  name: '',
  website_url: '',
  logo_url: '',
})

const emptyForm = {
  name: '',
  website_url: '',
  logo_url: '',
}

onMounted(async () => {
  if (!auth.isEditor) {
    alert('Only editors can access this page')
    return
  }
  fetchStudios()
})

const fetchStudios = async () => {
  try {
    const response = await api.getStudios()
    studios.value = response.data
  } catch {
    error.value = 'Failed to fetch studios'
  }
}

const openCreate = () => {
  form.value = { ...emptyForm }
  editingId.value = null
  showForm.value = true
  error.value = ''
}

const openEdit = (s) => {
  form.value = {
    name: s.name,
    website_url: s.website_url,
    logo_url: s.logo_url,
  }
  editingId.value = s.id
  showForm.value = true
  error.value = ''
}

const handleSubmit = async (e) => {
  e.preventDefault()
  error.value = ''

  try {
    const body = { ...form.value }
    const method = editingId.value ? 'PUT' : 'POST'

    if (method === 'POST') {
      await api.createStudio(body)
    } else {
      await api.updateStudio(editingId.value, body)
    }

    showForm.value = false
    fetchStudios()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error saving studio'
  }
}

const handleDelete = async (id) => {
  if (!confirm('ต้องการลบสตูดิโอนี้?')) return

  try {
    await api.deleteStudio(id)
    fetchStudios()
  } catch{
    error.value = 'Failed to delete studio'
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="font-heading text-3xl font-bold flex items-center gap-2">
        <svg class="w-7 h-7 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.581m0 0H9m5.581 0a2 2 0 100-4 2 2 0 000 4z" />
        </svg>
        จัดการสตูดิโอ
      </h1>
      <button
        @click="openCreate"
        class="px-4 py-2 bg-primary text-primary-foreground rounded-xl font-medium hover:bg-primary/90 flex items-center gap-2 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        เพิ่มสตูดิโอ
      </button>
    </div>

    <!-- Modal -->
    <template v-if="showForm">
      <div class="fixed inset-0 z-50 flex items-center justify-center bg-foreground/20 backdrop-blur-sm">
        <div class="bg-card rounded-2xl border border-border p-6 w-full max-w-md shadow-lg">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-heading text-xl font-bold">
              {{ editingId ? 'แก้ไขสตูดิโอ' : 'เพิ่มสตูดิโอใหม่' }}
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
              v-model="form.name"
              type="text"
              placeholder="Name"
              required
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <input
              v-model="form.website_url"
              type="text"
              placeholder="Website URL"
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <input
              v-model="form.logo_url"
              type="text"
              placeholder="Logo URL"
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

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

    <!-- Studios Table -->
    <div class="bg-card rounded-2xl border border-border overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border bg-muted/50">
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Name</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Website</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Logo</th>
              <th class="text-right px-4 py-3 font-medium text-foreground/60">Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="studios.length > 0">
              <tr
                v-for="s in studios"
                :key="s.id"
                class="border-b border-border last:border-0 hover:bg-muted/30 transition-colors"
              >
                <td class="px-4 py-3 font-medium">{{ s.name }}</td>
                <td class="px-4 py-3 text-foreground/60 truncate max-w-[200px]">
                  <a
                    v-if="s.website_url"
                    :href="s.website_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-primary hover:underline"
                  >
                    {{ s.website_url }}
                  </a>
                  <span v-else>-</span>
                </td>
                <td class="px-4 py-3 text-foreground/60">
                  <img
                    v-if="s.logo_url"
                    :src="s.logo_url"
                    :alt="s.name"
                    class="w-25 h-8 rounded object-cover"
                  />
                  <span v-else>-</span>
                </td>
                <td class="px-4 py-3 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      @click="openEdit(s)"
                      class="p-2 rounded-lg hover:bg-muted transition-colors"
                    >
                      <svg class="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      @click="handleDelete(s.id)"
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
              <td colspan="4" class="text-center py-8 text-foreground/60">ไม่พบข้อมูลสตูดิโอ</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
