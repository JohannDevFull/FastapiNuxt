<script setup lang="ts">
import { ArrowRight } from '@lucide/vue'
import { formatDateTime } from '~/utils/format'
import type { TrackingEvent } from '~/types/shipment'

defineProps<{
  events: TrackingEvent[]
}>()
</script>

<template>
  <div v-if="events.length" class="px-5 py-5">
    <ol class="relative ml-2 border-l border-slate-200 pl-6 dark:border-slate-700">
      <li v-for="event in events" :key="event.id" class="relative pb-6 last:pb-0">
        <span class="absolute -left-[31px] top-1 h-3 w-3 rounded-full border-2 border-white bg-blue-600 ring-1 ring-blue-600/20 dark:border-slate-900 dark:bg-blue-500"></span>
        <div class="flex flex-wrap items-center gap-2">
          <StatusBadge :status="event.previous_status" />
          <ArrowRight class="h-4 w-4 text-slate-400 dark:text-slate-500" />
          <StatusBadge :status="event.new_status" />
        </div>
        <p class="mt-2 text-sm text-slate-700 dark:text-slate-200">
          {{ event.observation || 'Sin observaciones registradas.' }}
        </p>
        <p class="mt-1 text-xs text-slate-400 dark:text-slate-500">
          {{ formatDateTime(event.created_at) }}
        </p>
      </li>
    </ol>
  </div>
  <div v-else class="px-5 pb-8 text-sm text-slate-500 dark:text-slate-400">
    Todavía no hay eventos de trazabilidad para este envío.
  </div>
</template>
