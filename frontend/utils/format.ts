const buildFormatter = (options: Intl.DateTimeFormatOptions) =>
  new Intl.DateTimeFormat('es-CO', options)

const longFormatter = buildFormatter({
  dateStyle: 'medium',
  timeStyle: 'short',
})

const shortFormatter = buildFormatter({
  day: '2-digit',
  month: 'short',
  year: 'numeric',
})

export const formatDateTime = (value: string | null | undefined) => {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return longFormatter.format(date)
}

export const formatDate = (value: string | null | undefined) => {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return shortFormatter.format(date)
}
