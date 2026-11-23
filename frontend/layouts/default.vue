<script setup lang="ts">
import { ref, watch } from 'vue'

const sidebarOpen = ref(false)
const route = useRoute()
const { init } = useTheme()

watch(
  () => route.fullPath,
  () => {
    sidebarOpen.value = false
  },
)

onMounted(init)
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <AppSidebar :open="sidebarOpen" @close="sidebarOpen = false" />

    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-30 bg-slate-900/50 backdrop-blur-sm lg:hidden"
      @click="sidebarOpen = false"
    />

    <div class="lg:pl-64">
      <AppHeader @toggle-sidebar="sidebarOpen = true" />
      <main class="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <slot />
      </main>
    </div>
  </div>
</template>
