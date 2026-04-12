<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'

const auth = useAuthStore()
const seriesList = ref([])
const studios = ref([])
const showForm = ref(false)
const editingId = ref(null)
const error = ref('')

const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
const dayLabels = {
  monday: 'Monday',
  tuesday: 'Tuesday',
  wednesday: 'Wednesday',
  thursday: 'Thursday',
  friday: 'Friday',
  saturday: 'Saturday',
  sunday: 'Sunday',
}

const form = ref({
  title_th: '',
  title_en: '',
  description: '',
  release_year: new Date().getFullYear(),
  poster_url: '',
  status: 'ongoing',
  air_day: '',
  air_time: '',
  studio_id: null,
})

const emptyForm = {
  title_th: '',
  title_en: '',
  description: '',
  release_year: new Date().getFullYear(),
  poster_url: '',
  status: 'ongoing',
  air_day: '',
  air_time: '',
  studio_id: null,
}

onMounted(async () => {
  if (!auth.isEditor) {
    alert('Only editors can access this page')
    return
  }
  fetchData()
})

const fetchData = async () => {
  try {
    const seriesRes = await api.getSeries({ limit: 20 })
    const studiosRes = await api.getStudios()

    const baseSeries = seriesRes.data

    const detailedSeries = await Promise.all(
      baseSeries.map(async (s) => {
        try {
          const res = await api.getSeriesDetail(s.id)
          return res.data
        } catch (e) {
          console.error(`Failed to fetch detail for series ${s.id}`)
          return s
        }
      })
    )

    seriesList.value = detailedSeries
    studios.value = studiosRes.data

  } catch (e) {
    error.value = 'Failed to fetch data'
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
    title_th: s.title_th,
    title_en: s.title_en,
    description: s.description,
    release_year: s.release_year,
    poster_url: s.poster_url,
    status: s.status,
    air_day: s.air_day || '',
    air_time: s.air_time || '',
    studio_id: s.studio_id || null,
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

    // Remove empty or null fields so backend doesn't receive explicit nulls
    Object.keys(body).forEach((k) => {
      if (body[k] === '' || body[k] === null) {
        delete body[k]
      }
    })

    const method = editingId.value ? 'PUT' : 'POST'

    if (method === 'POST') {
      await api.createSeries(body)
    } else {
      await api.updateSeries(editingId.value, body)
    }

    showForm.value = false
    fetchData()
  } catch (e) {
    console.error('Error saving series', e)
    error.value = e.response?.data?.detail || e.message || 'Error saving series'
  }
}

const handleDelete = async (id) => {
  if (!confirm('ต้องการลบซีรีส์นี้?')) return

  try {
    await api.deleteSeries(id)
    fetchData()
  } catch (e) {
    error.value = 'Failed to delete series'
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="font-heading text-3xl font-bold flex items-center gap-2">
        <svg class="w-7 h-7 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16m10-16v16m-10-4h10M7 8h10m0 8H7" />
        </svg>
        จัดการซีรีส์
      </h1>
      <button
        @click="openCreate"
        class="px-4 py-2 bg-primary text-primary-foreground rounded-xl font-medium hover:bg-primary/90 flex items-center gap-2 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        เพิ่มซีรีส์
      </button>
    </div>

    <!-- Modal -->
    <template v-if="showForm">
      <div class="fixed inset-0 z-50 flex items-center justify-center bg-foreground/20 backdrop-blur-sm">
        <div class="bg-card rounded-2xl border border-border p-6 w-full max-w-lg shadow-lg max-h-[90vh] overflow-y-auto">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-heading text-xl font-bold">
              {{ editingId ? 'แก้ไขซีรีส์' : 'เพิ่มซีรีส์ใหม่' }}
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
              v-model="form.title_th"
              type="text"
              placeholder="ชื่อไทย"
              required
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <input
              v-model="form.title_en"
              type="text"
              placeholder="English Title"
              required
              class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <textarea
              v-model="form.description"
              placeholder="Description"
              class="w-full rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 px-4 py-2 text-sm min-h-[80px] focus:outline-none focus:ring-2 focus:ring-primary"
            />

            <div class="grid grid-cols-2 gap-3">
              <input
                v-model.number="form.release_year"
                type="number"
                placeholder="ปีที่ออกอากาศ"
                class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <input
                v-model="form.poster_url"
                type="text"
                placeholder="Poster URL"
                class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-sm font-medium text-foreground/60 mb-1 block">วันออกอากาศ</label>
                <select
                  v-model="form.air_day"
                  class="w-full rounded-xl border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">-</option>
                  <option v-for="d in days" :key="d" :value="d">{{ dayLabels[d] }}</option>
                </select>
              </div>
              <label class="text-sm font-medium text-foreground/60">เวลาที่ออกอากาศ</label>
                <input
                  v-model="form.air_time"
                  type="text"
                  placeholder="เวลา (เช่น 20:30)"
                  class="w-full px-4 py-2 rounded-xl border border-border bg-background text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-2 focus:ring-primary"
                />
            </div>

            <div>
              <label class="text-sm font-medium text-foreground/60 mb-1 block">Status</label>
              <div class="flex gap-2">
                <button
                  type="button"
                  @click="form.status = 'ongoing'"
                  :class="[
                    'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
                    form.status === 'ongoing'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-foreground/60 hover:bg-muted/80',
                  ]"
                >
                  กำลังฉาย
                </button>
                <button
                  type="button"
                  @click="form.status = 'completed'"
                  :class="[
                    'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
                    form.status === 'completed'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-foreground/60 hover:bg-muted/80',
                  ]"
                >
                  จบแล้ว
                </button>
              </div>
            </div>

            <div>
              <label class="text-sm font-medium text-foreground/60 mb-1 block">Studio</label>
              <select
                v-model.number="form.studio_id"
                class="w-full rounded-xl border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option :value="null">-</option>
                <option v-for="s in studios" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>

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

    <!-- Series Table -->
    <div class="bg-card rounded-2xl border border-border overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border bg-muted/50">
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Name</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Year</th>              <th class="text-left px-4 py-3 font-medium text-foreground/60">Status</th>
              <th class="text-left px-4 py-3 font-medium text-foreground/60">Studio</th>
              <th class="text-right px-4 py-3 font-medium text-foreground/60">Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="seriesList.length > 0">
              <tr
                v-for="s in seriesList"
                :key="s.id"
                class="border-b border-border last:border-0 hover:bg-muted/30 transition-colors"
              >
                <td class="px-4 py-3">
                  <div class="font-medium">{{ s.title_en }}</div>
                  <div class="text-xs text-foreground/60">{{ s.title_th }}</div>
                </td>
                <td class="px-4 py-3 text-foreground/60">{{ s.release_year }}</td>
                 <td class="px-4 py-3">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xs font-medium',
                      s.status === 'ongoing'
                        ? 'bg-primary/10 text-primary'
                        : 'bg-muted text-foreground/60',
                    ]"
                  >
                    {{ s.status === 'ongoing' ? 'กำลังฉาย' : 'จบแล้ว' }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xs font-medium',
                      s.status === 'ongoing'
                        ? 'bg-primary/10 text-primary'
                        : 'bg-muted text-foreground/60',
                    ]"
                  >
                    {{ s.status === 'ongoing' ? 'กำลังฉาย' : 'จบแล้ว' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-foreground/60">{{ s.studio?.name || '-' }}</td>
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
              <td colspan="5" class="text-center py-8 text-foreground/60">ไม่พบข้อมูลซีรีส์</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
