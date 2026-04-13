<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="font-heading text-3xl font-bold mb-2 flex items-center gap-3">
      <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h18m-9 8V9m0 14h18a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
      </svg>
      ตารางออกอากาศ
    </h1>
    <p class="text-muted-foreground mb-8">ตารางซีรีส์วายไทยที่กำลังออกอากาศในแต่ละวัน</p>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-16">
      <p class="text-lg text-muted-foreground">กำลังโหลด...</p>
    </div>

    <!-- Schedule -->
    <div v-else class="space-y-4">
      <div
        v-for="(day, di) in scheduleData"
        :key="day.day"
        :class="`rounded-xl ${pastelBgs[di]} p-5 animate-fade-in`"
        :style="{ animationDelay: `${di * 100}ms` }"
      >
        <h2 class="font-heading text-lg font-semibold mb-3">
          {{ dayTranslation[day.day] || day.day }}
        </h2>
        <div v-if="day.series.length === 0" class="text-sm text-muted-foreground">
          ไม่มีซีรีส์ออกอากาศ
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <SeriesCard v-for="(s, i) in day.series" :key="s.id" :series="s" :index="i" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import SeriesCard from "@/components/SeriesCard.vue";
import api from "@/lib/api";

const dayTranslation = {
  monday: "วันจันทร์",
  tuesday: "วันอังคาร",
  wednesday: "วันพุธ",
  thursday: "วันพฤหัสบดี",
  friday: "วันศุกร์",
  saturday: "วันเสาร์",
  sunday: "วันอาทิตย์",
};

const pastelBgs = [
  "bg-lavender/50",
  "bg-mint/50",
  "bg-peach/50",
  "bg-sky/50",
  "bg-rose/50",
  "bg-lavender/50",
  "bg-mint/50",
];

const scheduleData = ref([]);
const loading = ref(false);
const error = ref(null);

// Default schedule data if API call fails
const defaultSchedule = [
  { day: "monday", series: [] },
  { day: "tuesday", series: [] },
  { day: "wednesday", series: [] },
  { day: "thursday", series: [] },
  { day: "friday", series: [] },
  { day: "saturday", series: [] },
  { day: "sunday", series: [] },
];

onMounted(async () => {
  loading.value = true;

  try {
    const response = await api.getSchedule();
    const data = response.data;

    // Transform schedule to array
    const transformed = Object.entries(data).map(([day, series]) => ({
      day,
      series: Array.isArray(series) ? series : [],
    }));
    const allSeries = transformed.flatMap((d) => d.series);

    const detailResults = await Promise.allSettled(
      allSeries.map((s) => api.getSeriesDetail(s.id))
    );

    const detailMap = {};
    detailResults.forEach((res, i) => {
      if (res.status === "fulfilled") {
        detailMap[allSeries[i].id] = res.value.data;
      }
    });

    scheduleData.value = transformed.map((d) => ({
      day: d.day,
      series: d.series.map((s) => ({
        ...s,
        ...(detailMap[s.id] || {}), // merge detail
      })),
    }));

  } catch (err) {
    console.error("Failed to fetch schedule:", err);
    scheduleData.value = defaultSchedule;
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

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
