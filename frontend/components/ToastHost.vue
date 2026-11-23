<script setup lang="ts">
import { CheckCircle2, AlertCircle, Info, X } from '@lucide/vue'
import { useToast, type ToastType } from '~/composables/useToast'

const { toasts, dismiss } = useToast()

const iconFor = (type: ToastType) => {
  if (type === 'success') return CheckCircle2
  if (type === 'error') return AlertCircle
  return Info
}

const classFor = (type: ToastType) => {
  if (type === 'success') {
    return 'border-emerald-200 bg-emerald-50 text-emerald-800 dark:border-emerald-500/30 dark:bg-emerald-500/10 dark:text-emerald-200'
  }
  if (type === 'error') {
    return 'border-rose-200 bg-rose-50 text-rose-800 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-200'
  }
  return 'border-blue-200 bg-blue-50 text-blue-800 dark:border-blue-500/30 dark:bg-blue-500/10 dark:text-blue-200'
}
</script>

<template>
  <div class="pointer-events-none fixed inset-x-0 top-4 z-[60] flex flex-col items-center gap-2 px-4 sm:items-end sm:px-6">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-xl border px-4 py-3 shadow-lg shadow-slate-900/5"
        :class="classFor(toast.type)"
      >
        <component :is="iconFor(toast.type)" class="mt-0.5 h-5 w-5 shrink-0" />
        <p class="flex-1 text-sm font-medium leading-5">{{ toast.message }}</p>
        <button
          type="button"
          class="rounded-md p-0.5 opacity-60 transition hover:opacity-100"
          aria-label="Cerrar notificación"
          @click="dismiss(toast.id)"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
