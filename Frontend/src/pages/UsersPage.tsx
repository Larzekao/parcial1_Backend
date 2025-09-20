import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Layout } from '../components/Layout'
import { UserTable } from '../components/UserTable'
import { UserFormModal } from '../components/UserFormModal'
import { useUsuarios } from '../hooks/useUsuarios'
import { getRoles } from '../api/users'
import type { Rol, UsuarioForm, Usuario } from '../types/user'
import './UsersPage.css'

export const UsersPage: React.FC = () => {
  const { user } = useAuth()
  if (!user) {
    throw new Error('Usuario no autenticado')
  }

  const usuariosState = useUsuarios({ authHeader: user.authHeader })
  const {
    usuarios,
    loading,
    error,
    page,
    setPage,
    totalPages,
    search,
    setSearch,
    estado,
    setEstado,
    create,
    update,
    remove,
  } = usuariosState

  const [roles, setRoles] = useState<Rol[]>([])
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<Usuario | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [feedback, setFeedback] = useState<string | null>(null)

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const data = await getRoles(user.authHeader)
        setRoles(data)
      } catch (err) {
        console.error('No se pudieron cargar los roles', err)
      }
    }
    void fetchRoles()
  }, [user.authHeader])

  useEffect(() => {
    if (page !== 1) {
      setPage(1)
    }
  }, [estado, page, search, setPage])

  const handleCreateRequest = () => {
    setSelected(null)
    setModalOpen(true)
  }

  const handleEditRequest = (usuario: Usuario) => {
    setSelected(usuario)
    setModalOpen(true)
  }

  const handleDelete = async (usuario: Usuario) => {
    const confirmed = window.confirm(`Eliminar al usuario ${usuario.username}?`)
    if (!confirmed) return
    try {
      await remove(usuario.id)
      setFeedback('Usuario eliminado correctamente')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'No se pudo eliminar el usuario'
      setFeedback(message)
    }
  }

  const handleSubmit = async (form: UsuarioForm) => {
    setSubmitting(true)
    try {
      if (selected) {
        const payload = { ...form }
        if (!payload.password) {
          delete payload.password
        }
        await update(selected.id, payload)
        setFeedback('Usuario actualizado correctamente')
      } else {
        await create(form)
        setFeedback('Usuario creado exitosamente')
      }
    } catch (err) {
      throw err instanceof Error ? err : new Error('No se pudo guardar el usuario')
    } finally {
      setSubmitting(false)
    }
  }

  const handleSearchSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  useEffect(() => {
    if (!feedback) return
    const timeout = setTimeout(() => setFeedback(null), 4000)
    return () => clearTimeout(timeout)
  }, [feedback])

  const estadoOptions = useMemo(
    () => [
      { value: '', label: 'Todos' },
      { value: 'true', label: 'Activos' },
      { value: 'false', label: 'Inactivos' },
    ],
    [],
  )

  return (
    <Layout>
      <section className="users">
        <header className="users__header">
          <div>
            <h2>Gestion de usuarios</h2>
            <p>Administra accesos, roles y estados de cuenta.</p>
          </div>
          <button type="button" onClick={handleCreateRequest}>
            + Nuevo usuario
          </button>
        </header>

        <form className="users__filters" onSubmit={handleSearchSubmit}>
          <div className="field">
            <label>Buscar</label>
            <input
              placeholder="Nombre de usuario, correo o telefono"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>
          <div className="field">
            <label>Estado</label>
            <select value={estado} onChange={(event) => setEstado(event.target.value)}>
              {estadoOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="ghost">
            Aplicar filtros
          </button>
        </form>

        {error ? <div className="users__error">{error}</div> : null}
        {feedback ? <div className="users__feedback">{feedback}</div> : null}

        <UserTable usuarios={usuarios} roles={roles} loading={loading} onEdit={handleEditRequest} onDelete={handleDelete} />

        <div className="users__pagination">
          <button type="button" disabled={page <= 1} onClick={() => setPage(page - 1)}>
            Anterior
          </button>
          <span>
            Pagina {page} de {totalPages}
          </span>
          <button type="button" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>
            Siguiente
          </button>
        </div>
      </section>

      <UserFormModal
        open={modalOpen}
        roles={roles}
        title={selected ? 'Editar usuario' : 'Crear usuario'}
        initialData={selected ?? undefined}
        onClose={() => {
          setModalOpen(false)
          setSelected(null)
        }}
        onSubmit={handleSubmit}
        submitting={submitting}
      />
    </Layout>
  )
}