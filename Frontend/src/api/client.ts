const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

interface RequestOptions extends Omit<RequestInit, 'body'> {
  authHeader?: string
  json?: unknown
  body?: BodyInit | null | Record<string, unknown>
}

const isBodyInit = (value: unknown): value is BodyInit =>
  value instanceof Blob ||
  value instanceof FormData ||
  value instanceof URLSearchParams ||
  value instanceof ReadableStream ||
  typeof value === 'string' ||
  value instanceof ArrayBuffer ||
  ArrayBuffer.isView(value as ArrayBufferView)

export const buildAuthHeader = (username: string, password: string) => {
  const token = window.btoa(`${username}:${password}`)
  return `Basic ${token}`
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { authHeader, json, body, headers, ...rest } = options
  const url = path.startsWith('http') ? path : `${API_BASE_URL}${path}`

  const finalHeaders = new Headers(headers)
  let finalBody: BodyInit | undefined

  if (authHeader) {
    finalHeaders.set('Authorization', authHeader)
  }

  if (json !== undefined) {
    finalHeaders.set('Content-Type', 'application/json')
    finalBody = JSON.stringify(json)
  } else if (body !== undefined && body !== null) {
    if (isBodyInit(body)) {
      finalBody = body
    } else {
      finalHeaders.set('Content-Type', 'application/json')
      finalBody = JSON.stringify(body)
    }
  }

  const response = await fetch(url, {
    ...rest,
    headers: finalHeaders,
    body: finalBody,
  })

  if (response.status === 204) {
    return undefined as T
  }

  if (!response.ok) {
    let detail = ''
    try {
      const data = await response.json()
      detail = typeof data === 'string' ? data : JSON.stringify(data)
    } catch (error) {
      detail = response.statusText
    }
    throw new Error(detail || 'Error en la solicitud al servidor')
  }

  return (await response.json()) as T
}

export { API_BASE_URL }