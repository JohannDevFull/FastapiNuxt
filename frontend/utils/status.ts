import type { ShipmentStatus } from '~/types/shipment'

const labels: Record<ShipmentStatus, string> = {
  PENDING: 'Pendiente',
  PICKED_UP: 'Recogido',
  IN_TRANSIT: 'En tránsito',
  OUT_FOR_DELIVERY: 'En reparto',
  DELIVERED: 'Entregado',
  CANCELLED: 'Cancelado',
}

const classes: Record<ShipmentStatus, string> = {
  PENDING:
    'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-300',
  PICKED_UP:
    'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-500/30 dark:bg-sky-500/10 dark:text-sky-300',
  IN_TRANSIT:
    'border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-500/30 dark:bg-indigo-500/10 dark:text-indigo-300',
  OUT_FOR_DELIVERY:
    'border-violet-200 bg-violet-50 text-violet-700 dark:border-violet-500/30 dark:bg-violet-500/10 dark:text-violet-300',
  DELIVERED:
    'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/30 dark:bg-emerald-500/10 dark:text-emerald-300',
  CANCELLED:
    'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-300',
}

const fallbackClass =
  'border-slate-200 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300'

export const getStatusLabel = (status: string) => {
  if (status in labels) {
    return labels[status as ShipmentStatus]
  }
  return status.replaceAll('_', ' ')
}

export const getStatusClasses = (status: string) => {
  if (status in classes) {
    return classes[status as ShipmentStatus]
  }
  return fallbackClass
}

export const statusOptions: Array<{ value: ShipmentStatus; label: string }> = (
  Object.keys(labels) as ShipmentStatus[]
).map((value) => ({ value, label: labels[value] }))
