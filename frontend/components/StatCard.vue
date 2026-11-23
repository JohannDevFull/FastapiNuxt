<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  label: string
  value: number
  hint: string
  icon: Component
  accent: 'blue' | 'amber' | 'indigo' | 'emerald'
}>()

const accents = {
  blue: 'bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400',
  amber: 'bg-amber-50 text-amber-600 dark:bg-amber-500/10 dark:text-amber-400',
  indigo: 'bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400',
  emerald: 'bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400',
}
</script>

<template>
  <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-card dark:border-slate-800 dark:bg-slate-900">
    <div class="flex items-start justify-between gap-4">
      <div>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400">{{ label }}</p>
        <p class="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
          {{ value }}
        </p>
      </div>
      <div class="flex h-10 w-10 items-center justify-center rounded-lg" :class="accents[accent]">
        <component :is="icon" class="h-5 w-5" />
      </div>
    </div>
    <p class="mt-3 text-xs text-slate-400 dark:text-slate-500">{{ hint }}</p>
  </div>
</template>
