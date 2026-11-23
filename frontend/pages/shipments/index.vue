<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ChevronLeft, ChevronRight, Plus, Search, X } from '@lucide/vue'
import { getApiErrorMessage, isNotFoundError } from '~/composables/useApiError'
import { statusOptions } from '~/utils/status'
import type { Shipment, ShipmentListResponse, ShipmentStatus } from '~/types/shipment'

type StatusFilter = ShipmentStatus | ''

definePageMeta({ layout: 'default' })

const route = useRoute()
const router = useRouter()
const pageSize = 10

const page = ref(Math.max(1, Number(route.query.page) || 1))
const trackingQuery = ref(String(route.query.q ?? ''))
const statusFilter = ref<StatusFilter>((route.query.status as StatusFilter) || '')

const { useList, getAll, getByTrackingNumber } = useShipments()
const listQuery = useList(page, pageSize)
const allQuery = useAsyncData('mini-cargoflow-all-shipments', () => getAll(), {
  immediate: false,
  server: false,
  default: () => [] as Shipment[],
})

const searchResult = ref<Shipment | null>(null)
const searchPending = ref(false)
const searchError = ref('')

const statusFiltered = computed(() =>
  statusFilter.value
    ? allQuery.data.value.filter((shipment) => shipment.status === statusFilter.value)
    : [],
)

const view = computed<ShipmentListResponse>(() => {
  if (searchResult.value) {
    return { items: [searchResult.value], total: 1, page: 1, page_size: 1 }
  }

  if (statusFilter.value) {
    const filtered = statusFiltered.value
    return {
      items: filtered.slice((page.value - 1) * pageSize, page.value * pageSize),
      total: filtered.length,
      page: page.value,
      page_size: pageSize,
    }
  }

  return (
    listQuery.data.value ?? {
      items: [],
      total: 0,
      page: page.value,
      page_size: pageSize,
    }
  )
})

const pending = computed(() =>
  searchPending.value || (statusFilter.value ? allQuery.pending.value : listQuery.pending.value),
)

const loadError = computed(() =>
  statusFilter.value ? allQuery.error.value : listQuery.error.value,
)

const errorMessage = computed(() =>
  loadError.value ? getApiErrorMessage(loadError.value, 'No se pudo cargar el listado de envíos.') : '',
)

const totalPages = computed(() => Math.max(1, Math.ceil(view.value.total / pageSize)))

const hasFilters = computed(
  () => Boolean(trackingQuery.value.trim()) || Boolean(statusFilter.value),
)

const clearSearch = () => {
  trackingQuery.value = ''
  searchResult.value = null
  searchError.value = ''
  page.value = 1
}

const clearFilters = () => {
  clearSearch()
  statusFilter.value = ''
}

const search = async () => {
  const value = trackingQuery.value.trim()
  searchResult.value = null
  searchError.value = ''

  if (!value) {
    return
  }

  searchPending.value = true
  try {
    searchResult.value = await getByTrackingNumber(value)
    page.value = 1
  } catch (error) {
    searchError.value = isNotFoundError(error)
      ? 'No se encontró un envío con ese número de guía.'
      : getApiErrorMessage(error, 'No se pudo realizar la búsqueda.')
  } finally {
    searchPending.value = false
  }
}

const retry = () => {
  if (statusFilter.value) {
    void allQuery.refresh()
  } else {
    void listQuery.refresh()
  }
}

const goToPage = (target: number) => {
  if (target >= 1 && target <= totalPages.value) {
    page.value = target
  }
}

watch(statusFilter, async () => {
  page.value = 1
  if (statusFilter.value) {
    await allQuery.refresh()
  }
})

watch(page, () => {
  if (import.meta.client) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

watch([page, trackingQuery, statusFilter], () => {
  void router.replace({
    query: {
      ...route.query,
      page: page.value !== 1 ? String(page.value) : undefined,
      q: trackingQuery.value.trim() || undefined,
      status: statusFilter.value || undefined,
    },
  })
})
</script>

<template>
  <div>
    <PageHeader title="Envíos" description="Consulta, filtra y gestiona los envíos registrados.">
      <template #actions>
        <NuxtLink
          to="/shipments/new"
          class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700"
        >
          <Plus class="h-4 w-4" />
          Nuevo envío
        </NuxtLink>
      </template>
    </PageHeader>

    <section class="mb-5 rounded-xl border border-slate-200 bg-white p-4 shadow-card dark:border-slate-800 dark:bg-slate-900">
      <div class="flex flex-col gap-3 lg:flex-row lg:items-end">
        <div class="flex-1">
          <label for="tracking-search" class="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
            Buscar por número de guía
          </label>
          <div class="flex gap-2">
            <input
              id="tracking-search"
              v-model="trackingQuery"
              type="text"
              placeholder="Ej. MCF-20260115-123456"
              class="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white dark:placeholder:text-slate-600"
              @keyup.enter="search"
            />
            <button
              type="button"
              :disabled="searchPending"
              class="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 disabled:opacity-60 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
              @click="search"
            >
              <Search class="h-4 w-4" />
              Buscar
            </button>
          </div>
          <p class="mt-1.5 text-xs text-slate-400 dark:text-slate-500">La búsqueda por guía es exacta.</p>
        </div>

        <div class="lg:w-64">
          <label for="status-filter" class="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
            Estado
          </label>
          <select
            id="status-filter"
            v-model="statusFilter"
            class="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
          >
            <option value="">Todos los estados</option>
            <option v-for="option in statusOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>

        <button
          v-if="hasFilters"
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2 text-sm font-medium text-slate-500 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-800"
          @click="clearFilters"
        >
          <X class="h-4 w-4" />
          Limpiar
        </button>
      </div>

      <div
        v-if="searchError"
        class="mt-4 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-300"
      >
        {{ searchError }}
      </div>
    </section>

    <LoadingState v-if="pending" label="Cargando envíos..." />
    <ErrorState v-else-if="errorMessage" :message="errorMessage" retry @retry="retry()" />
    <EmptyState
      v-else-if="!view.items.length"
      :title="hasFilters ? 'Sin coincidencias' : 'Aún no hay envíos registrados'"
      :description="hasFilters ? 'Prueba con otro número de guía o estado.' : 'Registra el primer envío para comenzar.'"
    >
      <NuxtLink
        v-if="!hasFilters"
        to="/shipments/new"
        class="mt-2 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
      >
        <Plus class="h-4 w-4" />
        Registrar envío
      </NuxtLink>
    </EmptyState>

    <section v-else class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
      <ShipmentTable :shipments="view.items" />

      <div class="flex flex-col gap-3 border-t border-slate-200 px-4 py-3 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800">
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Página {{ view.page }} de {{ totalPages }} · {{ view.total }} envío(s)
        </p>
        <div class="flex items-center gap-2">
          <button
            type="button"
            :disabled="view.page <= 1"
            class="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
            @click="goToPage(view.page - 1)"
          >
            <ChevronLeft class="h-4 w-4" />
            Anterior
          </button>
          <button
            type="button"
            :disabled="view.page >= totalPages"
            class="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
            @click="goToPage(view.page + 1)"
          >
            Siguiente
            <ChevronRight class="h-4 w-4" />
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
