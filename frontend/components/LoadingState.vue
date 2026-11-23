<script setup lang="ts">
import { LoaderCircle } from '@lucide/vue'

withDefaults(
  defineProps<{
    label?: string
  }>(),
  {
    label: 'Cargando información...',
  },
)
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-slate-200 bg-white/60 px-6 py-14 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-900/40 dark:text-slate-400">
    <LoaderCircle class="h-6 w-6 animate-spin text-blue-600 dark:text-blue-400" />
    <span>{{ label }}</span>
  </div>
</template>
