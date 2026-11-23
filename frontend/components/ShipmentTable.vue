<script setup lang="ts">
import { ArrowUpRight } from '@lucide/vue'
import { formatDate } from '~/utils/format'
import type { Shipment } from '~/types/shipment'

withDefaults(
  defineProps<{
    shipments: Shipment[]
    showActions?: boolean
  }>(),
  {
    showActions: true,
  },
)
</script>

<template>
  <div class="overflow-x-auto">
    <table class="w-full min-w-[820px] text-left text-sm">
      <thead>
        <tr class="border-b border-slate-200 text-xs font-medium uppercase tracking-wide text-slate-500 dark:border-slate-800 dark:text-slate-400">
          <th class="px-4 py-3 font-medium">Guía</th>
          <th class="px-4 py-3 font-medium">Destinatario</th>
          <th class="px-4 py-3 font-medium">Ruta</th>
          <th class="px-4 py-3 font-medium">Estado</th>
          <th class="px-4 py-3 font-medium">Peso</th>
          <th class="px-4 py-3 font-medium">Registro</th>
          <th v-if="showActions" class="px-4 py-3 text-right font-medium">Acciones</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
        <tr
          v-for="shipment in shipments"
          :key="shipment.id"
          class="transition hover:bg-slate-50/80 dark:hover:bg-slate-800/40"
        >
          <td class="px-4 py-3">
            <NuxtLink
              :to="`/shipments/${shipment.id}`"
              class="font-medium text-blue-600 hover:underline dark:text-blue-400"
            >
              {{ shipment.tracking_number }}
            </NuxtLink>
          </td>
          <td class="px-4 py-3">
            <p class="font-medium text-slate-800 dark:text-slate-100">{{ shipment.recipient_name }}</p>
            <p class="text-xs text-slate-400 dark:text-slate-500">{{ shipment.recipient_phone }}</p>
          </td>
          <td class="px-4 py-3">
            <p class="max-w-[220px] truncate text-slate-600 dark:text-slate-300" :title="shipment.origin_address">
              {{ shipment.origin_address }}
            </p>
            <p class="max-w-[220px] truncate text-xs text-slate-400 dark:text-slate-500" :title="shipment.destination_address">
              → {{ shipment.destination_address }}
            </p>
          </td>
          <td class="px-4 py-3"><StatusBadge :status="shipment.status" /></td>
          <td class="px-4 py-3 text-slate-600 dark:text-slate-300">{{ shipment.weight_kg.toFixed(2) }} kg</td>
          <td class="px-4 py-3 text-slate-500 dark:text-slate-400">{{ formatDate(shipment.created_at) }}</td>
          <td v-if="showActions" class="px-4 py-3 text-right">
            <NuxtLink
              :to="`/shipments/${shipment.id}`"
              class="inline-flex items-center gap-1 rounded-lg px-2 py-1 text-xs font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white"
            >
              Ver
              <ArrowUpRight class="h-3.5 w-3.5" />
            </NuxtLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
