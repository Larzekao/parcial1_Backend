import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { LoginPage } from './pages/LoginPage'
import { UsersPage } from './pages/UsersPage'
import { ProtectedRoute } from './components/ProtectedRoute'
import './index.css'

const RedirectIfAuthenticated: React.FC = () => {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? <Navigate to="/usuarios" replace /> : <LoginPage />
}

export const App: React.FC = () => (
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<RedirectIfAuthenticated />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/usuarios" element={<UsersPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/usuarios" replace />} />
      </Routes>
    </BrowserRouter>
  </AuthProvider>
)

export default App