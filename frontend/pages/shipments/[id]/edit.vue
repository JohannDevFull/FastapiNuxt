<script setup lang="ts">
import { computed, ref } from 'vue'
import { getApiErrorMessage } from '~/composables/useApiError'
import type { ShipmentCreatePayload } from '~/types/shipment'

definePageMeta({ layout: 'default' })

const route = useRoute()
const router = useRouter()
const toast = useToast()
const id = computed(() => Number(route.params.id) || 0)

const { useDetail, update } = useShipments()
const detail = useDetail(id)

const submitting = ref(false)
const errorMessage = computed(() =>
  detail.error.value ? getApiErrorMessage(detail.error.value, 'No se pudo cargar el envío.') : '',
)

const handleSubmit = async (payload: ShipmentCreatePayload) => {
  submitting.value = true
  try {
    await update(id.value, payload)
    toast.success('Los datos del envío se actualizaron correctamente.')
    await router.push(`/shipments/${id.value}`)
  } catch (error) {
    toast.error(getApiErrorMessage(error, 'No se pudo actualizar el envío.'))
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div>
    <PageHeader title="Editar envío" description="Modifica los datos del envío. La API valida los cambios permitidos." />

    <LoadingState v-if="detail.pending.value" label="Cargando envío..." />
    <ErrorState v-else-if="errorMessage" :message="errorMessage" retry @retry="detail.refresh()" />
    <EmptyState v-else-if="!detail.data.value" title="Envío no encontrado" description="El identificador solicitado no existe." />
    <ShipmentForm
      v-else
      :initial="detail.data.value"
      :submitting="submitting"
      submit-label="Guardar cambios"
      @submit="handleSubmit"
    />
  </div>
</template>
