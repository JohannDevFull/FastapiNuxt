<script setup lang="ts">
useHead({
  titleTemplate: (title) => (title ? `${title} · Mini CargoFlow` : 'Mini CargoFlow'),
  meta: [
    { name: 'description', content: 'Panel administrativo y consulta pública de envíos Mini CargoFlow.' },
  ],
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <ToastHost />
</template>
