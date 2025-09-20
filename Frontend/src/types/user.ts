export interface Rol {
  id: number
  nombre: string
}

export interface UsuarioForm {
  username: string
  email: string
  telefono?: string
  estado: boolean
  rol?: number | null
  password?: string
  first_name?: string
  last_name?: string
}

export interface Usuario extends UsuarioForm {
  id: number
}