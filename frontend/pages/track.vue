<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Search, ShieldCheck } from '@lucide/vue'
import { getApiErrorMessage, isNotFoundError } from '~/composables/useApiError'
import { formatDateTime } from '~/utils/format'
import type { PublicShipmentView, TrackingEvent } from '~/types/shipment'

definePageMeta({ layout: 'public' })

useHead({ title: 'Consulta pública' })

const route = useRoute()
const { getByTrackingNumber } = useShipments()
const { byTrackingNumber } = useTracking()

const trackingNumber = ref(String(route.query.guia ?? ''))
const loading = ref(false)
const error = ref('')
const searched = ref(false)
const shipment = ref<PublicShipmentView | null>(null)
const events = ref<TrackingEvent[]>([])

const search = async () => {
  const value = trackingNumber.value.trim()
  searched.value = true
  error.value = ''
  shipment.value = null
  events.value = []

  if (!value) {
    error.value = 'Ingresa un número de guía para consultar el envío.'
    return
  }

  loading.value = true
  try {
    const [found, history] = await Promise.all([
      getByTrackingNumber(value),
      byTrackingNumber(value),
    ])

    shipment.value = {
      tracking_number: found.tracking_number,
      status: found.status,
      created_at: found.created_at,
      updated_at: found.updated_at,
    }
    events.value = history
  } catch (requestError) {
    error.value = isNotFoundError(requestError)
      ? 'No encontramos un envío con ese número de guía.'
      : getApiErrorMessage(requestError, 'No se pudo consultar el envío. Intenta nuevamente.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (trackingNumber.value.trim()) {
    void search()
  }
})
</script>

<template>
  <div>
    <div class="mx-auto max-w-2xl text-center">
      <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
        <Search class="h-6 w-6" />
      </div>
      <h1 class="mt-5 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
        Consulta el estado de tu envío
      </h1>
      <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
        Ingresa el número de guía para ver el estado actual y su historial de trazabilidad.
      </p>
    </div>

    <section class="mx-auto mt-8 max-w-2xl rounded-xl border border-slate-200 bg-white p-5 shadow-card dark:border-slate-800 dark:bg-slate-900 sm:p-6">
      <form class="flex flex-col gap-3 sm:flex-row" @submit.prevent="search">
        <label for="public-tracking" class="sr-only">Número de guía</label>
        <input
          id="public-tracking"
          v-model="trackingNumber"
          type="text"
          placeholder="Ej. MCF-20260115-123456"
          class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white dark:placeholder:text-slate-600"
        />
        <button
          type="submit"
          :disabled="loading"
          class="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-5 py-3 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700 disabled:opacity-60"
        >
          <Search class="h-4 w-4" />
          {{ loading ? 'Consultando...' : 'Consultar' }}
        </button>
      </form>

      <p class="mt-3 flex items-center gap-1.5 text-xs text-slate-400 dark:text-slate-500">
        <ShieldCheck class="h-3.5 w-3.5" />
        Solo mostramos el estado y la trazabilidad; no se exhiben datos de remitentes ni destinatarios.
      </p>
    </section>

    <LoadingState v-if="loading" class="mx-auto mt-6 max-w-2xl" label="Buscando envío..." />

    <ErrorState
      v-else-if="error"
      class="mx-auto mt-6 max-w-2xl"
      :message="error"
      :retry="Boolean(trackingNumber.trim())"
      @retry="search"
    />

    <EmptyState
      v-else-if="searched && !shipment"
      class="mx-auto mt-6 max-w-2xl"
      title="Sin resultados"
      description="Verifica el número de guía e inténtalo nuevamente."
    />

    <template v-else-if="shipment">
      <section class="mx-auto mt-6 max-w-2xl overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
        <div class="flex flex-col gap-4 border-b border-slate-200 px-5 py-5 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800">
          <div>
            <p class="text-xs font-medium uppercase tracking-wide text-slate-400 dark:text-slate-500">Número de guía</p>
            <h2 class="mt-1 font-mono text-lg font-semibold text-slate-900 dark:text-white">
              {{ shipment.tracking_number }}
            </h2>
            <p class="mt-2 text-xs text-slate-500 dark:text-slate-400">
              Última actualización: {{ formatDateTime(shipment.updated_at) }}
            </p>
          </div>
          <StatusBadge :status="shipment.status" />
        </div>

        <div class="border-b border-slate-200 px-5 py-4 dark:border-slate-800">
          <h3 class="text-sm font-semibold text-slate-900 dark:text-white">Historial de trazabilidad</h3>
          <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">
            EVENTOS REGISTRADOS POR LA API · {{ events.length }} EN TOTAL
          </p>
        </div>

        <TrackingTimeline :events="events" />
      </section>

      <div class="mx-auto mt-5 max-w-2xl text-center">
        <NuxtLink
          to="/"
          class="inline-flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-slate-800 dark:text-slate-400 dark:hover:text-white"
        >
          <Plus class="h-4 w-4" />
          Ir al panel administrativo
        </NuxtLink>
      </div>
    </template>
  </div>
</template>
