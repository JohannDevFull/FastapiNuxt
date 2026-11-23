<script setup lang="ts">
import { PackageSearch } from '@lucide/vue'

withDefaults(
  defineProps<{
    title?: string
    description?: string
  }>(),
  {
    title: 'No hay resultados',
    description: 'No encontramos información que coincida con los filtros seleccionados.',
  },
)
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-slate-200 bg-white/60 px-6 py-12 text-center dark:border-slate-700 dark:bg-slate-900/40">
    <div class="flex h-11 w-11 items-center justify-center rounded-full bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-500">
      <PackageSearch class="h-5 w-5" />
    </div>
    <div>
      <p class="font-medium text-slate-800 dark:text-slate-100">{{ title }}</p>
      <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ description }}</p>
    </div>
    <slot />
  </div>
</template>
