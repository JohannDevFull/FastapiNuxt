<script setup lang="ts">
import { Clock3, Package, CheckCircle2, Truck } from '@lucide/vue'
import { getApiErrorMessage } from '~/composables/useApiError'

definePageMeta({ layout: 'default' })

const { getDashboardData } = useShipments()

const { data, pending, error, refresh } = useAsyncData(
  'mini-cargoflow-dashboard',
  () => getDashboardData(),
  {
    default: () => ({
      total: 0,
      pending: 0,
      inTransit: 0,
      delivered: 0,
      recent: [],
    }),
  },
)

const stats = computed(() => data.value)
const errorMessage = computed(() =>
  error.value ? getApiErrorMessage(error.value, 'No se pudieron cargar los indicadores.') : '',
)
</script>

<template>
  <div>
    <PageHeader title="Dashboard" description="Resumen operativo de los envíos registrados en el sistema.">
      <template #actions>
        <NuxtLink
          to="/shipments/new"
          class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700"
        >
          <Package class="h-4 w-4" />
          Nuevo envío
        </NuxtLink>
      </template>
    </PageHeader>

    <LoadingState v-if="pending" label="Calculando indicadores..." />
    <ErrorState v-else-if="errorMessage" :message="errorMessage" retry @retry="refresh()" />

    <template v-else>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total de envíos" :value="stats.total" hint="Registros en el sistema" :icon="Package" accent="blue" />
        <StatCard label="Envíos pendientes" :value="stats.pending" hint="Estado PENDIENTE" :icon="Clock3" accent="amber" />
        <StatCard label="Envíos en tránsito" :value="stats.inTransit" hint="Estado IN_TRANSIT" :icon="Truck" accent="indigo" />
        <StatCard label="Envíos entregados" :value="stats.delivered" hint="Estado DELIVERED" :icon="CheckCircle2" accent="emerald" />
      </div>

      <section class="mt-6 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card dark:border-slate-800 dark:bg-slate-900">
        <div class="flex items-center justify-between gap-4 border-b border-slate-200 px-5 py-4 dark:border-slate-800">
          <div>
            <h2 class="text-sm font-semibold text-slate-900 dark:text-white">Últimos envíos registrados</h2>
            <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">Los cinco envíos más recientes según la API.</p>
          </div>
          <NuxtLink
            to="/shipments"
            class="inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:underline dark:text-blue-400"
          >
            Ver todos
          </NuxtLink>
        </div>

        <ShipmentTable v-if="stats.recent.length" :shipments="stats.recent" />
        <EmptyState v-else class="m-5" title="Aún no hay envíos" description="Cuando registres el primer envío aparecerá aquí." />
      </section>
    </template>
  </div>
</template>
