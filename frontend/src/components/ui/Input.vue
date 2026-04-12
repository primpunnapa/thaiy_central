<template>
  <input
    :type="type"
    :value="modelValue"
    @input="onInput"
    :class="cn(
      'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
      className
    )"
    ref="inputRef"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  modelValue?: string
  type?: string
  className?: string
}>()

const emit = defineEmits(['update:modelValue'])

const inputRef = ref<HTMLInputElement>()

const onInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

defineExpose({
  inputRef
})
</script>
