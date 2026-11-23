<script setup lang="ts">
import { getStatusClasses, getStatusLabel } from '~/utils/status'

const props = defineProps<{
  status: string
}>()

const label = computed(() => getStatusLabel(props.status))
const classes = computed(() => getStatusClasses(props.status))
</script>

<template>
  <span
    class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium whitespace-nowrap"
    :class="classes"
  >
    {{ label }}
  </span>
</template>
