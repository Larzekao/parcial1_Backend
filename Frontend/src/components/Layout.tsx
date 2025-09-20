import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Layout.css'

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuth()

  return (
    <div className="layout">
      <header className="layout__header">
        <div>
          <h1>Smart Condominium</h1>
          <p className="layout__subtitle">Panel de administracion</p>
        </div>
        <nav className="layout__nav">
          <Link to="/usuarios">Usuarios</Link>
          <button type="button" onClick={logout} className="layout__logout">
            Cerrar sesion
          </button>
          {user ? <span className="layout__user">Sesion: {user.username}</span> : null}
        </nav>
      </header>
      <main className="layout__main">{children}</main>
    </div>
  )
}