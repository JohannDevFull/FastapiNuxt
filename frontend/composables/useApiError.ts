interface FastApiValidationItem {
  loc?: Array<string | number>
  msg?: string
  type?: string
}

interface ApiErrorShape {
  statusCode?: number
  status?: number
  data?: {
    detail?: string | FastApiValidationItem[]
    message?: string
  }
}

export const getApiErrorMessage = (error: unknown, fallback = 'Ocurrió un error inesperado.') => {
  const apiError = error as ApiErrorShape
  const detail = apiError?.data?.detail

  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }

  if (Array.isArray(detail)) {
    const messages = detail.map((item) => {
      const field = Array.isArray(item.loc)
        ? item.loc.filter((part) => part !== 'body' && part !== 'query').join('.')
        : ''
      return field ? `${field}: ${item.msg || 'valor inválido'}` : item.msg || 'valor inválido'
    })
    if (messages.length) {
      return messages.join(' · ')
    }
  }

  if (apiError?.data?.message) {
    return apiError.data.message
  }

  return fallback
}

export const isNotFoundError = (error: unknown) => {
  const apiError = error as ApiErrorShape
  return apiError?.statusCode === 404 || apiError?.status === 404
}
