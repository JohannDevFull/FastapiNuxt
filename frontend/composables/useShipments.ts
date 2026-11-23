import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { shipmentEndpoints } from '~/services/shipments'
import type {
  DashboardStats,
  Shipment,
  ShipmentCreatePayload,
  ShipmentListResponse,
  ShipmentStatusUpdatePayload,
  ShipmentUpdatePayload,
} from '~/types/shipment'

export const useShipments = () => {
  const { baseURL, request } = useApi()

  const list = (page = 1, pageSize = 10) =>
    request<ShipmentListResponse>(shipmentEndpoints.list(page, pageSize))

  const getById = (id: number) => request<Shipment>(shipmentEndpoints.detail(id))

  const getByTrackingNumber = (trackingNumber: string) =>
    request<Shipment>(shipmentEndpoints.byTrackingNumber(trackingNumber))

  const create = (payload: ShipmentCreatePayload) =>
    request<Shipment>(shipmentEndpoints.create(), { method: 'POST', body: payload })

  const update = (id: number, payload: ShipmentUpdatePayload) =>
    request<Shipment>(shipmentEndpoints.detail(id), { method: 'PUT', body: payload })

  const updateStatus = (id: number, payload: ShipmentStatusUpdatePayload) =>
    request<Shipment>(shipmentEndpoints.status(id), { method: 'PATCH', body: payload })

  const cancel = (id: number) =>
    request<void>(shipmentEndpoints.detail(id), { method: 'DELETE' })

  const fetchAllPages = async () => {
    const pageSize = 100
    const first = await list(1, pageSize)
    const items = [...first.items]
    const totalPages = Math.ceil(first.total / pageSize)

    for (let page = 2; page <= totalPages; page += 1) {
      const batch = await list(page, pageSize)
      items.push(...batch.items)
    }

    return { items, first }
  }

  const getAll = async () => (await fetchAllPages()).items

  const getDashboardData = async (): Promise<DashboardStats> => {
    const { items, first } = await fetchAllPages()

    return {
      total: first.total,
      pending: items.filter((shipment) => shipment.status === 'PENDING').length,
      inTransit: items.filter((shipment) => shipment.status === 'IN_TRANSIT').length,
      delivered: items.filter((shipment) => shipment.status === 'DELIVERED').length,
      recent: first.items.slice(0, 5),
    }
  }

  const useList = (page: MaybeRefOrGetter<number>, pageSize: MaybeRefOrGetter<number> = 10) => {
    const url = computed(() => shipmentEndpoints.list(toValue(page), toValue(pageSize)))

    return useFetch<ShipmentListResponse>(url, {
      baseURL,
      watch: [url],
    })
  }

  const useDetail = (id: MaybeRefOrGetter<number>) => {
    const url = computed(() => shipmentEndpoints.detail(toValue(id)))

    return useFetch<Shipment>(url, {
      baseURL,
      watch: [url],
    })
  }

  return {
    baseURL,
    list,
    getAll,
    getById,
    getByTrackingNumber,
    getDashboardData,
    create,
    update,
    updateStatus,
    cancel,
    useList,
    useDetail,
  }
}
