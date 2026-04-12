<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Back Button -->
    <router-link to="/series">
      <button class="flex items-center gap-2 px-4 py-2 mb-6 text-foreground hover:bg-muted rounded-md transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        กลับ
      </button>
    </router-link>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16">
      <p class="text-lg text-muted-foreground">กำลังโหลด...</p>
    </div>

    <!-- Not Found -->
    <div v-else-if="!series" class="text-center py-16">
      <p class="text-lg text-muted-foreground mb-4">ไม่พบซีรีส์นี้</p>
      <router-link to="/series">
        <button class="px-4 py-2 border border-input bg-background hover:bg-accent rounded-md">
          กลับไปดูซีรีส์ทั้งหมด
        </button>
      </router-link>
    </div>

    <!-- Content -->
    <div v-else class="grid md:grid-cols-[300px_1fr] gap-8 animate-fade-in">
      <!-- Poster -->
      <div class="rounded-xl overflow-hidden bg-lavender aspect-[3/4] flex items-center justify-center">
        <img
          v-if="series.poster_url"
          :src="series.poster_url"
          :alt="series.title_en"
          class="w-full h-full object-cover"
        />
        <span v-else class="font-heading text-2xl font-bold text-foreground/30 text-center px-4">
          {{ series.title_en }}
        </span>
      </div>

      <!-- Info -->
      <div>
        <!-- Status Badge -->
        <span
          :class="[
            'inline-block px-3 py-1 rounded-md text-sm font-medium',
            series.status === 'ongoing'
              ? 'bg-accent text-accent-foreground'
              : 'bg-secondary text-secondary-foreground'
          ]"
        >
          {{ series.status === 'ongoing' ? 'กำลังฉาย' : 'จบแล้ว' }}
        </span>

        <!-- Title -->
        <h1 class="font-heading text-3xl md:text-4xl font-bold mt-3">{{ series.title_th }}</h1>
        <p class="text-lg text-muted-foreground">{{ series.title_en }}</p>

        <!-- Meta Info -->
        <div class="flex flex-wrap gap-4 mt-6 text-sm text-muted-foreground">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            ปี {{ series.release_year }}
          </span>
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            {{ formatViews(series.views) }} views
          </span>
          <span v-if="series.air_day" class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4a1 1 0 011 1v12a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1h3zm0 0a1 1 0 00-1-1H4a1 1 0 00-1 1v12a1 1 0 001 1h3a1 1 0 001-1V5z" />
            </svg>
            {{ series.air_day }}
          </span>
          <span v-if="series.air_time" class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ series.air_time }}
          </span>
        </div>

        <!-- Description -->
        <div class="mt-6">
          <h2 class="font-heading text-lg font-semibold mb-2">เรื่องย่อ</h2>
          <p class="text-foreground/80 leading-relaxed">{{ series.description }}</p>
        </div>

        <!-- Platforms -->
        <div v-if="series.platforms && series.platforms.length > 0" class="mt-6">
          <h2 class="font-heading text-lg font-semibold mb-3">แพลตฟอร์มรับชม</h2>
          <div class="flex flex-wrap gap-3">
            <div
              v-for="platform in series.platforms"
              :key="platform"
              :class="[
                platformColors[platform] || 'bg-muted',
                'rounded-lg px-4 py-3'
              ]"
            >
              <p class="font-medium text-foreground capitalize">{{ platform }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/lib/api'

const route = useRoute()
const seriesData = ref(null)
const loading = ref(false)
const error = ref(null)

const platformColors = {
  iqiyi: 'bg-mint',
  viu: 'bg-lavender',
  netflix: 'bg-rose',
  aisplay: 'bg-peach',
  oned: 'bg-sky',
  wetv: 'bg-accent',
}

onMounted(async () => {
  loading.value = true
  try {
    const id = route.params.id
    const response = await api.getSeriesDetail(id)
    seriesData.value = response.data
  } catch (err) {
    console.error('Failed to fetch series detail:', err)
    seriesData.value = null
    error.value = err.message
  } finally {
    loading.value = false
  }
})

const series = computed(() => seriesData.value)

const formatViews = (views) => {
  if (views >= 1000) {
    return `${(views / 1000).toFixed(0)}K`
  }
  return views.toLocaleString()
}
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
