export const trackingEndpoints = {
  byShipmentId: (id: number) => `/shipments/${id}/tracking`,
  byTrackingNumber: (trackingNumber: string) =>
    `/tracking/${encodeURIComponent(trackingNumber)}`,
}
