export const shipmentEndpoints = {
  create: () => '/shipments',
  list: (page = 1, pageSize = 10) => `/shipments?page=${page}&page_size=${pageSize}`,
  detail: (id: number) => `/shipments/${id}`,
  byTrackingNumber: (trackingNumber: string) =>
    `/shipments/tracking/${encodeURIComponent(trackingNumber)}`,
  status: (id: number) => `/shipments/${id}/status`,
  tracking: (id: number) => `/shipments/${id}/tracking`,
}
