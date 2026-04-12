<script setup>
defineProps({
  studio: Object,
  index: Number
})

const platformColors = {
  iqiyi: 'bg-green-300',
  viu: 'bg-purple-300',
  netflix: 'bg-red-300',
  aisplay: 'bg-orange-300',
  oned: 'bg-blue-300',
  wetv: 'bg-pink-300'
}

const platformLabels = {
  iqiyi: 'iQIYI',
  viu: 'Viu',
  netflix: 'Netflix',
  aisplay: 'AIS Play',
  oned: 'One D',
  wetv: 'WeTV'
}
</script>

<template>
  <div
    class="rounded-xl border p-6 hover:shadow-md transition"
    :style="{ animationDelay: index * 100 + 'ms' }"
  >
    <div class="flex justify-between">
      <div>
        <h3 class="text-xl font-semibold">{{ studio.name }}</h3>

        <span
          class="inline-block mt-2 text-xs px-3 py-1 rounded-full"
          :class="platformColors[studio.platform] || 'bg-gray-200'"
        >
          {{ platformLabels[studio.platform] || studio.platform }}
        </span>
      </div>

      <div
        class="w-12 h-12 rounded-lg flex items-center justify-center"
        :class="platformColors[studio.platform] || 'bg-gray-200'"
      >
        🏢
      </div>
    </div>

    <a
      v-if="studio.website_url"
      :href="studio.website_url"
      target="_blank"
      class="mt-4 inline-block text-sm text-blue-500 hover:underline"
    >
      website ↗
    </a>
  </div>
</template>
