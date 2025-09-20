import { useEffect, useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import type { Rol, Usuario, UsuarioForm } from '../types/user'
import './UserFormModal.css'

interface Props {
  open: boolean
  roles: Rol[]
  title: string
  initialData?: Usuario | null
  submitting?: boolean
  onClose: () => void
  onSubmit: (values: UsuarioForm) => Promise<void>
}

const defaultData: UsuarioForm = {
  username: '',
  email: '',
  telefono: '',
  estado: true,
  rol: null,
  password: '',
  first_name: '',
  last_name: '',
}

export const UserFormModal: React.FC<Props> = ({ open, roles, title, initialData, submitting = false, onClose, onSubmit }) => {
  const [form, setForm] = useState<UsuarioForm>(defaultData)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (initialData) {
      setForm({
        username: initialData.username,
        email: initialData.email,
        telefono: initialData.telefono,
        estado: initialData.estado,
        rol: initialData.rol ?? null,
        password: '',
        first_name: initialData.first_name ?? '',
        last_name: initialData.last_name ?? '',
      })
    } else {
      setForm(defaultData)
    }
    setError(null)
  }, [initialData, open])

  if (!open) {
    return null
  }

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const target = event.currentTarget
    const { name, value } = target

    setForm((prev) => {
      if (name === 'estado') {
        if (target instanceof HTMLInputElement) {
          return { ...prev, estado: target.checked }
        }
        return prev
      }

      if (name === 'rol') {
        return { ...prev, rol: value ? Number(value) : null }
      }

      return {
        ...prev,
        [name]: value,
      }
    })
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)

    try {
      await onSubmit(form)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'No se pudo guardar el usuario'
      setError(message)
      return
    }

    onClose()
  }

  return (
    <div className="modal__backdrop">
      <div className="modal">
        <header className="modal__header">
          <h2>{title}</h2>
          <button type="button" onClick={onClose} className="modal__close" aria-label="Cerrar">
            x
          </button>
        </header>
        <form className="modal__body" onSubmit={handleSubmit}>
          {error ? <p className="modal__error">{error}</p> : null}
          <div className="modal__grid">
            <label>
              Usuario
              <input name="username" value={form.username} onChange={handleChange} required autoComplete="off" />
            </label>
            <label>
              Correo
              <input type="email" name="email" value={form.email} onChange={handleChange} />
            </label>
            <label>
              Nombre(s)
              <input name="first_name" value={form.first_name ?? ''} onChange={handleChange} />
            </label>
            <label>
              Apellidos
              <input name="last_name" value={form.last_name ?? ''} onChange={handleChange} />
            </label>
            <label>
              Telefono
              <input name="telefono" value={form.telefono ?? ''} onChange={handleChange} />
            </label>
            <label>
              Rol
              <select name="rol" value={form.rol ?? ''} onChange={handleChange}>
                <option value="">Sin asignar</option>
                {roles.map((rol) => (
                  <option key={rol.id} value={rol.id}>
                    {rol.nombre}
                  </option>
                ))}
              </select>
            </label>
            {!initialData && (
              <label>
                Contrasena temporal
                <input name="password" type="password" value={form.password ?? ''} onChange={handleChange} required />
              </label>
            )}
            {initialData && (
              <label>
                Contrasena (opcional)
                <input name="password" type="password" value={form.password ?? ''} onChange={handleChange} placeholder="Dejar en blanco para mantener" />
              </label>
            )}
            <label className="modal__checkbox">
              <input type="checkbox" name="estado" checked={form.estado} onChange={handleChange} /> Activo
            </label>
          </div>
          <footer className="modal__footer">
            <button type="button" className="ghost" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" disabled={submitting}>
              {submitting ? 'Guardando...' : 'Guardar'}
            </button>
          </footer>
        </form>
      </div>
    </div>
  )
}