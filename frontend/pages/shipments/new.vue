<script setup lang="ts">
import { ref } from 'vue'
import { getApiErrorMessage } from '~/composables/useApiError'
import type { ShipmentCreatePayload } from '~/types/shipment'

definePageMeta({ layout: 'default' })

useHead({ title: 'Nuevo envío' })

const router = useRouter()
const toast = useToast()
const { create } = useShipments()

const submitting = ref(false)
const errorMessage = ref('')

const handleSubmit = async (payload: ShipmentCreatePayload) => {
  submitting.value = true
  errorMessage.value = ''

  try {
    const created = await create(payload)
    toast.success('Envío registrado correctamente.')
    await router.push(`/shipments/${created.id}`)
  } catch (error) {
    errorMessage.value = getApiErrorMessage(error, 'No se pudo registrar el envío.')
    toast.error(errorMessage.value)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div>
    <PageHeader title="Nuevo envío" description="Registra un envío. El número de guía y el estado inicial los genera la API." />

    <div
      v-if="errorMessage"
      class="mb-5 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-300"
    >
      {{ errorMessage }}
    </div>

    <ShipmentForm :submitting="submitting" submit-label="Registrar envío" @submit="handleSubmit" />
  </div>
</template>
