<script setup lang="ts">
import { AlertTriangle, RotateCcw } from '@lucide/vue'

defineProps<{
  message: string
  retry?: boolean
}>()

const emit = defineEmits<{
  retry: []
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 rounded-xl border border-rose-200 bg-rose-50/60 px-6 py-12 text-center dark:border-rose-500/30 dark:bg-rose-500/5">
    <div class="flex h-11 w-11 items-center justify-center rounded-full bg-rose-100 text-rose-600 dark:bg-rose-500/15 dark:text-rose-300">
      <AlertTriangle class="h-5 w-5" />
    </div>
    <div>
      <p class="font-medium text-rose-900 dark:text-rose-200">No se pudo completar la consulta</p>
      <p class="mt-1 max-w-xl text-sm text-rose-700 dark:text-rose-300/80">{{ message }}</p>
    </div>
    <button
      v-if="retry"
      type="button"
      class="inline-flex items-center gap-2 rounded-lg border border-rose-300 bg-white px-3 py-2 text-sm font-medium text-rose-700 transition hover:bg-rose-50 dark:border-rose-500/40 dark:bg-slate-900 dark:text-rose-200 dark:hover:bg-rose-500/10"
      @click="emit('retry')"
    >
      <RotateCcw class="h-4 w-4" />
      Reintentar
    </button>
  </div>
</template>
