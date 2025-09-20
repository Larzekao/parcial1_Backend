import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { buildAuthHeader } from '../api/client'
import { getUsuarios } from '../api/users'

const STORAGE_KEY = 'smart-condo-auth'

interface AuthState {
  username: string
  authHeader: string
}

interface AuthContextValue {
  user: AuthState | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

const readStoredAuth = (): AuthState | null => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as AuthState
  } catch (error) {
    console.error('Error leyendo credenciales almacenadas', error)
    return null
  }
}

const storeAuth = (auth: AuthState | null) => {
  if (!auth) {
    localStorage.removeItem(STORAGE_KEY)
    return
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(auth))
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthState | null>(() => readStoredAuth())

  useEffect(() => {
    storeAuth(user)
  }, [user])

  const login = async (username: string, password: string) => {
    const authHeader = buildAuthHeader(username, password)
    // Validamos credenciales haciendo una solicitud simple
    await getUsuarios(authHeader, { page: 1 })
    setUser({ username, authHeader })
  }

  const logout = () => setUser(null)

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      login,
      logout,
    }),
    [user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider')
  }
  return context
}