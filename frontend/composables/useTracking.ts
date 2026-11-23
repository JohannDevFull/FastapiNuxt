import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { trackingEndpoints } from '~/services/tracking'
import type { TrackingEvent } from '~/types/shipment'

export const useTracking = () => {
  const { baseURL, request } = useApi()

  const byShipmentId = (id: number) =>
    request<TrackingEvent[]>(trackingEndpoints.byShipmentId(id))

  const byTrackingNumber = (trackingNumber: string) =>
    request<TrackingEvent[]>(trackingEndpoints.byTrackingNumber(trackingNumber))

  const useByShipmentId = (id: MaybeRefOrGetter<number>) => {
    const url = computed(() => trackingEndpoints.byShipmentId(toValue(id)))

    return useFetch<TrackingEvent[]>(url, {
      baseURL,
      watch: [url],
    })
  }

  return { byShipmentId, byTrackingNumber, useByShipmentId }
}
