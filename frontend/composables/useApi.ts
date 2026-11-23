type ApiMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

interface ApiRequestOptions {
  method?: ApiMethod
  body?: unknown
  query?: Record<string, string | number | boolean | undefined>
}

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = String(config.public.apiBase || 'http://localhost:8000/api/v1')

  const request = <T>(path: string, options: ApiRequestOptions = {}) =>
    $fetch<T>(path, {
      baseURL,
      method: options.method,
      body: options.body as Record<string, unknown> | undefined,
      query: options.query,
    })

  return { baseURL, request }
}
