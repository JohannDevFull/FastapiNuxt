export const SHIPMENT_STATUSES = [
  'PENDING',
  'PICKED_UP',
  'IN_TRANSIT',
  'OUT_FOR_DELIVERY',
  'DELIVERED',
  'CANCELLED',
] as const

export type ShipmentStatus = (typeof SHIPMENT_STATUSES)[number]

export interface Shipment {
  id: number
  tracking_number: string
  sender_name: string
  sender_phone: string
  recipient_name: string
  recipient_phone: string
  origin_address: string
  destination_address: string
  package_description: string
  weight_kg: number
  status: ShipmentStatus
  created_at: string
  updated_at: string
}

export interface ShipmentListResponse {
  items: Shipment[]
  total: number
  page: number
  page_size: number
}

export interface TrackingEvent {
  id: number
  shipment_id: number
  previous_status: string
  new_status: string
  observation: string | null
  created_at: string
}

export interface ShipmentCreatePayload {
  sender_name: string
  sender_phone: string
  recipient_name: string
  recipient_phone: string
  origin_address: string
  destination_address: string
  package_description: string
  weight_kg: number
}

export type ShipmentUpdatePayload = Partial<ShipmentCreatePayload>

export interface ShipmentStatusUpdatePayload {
  new_status: ShipmentStatus
  observation?: string | null
}

export interface DashboardStats {
  total: number
  pending: number
  inTransit: number
  delivered: number
  recent: Shipment[]
}

export interface PublicShipmentView {
  tracking_number: string
  status: ShipmentStatus
  created_at: string
  updated_at: string
}
