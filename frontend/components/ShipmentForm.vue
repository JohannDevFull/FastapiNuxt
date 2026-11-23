<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Shipment, ShipmentCreatePayload } from '~/types/shipment'

interface FormState {
  sender_name: string
  sender_phone: string
  recipient_name: string
  recipient_phone: string
  origin_address: string
  destination_address: string
  package_description: string
  weight_kg: string
}

const props = withDefaults(
  defineProps<{
    initial?: Shipment | null
    submitting?: boolean
    submitLabel?: string
  }>(),
  {
    initial: null,
    submitting: false,
    submitLabel: 'Guardar envío',
  },
)

const emit = defineEmits<{
  submit: [payload: ShipmentCreatePayload]
}>()

const emptyForm = (): FormState => ({
  sender_name: '',
  sender_phone: '',
  recipient_name: '',
  recipient_phone: '',
  origin_address: '',
  destination_address: '',
  package_description: '',
  weight_kg: '',
})

const form = reactive<FormState>(emptyForm())

const hydrate = (shipment: Shipment | null | undefined) => {
  Object.assign(form, shipment ? {
    sender_name: shipment.sender_name,
    sender_phone: shipment.sender_phone,
    recipient_name: shipment.recipient_name,
    recipient_phone: shipment.recipient_phone,
    origin_address: shipment.origin_address,
    destination_address: shipment.destination_address,
    package_description: shipment.package_description,
    weight_kg: String(shipment.weight_kg),
  } : emptyForm())
}

watch(() => props.initial, hydrate, { immediate: true })

const submit = () => {
  emit('submit', {
    sender_name: form.sender_name.trim(),
    sender_phone: form.sender_phone.trim(),
    recipient_name: form.recipient_name.trim(),
    recipient_phone: form.recipient_phone.trim(),
    origin_address: form.origin_address.trim(),
    destination_address: form.destination_address.trim(),
    package_description: form.package_description.trim(),
    weight_kg: Number(form.weight_kg),
  })
}
</script>

<template>
  <form class="space-y-6" @submit.prevent="submit">
    <section class="rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
      <div class="border-b border-slate-200 px-5 py-4 dark:border-slate-800">
        <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Remitente</h2>
        <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">Datos de quien envía el paquete.</p>
      </div>
      <div class="grid gap-4 p-5 sm:grid-cols-2">
        <FormField v-model="form.sender_name" label="Nombre completo" name="sender_name" placeholder="Ej. Juan Pérez" :minlength="2" :maxlength="100" required />
        <FormField v-model="form.sender_phone" label="Teléfono" name="sender_phone" type="tel" placeholder="Ej. 3001234567" :minlength="7" :maxlength="20" required />
      </div>
    </section>

    <section class="rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
      <div class="border-b border-slate-200 px-5 py-4 dark:border-slate-800">
        <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Destinatario</h2>
        <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">Datos de quien recibe el paquete.</p>
      </div>
      <div class="grid gap-4 p-5 sm:grid-cols-2">
        <FormField v-model="form.recipient_name" label="Nombre completo" name="recipient_name" placeholder="Ej. María Gómez" :minlength="2" :maxlength="100" required />
        <FormField v-model="form.recipient_phone" label="Teléfono" name="recipient_phone" type="tel" placeholder="Ej. 3107654321" :minlength="7" :maxlength="20" required />
      </div>
    </section>

    <section class="rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
      <div class="border-b border-slate-200 px-5 py-4 dark:border-slate-800">
        <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Envío</h2>
        <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">Ruta, contenido y peso del paquete.</p>
      </div>
      <div class="grid gap-4 p-5 sm:grid-cols-2">
        <FormField v-model="form.origin_address" label="Dirección de origen" name="origin_address" placeholder="Calle 10 # 20-30, Medellín" :minlength="5" :maxlength="255" required />
        <FormField v-model="form.destination_address" label="Dirección de destino" name="destination_address" placeholder="Carrera 50 # 40-20, Bogotá" :minlength="5" :maxlength="255" required />
        <FormField v-model="form.weight_kg" label="Peso (kg)" name="weight_kg" type="number" placeholder="Ej. 2.5" :min="0.01" :step="0.01" required />
        <div class="sm:col-span-2">
          <FormField v-model="form.package_description" label="Descripción del paquete" name="package_description" type="textarea" placeholder="Ej. Caja con documentos" :minlength="3" :maxlength="500" required />
        </div>
      </div>
    </section>

    <div class="flex flex-wrap items-center gap-3">
      <button
        type="submit"
        :disabled="submitting"
        class="inline-flex items-center justify-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {{ submitting ? 'Guardando...' : submitLabel }}
      </button>
      <NuxtLink
        to="/shipments"
        class="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800"
      >
        Cancelar
      </NuxtLink>
    </div>
  </form>
</template>
