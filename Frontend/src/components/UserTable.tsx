import type { Rol, Usuario } from '../types/user'
import './UserTable.css'

interface Props {
  usuarios: Usuario[]
  roles: Rol[]
  loading?: boolean
  onEdit: (usuario: Usuario) => void
  onDelete: (usuario: Usuario) => void
}

const getRolNombre = (rolId: number | null | undefined, roles: Rol[]) =>
  roles.find((rol) => rol.id === rolId)?.nombre ?? 'Sin rol'

export const UserTable: React.FC<Props> = ({ usuarios, roles, loading = false, onEdit, onDelete }) => {
  if (loading) {
    return <div className="table__placeholder">Cargando usuarios...</div>
  }

  if (!usuarios.length) {
    return <div className="table__placeholder">No existen usuarios registrados.</div>
  }

  return (
    <div className="table__wrapper">
      <table className="user-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Telefono</th>
            <th>Rol</th>
            <th>Estado</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((usuario) => (
            <tr key={usuario.id}>
              <td>{usuario.username}</td>
              <td>{`${usuario.first_name ?? ''} ${usuario.last_name ?? ''}`.trim() || '—'}</td>
              <td>{usuario.email || '—'}</td>
              <td>{usuario.telefono || '—'}</td>
              <td>{getRolNombre(usuario.rol ?? null, roles)}</td>
              <td>
                <span className={usuario.estado ? 'badge badge--success' : 'badge badge--danger'}>
                  {usuario.estado ? 'Activo' : 'Inactivo'}
                </span>
              </td>
              <td>
                <div className="table__actions">
                  <button type="button" onClick={() => onEdit(usuario)}>
                    Editar
                  </button>
                  <button type="button" className="danger" onClick={() => onDelete(usuario)}>
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}