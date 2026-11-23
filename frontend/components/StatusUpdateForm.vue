<script setup lang="ts">
import { watch, ref } from 'vue'
import { statusOptions } from '~/utils/status'
import type { Shipment, ShipmentStatus, ShipmentStatusUpdatePayload } from '~/types/shipment'

const props = defineProps<{
  shipment: Shipment
  submitting?: boolean
}>()

const emit = defineEmits<{
  submit: [payload: ShipmentStatusUpdatePayload]
}>()

const newStatus = ref<ShipmentStatus>(props.shipment.status)
const observation = ref('')

watch(
  () => [props.shipment.id, props.shipment.status],
  () => {
    newStatus.value = props.shipment.status
    observation.value = ''
  },
)

const submit = () => {
  emit('submit', {
    new_status: newStatus.value,
    observation: observation.value.trim() || null,
  })
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="submit">
    <label class="block">
      <span class="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">Nuevo estado</span>
      <select
        v-model="newStatus"
        class="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-900 dark:text-white"
      >
        <option v-for="option in statusOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </label>

    <label class="block">
      <span class="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">Observación</span>
      <input
        v-model="observation"
        type="text"
        maxlength="255"
        placeholder="Ej. Paquete recogido en almacén"
        class="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:placeholder:text-slate-600"
      />
    </label>

    <button
      type="submit"
      :disabled="submitting"
      class="inline-flex w-full items-center justify-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
    >
      {{ submitting ? 'Actualizando...' : 'Actualizar estado' }}
    </button>
  </form>
</template>
