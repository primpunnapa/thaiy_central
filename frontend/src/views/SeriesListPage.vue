<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="font-heading text-3xl font-bold mb-6">ซีรีส์ทั้งหมด</h1>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16">
      <p class="text-muted-foreground">กำลังโหลด...</p>
    </div>

    <!-- Search + Filters -->
    <template v-else>
      <div class="flex flex-col sm:flex-row gap-3 mb-8">
        <Input v-model="search" placeholder="ค้นหาซีรีส์..." />

        <div class="flex gap-2">
          <button
            v-for="status in ['all', 'ongoing', 'completed']"
            :key="status"
            @click="setStatus(status)"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium transition-colors',
              statusFilter === status
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted text-foreground/70 hover:bg-muted/80'
            ]"
          >
            {{
              status === 'all'
                ? 'ทั้งหมด'
                : status === 'ongoing'
                ? 'กำลังฉาย'
                : 'จบแล้ว'
            }}
          </button>
        </div>
      </div>

      <!-- Results -->
      <div v-if="filtered.length === 0" class="text-center py-16 text-muted-foreground">
        ไม่พบซีรีส์ที่ค้นหา
      </div>

      <div
        v-else
        class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-5"
      >
        <SeriesCard
          v-for="(s, i) in filtered"
          :key="s.id"
          :series="s"
          :index="i"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SeriesCard from '@/components/SeriesCard.vue'
import Input from '@/components/ui/Input.vue'
import api from '@/lib/api'

const search = ref('')
const statusFilter = ref('all')
const allSeries = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true;
  try {
    const response = await api.getSeries();
    const baseSeries = Array.isArray(response.data) ? response.data : response.data?.data || [];
    const settled = await Promise.allSettled(
      baseSeries.map((s) => api.getSeriesDetail(s.id))
    )

    const merged = settled.map((r, i) => (r.status === 'fulfilled' ? r.value.data : baseSeries[i]))
    allSeries.value = merged
  } catch (err) {
    console.error('Failed to fetch series:', err);
    allSeries.value = [];
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

const filtered = computed(() => {
  return allSeries.value.filter((s) => {
    if (search.value.trim()) {
      const searchLower = search.value.trim().toLowerCase()
      const matchesSearch =
        (s.title_th?.toLowerCase().includes(searchLower) || false) ||
        (s.title_en?.toLowerCase().includes(searchLower) || false) ||
        (s.description?.toLowerCase().includes(searchLower) || false)

      const matchesStatus =
        statusFilter.value === 'all' || s.status === statusFilter.value

      return matchesSearch && matchesStatus
    }

    const matchesStatus =
      statusFilter.value === 'all' || s.status === statusFilter.value

    return matchesStatus
  })
})

const setStatus = (status) => {
  statusFilter.value = status
}
</script>
