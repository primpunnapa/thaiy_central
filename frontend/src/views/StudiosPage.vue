<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="font-heading text-3xl font-bold mb-2 flex items-center gap-3">
      <Building2 class="w-8 h-8 text-primary" />
      สตูดิโอ
    </h1>
    <p class="text-muted-foreground mb-8">รวมสตูดิโอผู้ผลิตซีรีส์วายไทยชั้นนำ</p>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-16">
      <p class="text-lg text-muted-foreground">กำลังโหลด...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="studiosData.length === 0" class="text-center py-16">
      <p class="text-lg text-muted-foreground">ไม่พบสตูดิโอ</p>
    </div>

    <!-- Studios grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="(studio, i) in studiosData"
        :key="studio.id"
        class="rounded-xl border border-border bg-card p-6 hover:shadow-md transition-shadow animate-fade-in"
        :style="{ animationDelay: `${i * 100}ms` }"
      >
        <div class="flex items-start justify-between">
          <div>
            <h3 class="font-heading text-xl font-semibold">{{ studio.name }}</h3>
            <a
              v-if="studio.website_url"
              :href="studio.website_url"
              target="_blank"
              rel="noopener noreferrer"
              :class="`inline-block mt-2 text-xs font-medium px-3 py-1 rounded-full ${
                studioColors[i % studioColors.length]
              } text-foreground hover:underline truncate max-w-[200px]`"
            >
              {{ studio.website_url }}
            </a>
            </div>
          <div :class="`w-12 h-12 rounded-lg ${studioColors[i % studioColors.length]} flex items-center justify-center`">
             <img
              v-if="studio.logo_url"
              :src="studio.logo_url"
              :alt="studio.name"
              class="w-10 h-10 rounded"
            />
            <Building2 v-else class="w-6 h-6 text-foreground/70" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Building2 } from '@lucide/vue';
import api from '@/lib/api'

const studiosData = ref([])
const loading = ref(false)
const error = ref(null)

// Rotating colors for studios
const studioColors = [
  'bg-mint',
  'bg-lavender',
  'bg-rose',
  'bg-peach',
  'bg-sky',
  'bg-accent',
]

onMounted(async () => {
  loading.value = true
  try {
    const response = await api.getStudios()
    studiosData.value = Array.isArray(response.data) ? response.data : response.data?.data || []
  } catch (err) {
    console.error('Failed to fetch studios:', err)
    error.value = err.message
    studiosData.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}
</style>
