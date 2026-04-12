<script setup>
defineProps({
  series: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    default: 0
  }
})

const pastelColors = [
  'bg-lavender',
  'bg-mint',
  'bg-peach',
  'bg-sky',
  'bg-rose'
]

const getBgColor = (index) => {
  return pastelColors[index % pastelColors.length]
}
</script>

<template>
  <router-link
    :to="`/series/${series.id}`"
    class="group block rounded-xl overflow-hidden bg-white border shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1"
    :style="{ animationDelay: index * 80 + 'ms' }"
  >
    <!-- Image -->
    <div
      class="aspect-[3/4] flex items-center justify-center relative overflow-hidden"
      :class="getBgColor(index)"
    >
      <img
        v-if="series.poster_url"
        :src="series.poster_url"
        :alt="series.title_en"
        class="w-full h-full object-cover"
      />

      <div v-else class="text-center p-4">
        <span class="text-2xl font-bold text-gray-400">
          {{ series.title_en }}
        </span>
      </div>

      <!-- Badge -->
      <span
        class="absolute top-3 right-3 text-xs px-2 py-1 rounded-full"
        :class="
          series.status === 'ongoing'
            ? 'bg-green-300 text-green-900'
            : 'bg-gray-300 text-gray-800'
        "
      >
        {{ series.status === 'ongoing' ? 'กำลังฉาย' : 'จบแล้ว' }}
      </span>
    </div>

    <!-- Content -->
    <div class="p-4">
      <h3 class="font-semibold group-hover:text-blue-500 transition line-clamp-1">
        {{ series.title_th }}
      </h3>

      <p class="text-sm text-gray-500 mt-0.5">
        {{ series.title_en }}
      </p>

      <!-- Meta -->
      <div class="flex items-center gap-3 mt-3 text-xs text-gray-500">
        <span class="flex items-center gap-1">
          <Calendar class="w-4 h-4" />
          {{ series.release_year }}
        </span>

        <span class="flex items-center gap-1">
          <Eye class="w-4 h-4" />
          {{ Math.floor(series.views / 1000) }}K
        </span>
      </div>

      <!-- Studios -->
      <div
        v-if="series.studios && series.studios.length > 0"
        class="mt-2 flex flex-wrap gap-1"
      >
        <span
          v-for="s in series.studios"
          :key="s.id"
          class="text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full"
        >
          {{ s.name }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script>
import { Eye, Calendar } from '@lucide/vue';
</script>
