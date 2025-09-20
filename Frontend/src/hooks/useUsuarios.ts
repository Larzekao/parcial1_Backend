import { useCallback, useEffect, useMemo, useState } from 'react'
import { createUsuario, deleteUsuario, getUsuarios, updateUsuario } from '../api/users'
import type { Usuario, UsuarioForm } from '../types/user'

interface UseUsuariosOptions {
  authHeader: string
}

export const useUsuarios = ({ authHeader }: UseUsuariosOptions) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [estado, setEstado] = useState<string>('')
  const [data, setData] = useState<{ count: number; results: Usuario[] }>({ count: 0, results: [] })

  const fetchUsuarios = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await getUsuarios(authHeader, { page, search, estado })
      setData({ count: response.count, results: response.results })
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error cargando usuarios'
      setError(message)
    } finally {
      setLoading(false)
    }
  }, [authHeader, estado, page, search])

  useEffect(() => {
    void fetchUsuarios()
  }, [fetchUsuarios])

  const create = useCallback(
    async (payload: UsuarioForm) => {
      await createUsuario(authHeader, payload)
      await fetchUsuarios()
    },
    [authHeader, fetchUsuarios],
  )

  const update = useCallback(
    async (id: number, payload: Partial<UsuarioForm>) => {
      await updateUsuario(authHeader, id, payload)
      await fetchUsuarios()
    },
    [authHeader, fetchUsuarios],
  )

  const remove = useCallback(
    async (id: number) => {
      await deleteUsuario(authHeader, id)
      await fetchUsuarios()
    },
    [authHeader, fetchUsuarios],
  )

  const totalPages = useMemo(() => Math.max(1, Math.ceil(data.count / 20)), [data.count])

  return {
    usuarios: data.results,
    total: data.count,
    totalPages,
    loading,
    error,
    page,
    setPage,
    search,
    setSearch,
    estado,
    setEstado,
    refresh: fetchUsuarios,
    create,
    update,
    remove,
  }
}