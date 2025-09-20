import { apiRequest } from './client'
import type { Rol, Usuario, UsuarioForm } from '../types/user'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

const buildQueryString = (params: Record<string, string | number | undefined>) => {
  const searchParams = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return
    }
    searchParams.append(key, String(value))
  })
  const query = searchParams.toString()
  return query ? `?${query}` : ''
}

export const getRoles = (authHeader: string) =>
  apiRequest<Rol[]>(`/api/roles/`, { authHeader })

export const getUsuarios = (
  authHeader: string,
  options: { page?: number; search?: string; estado?: string } = {},
) => {
  const query = buildQueryString({ page: options.page, search: options.search, estado: options.estado })
  return apiRequest<PaginatedResponse<Usuario>>(`/api/usuarios/${query}`, { authHeader })
}

export const createUsuario = (authHeader: string, payload: UsuarioForm) =>
  apiRequest<Usuario>(`/api/usuarios/`, {
    method: 'POST',
    authHeader,
    json: payload,
  })

export const updateUsuario = (authHeader: string, id: number, payload: Partial<UsuarioForm>) =>
  apiRequest<Usuario>(`/api/usuarios/${id}/`, {
    method: 'PATCH',
    authHeader,
    json: payload,
  })

export const deleteUsuario = (authHeader: string, id: number) =>
  apiRequest<void>(`/api/usuarios/${id}/`, {
    method: 'DELETE',
    authHeader,
  })