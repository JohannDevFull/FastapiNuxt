export type ToastType = 'success' | 'error' | 'info'

export interface Toast {
  id: number
  type: ToastType
  message: string
}

export const useToast = () => {
  const toasts = useState<Toast[]>('mini-cargoflow-toasts', () => [])

  const dismiss = (id: number) => {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  const push = (type: ToastType, message: string) => {
    const id = Date.now() + Math.floor(Math.random() * 1000)
    toasts.value = [...toasts.value, { id, type, message }]

    if (import.meta.client) {
      window.setTimeout(() => dismiss(id), 5000)
    }
  }

  return {
    toasts,
    success: (message: string) => push('success', message),
    error: (message: string) => push('error', message),
    info: (message: string) => push('info', message),
    dismiss,
  }
}
