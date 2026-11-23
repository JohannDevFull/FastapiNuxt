<script setup lang="ts">
import { computed } from 'vue'
import { Menu, Moon, Sun, ExternalLink } from '@lucide/vue'

const emit = defineEmits<{
  'toggle-sidebar': []
}>()

const route = useRoute()
const { theme, toggle } = useTheme()

const title = computed(() => {
  const path = route.path
  if (path === '/') return 'Dashboard'
  if (path === '/shipments') return 'Envíos'
  if (path === '/shipments/new') return 'Nuevo envío'
  if (path.includes('/edit')) return 'Editar envío'
  if (path.startsWith('/shipments/')) return 'Detalle del envío'
  return 'Mini CargoFlow'
})
</script>

<template>
  <header class="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-slate-200 bg-white/85 px-4 backdrop-blur dark:border-slate-800 dark:bg-slate-950/85 sm:px-6">
    <button
      type="button"
      class="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 lg:hidden"
      aria-label="Abrir menú"
      @click="emit('toggle-sidebar')"
    >
      <Menu class="h-5 w-5" />
    </button>

    <div class="min-w-0 flex-1">
      <h2 class="truncate text-base font-semibold text-slate-900 dark:text-white">{{ title }}</h2>
      <p class="hidden text-xs text-slate-400 dark:text-slate-500 sm:block">Gestión y seguimiento de envíos</p>
    </div>

    <NuxtLink
      to="/track"
      class="hidden items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 sm:inline-flex"
    >
      Consulta pública
      <ExternalLink class="h-3.5 w-3.5" />
    </NuxtLink>

    <button
      type="button"
      class="rounded-lg border border-slate-200 bg-white p-2 text-slate-500 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800"
      :aria-label="theme === 'dark' ? 'Activar modo claro' : 'Activar modo oscuro'"
      @click="toggle"
    >
      <Sun v-if="theme === 'dark'" class="h-4 w-4" />
      <Moon v-else class="h-4 w-4" />
    </button>
  </header>
</template>
