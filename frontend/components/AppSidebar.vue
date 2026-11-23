<script setup lang="ts">
import type { Component } from 'vue'
import {
  LayoutDashboard,
  Package,
  Search,
  Plus,
  Boxes,
  X,
} from '@lucide/vue'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const route = useRoute()

interface NavItem {
  label: string
  to: string
  icon: Component
  exact?: boolean
}

const items: NavItem[] = [
  { label: 'Dashboard', to: '/', icon: LayoutDashboard, exact: true },
  { label: 'Envíos', to: '/shipments', icon: Package },
  { label: 'Consulta pública', to: '/track', icon: Search },
]

const isActive = (item: NavItem) =>
  item.exact ? route.path === item.to : route.path.startsWith(item.to)
</script>

<template>
  <aside
    class="fixed inset-y-0 left-0 z-40 flex w-64 transform flex-col border-r border-slate-200 bg-white transition-transform duration-200 dark:border-slate-800 dark:bg-slate-900 lg:translate-x-0"
    :class="open ? 'translate-x-0' : '-translate-x-full'"
  >
    <div class="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
      <NuxtLink to="/" class="flex items-center gap-3" @click="emit('close')">
        <span class="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white shadow-sm">
          <Boxes class="h-5 w-5" />
        </span>
        <span>
          <span class="block text-sm font-semibold leading-tight text-slate-900 dark:text-white">Mini CargoFlow</span>
          <span class="block text-xs text-slate-400 dark:text-slate-500">Panel administrativo</span>
        </span>
      </NuxtLink>
      <button
        type="button"
        class="rounded-md p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-800 lg:hidden"
        aria-label="Cerrar menú"
        @click="emit('close')"
      >
        <X class="h-5 w-5" />
      </button>
    </div>

    <nav class="flex-1 space-y-1 overflow-y-auto px-3 py-5">
      <p class="mb-2 px-3 text-xs font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500">
        Navegación
      </p>
      <NuxtLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition"
        :class="isActive(item)
          ? 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-300'
          : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white'"
        @click="emit('close')"
      >
        <component :is="item.icon" class="h-4 w-4" />
        {{ item.label }}
      </NuxtLink>

      <div class="pt-6">
        <p class="mb-2 px-3 text-xs font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500">
          Acciones rápidas
        </p>
        <NuxtLink
          to="/shipments/new"
          class="flex items-center gap-3 rounded-lg border border-dashed border-slate-200 px-3 py-2 text-sm font-medium text-slate-500 transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700 dark:border-slate-700 dark:text-slate-400 dark:hover:border-blue-500/40 dark:hover:bg-blue-500/10 dark:hover:text-blue-300"
          @click="emit('close')"
        >
          <Plus class="h-4 w-4" />
          Nuevo envío
        </NuxtLink>
      </div>
    </nav>

    <div class="border-t border-slate-200 px-5 py-4 dark:border-slate-800">
      <p class="text-xs text-slate-400 dark:text-slate-500">Mini CargoFlow V1</p>
    </div>
  </aside>
</template>
