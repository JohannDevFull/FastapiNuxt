<script setup lang="ts">
import { Boxes, Moon, Sun } from '@lucide/vue'

const { theme, toggle, init } = useTheme()

onMounted(init)
</script>

<template>
  <div class="flex min-h-screen flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <header class="border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
      <div class="mx-auto flex h-16 w-full max-w-5xl items-center justify-between px-4 sm:px-6">
        <NuxtLink to="/" class="flex items-center gap-3">
          <span class="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white shadow-sm">
            <Boxes class="h-5 w-5" />
          </span>
          <span>
            <span class="block text-sm font-semibold leading-tight text-slate-900 dark:text-white">Mini CargoFlow</span>
            <span class="block text-xs text-slate-400 dark:text-slate-500">Consulta pública</span>
          </span>
        </NuxtLink>

        <div class="flex items-center gap-2">
          <NuxtLink
            to="/"
            class="hidden rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 sm:inline-flex"
          >
            Panel administrativo
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
        </div>
      </div>
    </header>

    <main class="mx-auto w-full max-w-5xl flex-1 px-4 py-10 sm:px-6">
      <slot />
    </main>

    <footer class="border-t border-slate-200 py-5 text-center text-xs text-slate-400 dark:border-slate-800 dark:text-slate-500">
      Mini CargoFlow V1 · La consulta pública muestra únicamente el estado y la trazabilidad del envío.
    </footer>
  </div>
</template>
