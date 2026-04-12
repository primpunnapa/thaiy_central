<template>
  <div>
    <section class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-background/90 via-background/70 to-background/40" />
      <div class="container mx-auto px-4 py-20 md:py-32 relative">
        <div class="max-w-2xl animate-fade-in">
          <div class="flex items-center gap-2 mb-4">
            <svg class="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L15.09 8.26H21.77L16.88 12.19L17.97 18.45L12 14.56L6.03 18.45L7.12 12.19L2.23 8.26H8.91L12 2Z" />
            </svg>
            <span class="text-sm font-medium text-primary">Thai BL Series Hub</span>
          </div>
          <h1 class="font-heading text-4xl md:text-6xl font-bold text-foreground leading-tight">
            รวมซีรีส์วายไทย
            <br />
            <span class="text-primary">ครบทุกเรื่อง</span>
          </h1>
          <p class="mt-4 text-lg text-foreground/70 max-w-lg">
            ค้นหาข้อมูลซีรีส์วายไทย ตารางออกอากาศ สตูดิโอ และแพลตฟอร์มรับชม ทั้งหมดในที่เดียว
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <Button as-child size="lg" class="rounded-full">
              <router-link to="/series">
                ดูซีรีส์ทั้งหมด
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7m0 0l-7 7m7-7H5" />
                </svg>
              </router-link>
            </Button>
            <Button as-child variant="outline" size="lg" class="rounded-full">
              <router-link to="/schedule">ตารางออกอากาศ</router-link>
            </Button>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured -->
    <section class="container mx-auto px-4 py-12">
      <div class="flex items-center justify-between mb-6">
        <h2 class="font-heading text-2xl font-bold flex items-center gap-2">
          <svg class="w-6 h-6 fill-primary text-primary" viewBox="0 0 24 24">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
          </svg>
          ซีรีส์ยอดนิยม
        </h2>
        <router-link to="/series" class="text-sm text-primary hover:underline flex items-center gap-1">
          ดูทั้งหมด
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7m0 0l-7 7m7-7H5" />
          </svg>
        </router-link>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-if="loading" class="col-span-full text-center py-8">Loading...</div>
        <SeriesCard v-for="(series, index) in featured" :key="series.id" :series="series" :index="index" />
      </div>
    </section>

    <!-- Latest -->
    <section class="bg-muted/50 py-12">
      <div class="container mx-auto px-4">
        <h2 class="font-heading text-2xl font-bold mb-6">ซีรีส์ล่าสุด</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          <SeriesCard v-for="(series, index) in latest" :key="series.id" :series="series" :index="index" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import Button from "@/components/ui/Button.vue";
import SeriesCard from "@/components/SeriesCard.vue";
import api from "@/lib/api";

const series = ref([]);
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  loading.value = true;
  try {
    const response = await api.getSeries();
    const baseSeries = Array.isArray(response.data) ? response.data : response.data?.data || [];

    const settled = await Promise.allSettled(
      baseSeries.map((s) => api.getSeriesDetail(s.id))
    )

    const merged = settled.map((r, i) => (r.status === 'fulfilled' ? r.value.data : baseSeries[i]))
    series.value = merged
    console.log('Fetched series (merged details):', series.value)
  } catch (err) {
    console.error('Failed to fetch series:', err);
    series.value = [];
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

const featured = computed(() => series.value.slice(0, 3));
const latest = computed(() => series.value.slice(0, 6));
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
