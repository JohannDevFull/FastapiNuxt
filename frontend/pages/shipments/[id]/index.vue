<script setup lang="ts">
import { computed, ref } from 'vue'
import { Ban, CalendarDays, Pencil, Scale } from '@lucide/vue'
import { getApiErrorMessage } from '~/composables/useApiError'
import { formatDateTime } from '~/utils/format'
import type { Shipment, ShipmentStatusUpdatePayload } from '~/types/shipment'

definePageMeta({ layout: 'default' })

const route = useRoute()
const toast = useToast()
const id = computed(() => Number(route.params.id) || 0)

const { useDetail, updateStatus, cancel } = useShipments()
const { useByShipmentId } = useTracking()

const detail = useDetail(id)
const tracking = useByShipmentId(id)

const shipment = computed(() => detail.data.value)
const detailError = computed(() =>
  detail.error.value ? getApiErrorMessage(detail.error.value, 'No se pudo cargar el envío.') : '',
)
const trackingError = computed(() =>
  tracking.error.value ? getApiErrorMessage(tracking.error.value, 'No se pudo cargar la trazabilidad.') : '',
)

const statusSubmitting = ref(false)
const cancelSubmitting = ref(false)

const refreshAll = async () => {
  await Promise.all([detail.refresh(), tracking.refresh()])
}

const handleStatusUpdate = async (payload: ShipmentStatusUpdatePayload) => {
  statusSubmitting.value = true
  try {
    await updateStatus(id.value, payload)
    toast.success('Estado del envío actualizado correctamente.')
    await refreshAll()
  } catch (error) {
    toast.error(getApiErrorMessage(error, 'No se pudo actualizar el estado.'))
  } finally {
    statusSubmitting.value = false
  }
}

const handleCancel = async () => {
  if (!shipment.value) return
  if (!window.confirm(`¿Cancelar el envío ${shipment.value.tracking_number}?`)) return

  cancelSubmitting.value = true
  try {
    await cancel(id.value)
    toast.success('El envío fue cancelado.')
    await refreshAll()
  } catch (error) {
    toast.error(getApiErrorMessage(error, 'No se pudo cancelar el envío.'))
  } finally {
    cancelSubmitting.value = false
  }
}
</script>

<template>
  <div>
    <PageHeader title="Detalle del envío" description="Información completa, estado actual e historial de trazabilidad.">
      <template #actions>
        <NuxtLink
          v-if="shipment"
          :to="`/shipments/${shipment.id}/edit`"
          class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800"
        >
          <Pencil class="h-4 w-4" />
          Editar
        </NuxtLink>
      </template>
    </PageHeader>

    <LoadingState v-if="detail.pending.value" label="Cargando envío..." />
    <ErrorState v-else-if="detailError" :message="detailError" retry @retry="detail.refresh()" />
    <EmptyState v-else-if="!shipment" title="Envío no encontrado" description="El identificador solicitado no existe." />

    <template v-else-if="shipment">
      <div class="grid gap-6 lg:grid-cols-3">
        <section class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900 lg:col-span-2">
          <div class="flex flex-col gap-4 border-b border-slate-200 px-5 py-5 sm:flex-row sm:items-start sm:justify-between dark:border-slate-800">
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Número de guía</p>
              <h2 class="mt-1 font-mono text-lg font-semibold text-slate-900 dark:text-white">
                {{ shipment.tracking_number }}
              </h2>
              <div class="mt-3 flex flex-wrap items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
                <span class="inline-flex items-center gap-1.5">
                  <CalendarDays class="h-3.5 w-3.5" />
                  Registrado {{ formatDateTime(shipment.created_at) }}
                </span>
                <span class="inline-flex items-center gap-1.5">
                  <Scale class="h-3.5 w-3.5" />
                  {{ shipment.weight_kg.toFixed(2) }} kg
                </span>
              </div>
            </div>
            <StatusBadge :status="shipment.status" />
          </div>

          <div class="grid gap-x-6 gap-y-5 p-5 sm:grid-cols-2">
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Remitente</p>
              <p class="mt-1 text-sm font-medium text-slate-800 dark:text-slate-100">{{ shipment.sender_name }}</p>
              <p class="text-sm text-slate-500 dark:text-slate-400">{{ shipment.sender_phone }}</p>
            </div>
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Destinatario</p>
              <p class="mt-1 text-sm font-medium text-slate-800 dark:text-slate-100">{{ shipment.recipient_name }}</p>
              <p class="text-sm text-slate-500 dark:text-slate-400">{{ shipment.recipient_phone }}</p>
            </div>
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Origen</p>
              <p class="mt-1 text-sm text-slate-700 dark:text-slate-200">{{ shipment.origin_address }}</p>
            </div>
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Destino</p>
              <p class="mt-1 text-sm text-slate-700 dark:text-slate-200">{{ shipment.destination_address }}</p>
            </div>
            <div class="sm:col-span-2">
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Descripción del paquete</p>
              <p class="mt-1 text-sm text-slate-700 dark:text-slate-200">{{ shipment.package_description }}</p>
            </div>
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Última actualización</p>
              <p class="mt-1 text-sm text-slate-700 dark:text-slate-200">{{ formatDateTime(shipment.updated_at) }}</p>
            </div>
          </div>
        </section>

        <div class="space-y-6">
          <section class="rounded-xl border border-slate-200 bg-white p-5 shadow-card dark:border-slate-800 dark:bg-slate-900">
            <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Actualizar estado</h2>
            <p class="mb-4 mt-1 text-xs text-slate-500 dark:text-slate-400">
              El backend valida las transiciones permitidas.
            </p>
            <StatusUpdateForm :shipment="shipment" :submitting="statusSubmitting" @submit="handleStatusUpdate" />
          </section>

          <section class="rounded-xl border border-slate-200 bg-white p-5 shadow-card dark:border-slate-800 dark:bg-slate-900">
            <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Acciones</h2>
            <p class="mb-4 mt-1 text-xs text-slate-500 dark:text-slate-400">
              Cancela el envío cuando ya no deba continuar el proceso.
            </p>
            <button
              type="button"
              :disabled="cancelSubmitting"
              class="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-rose-200 bg-rose-50 px-4 py-2 text-sm font-medium text-rose-700 transition hover:bg-rose-100 disabled:opacity-60 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-300 dark:hover:bg-rose-500/20"
              @click="handleCancel"
            >
              <Ban class="h-4 w-4" />
              {{ cancelSubmitting ? 'Cancelando...' : 'Cancelar envío' }}
            </button>
          </section>
        </div>
      </div>

      <section class="mt-6 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
        <div class="border-b border-slate-200 px-5 py-4 dark:border-slate-800">
          <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Trazabilidad</h2>
          <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">Historial de cambios de estado del envío.</p>
        </div>

        <LoadingState v-if="tracking.pending.value" label="Cargando trazabilidad..." />
        <ErrorState
          v-else-if="trackingError"
          :message="trackingError"
          retry
          @retry="tracking.refresh()"
        />
        <TrackingTimeline v-else :events="tracking.data.value ?? []" />
      </section>
    </template>
  </div>
</template>
