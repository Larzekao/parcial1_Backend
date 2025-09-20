# Smart Condominium – Frontend Web

Aplicacion web en React + Vite para la suite "Smart Condominium". Este primer modulo cubre la gestion de usuarios conectandose al backend Django previamente construido.

## Stack

- Vite + React 18 + TypeScript
- React Router 6
- Context API para sesion básica (autenticacion con Basic Auth contra el backend)

## Requisitos previos

- Node.js 18+ y npm 9+
- Backend desplegado localmente o accesible via HTTP (por defecto `http://127.0.0.1:8000`).

## Configuracion rapida

```bash
cd Frontend
cp .env.example .env           # Ajusta VITE_API_BASE_URL si es necesario
npm install
npm run dev
```

Para compilar produccion: `npm run build`. El servidor de previsualizacion se inicia con `npm run preview`.

## Modulo actual: Usuarios

- Login protegido (usa credenciales de superusuario/administrador del backend).
- Listado paginado de usuarios (`/api/usuarios/`).
- Filtros por texto y estado.
- Creacion, edicion (incluye asignacion de rol y cambio de estado) y eliminacion.
- Catálogo de roles (`/api/roles/`) para mostrar nombres legibles.

## Estructura de carpetas destacada

```
src/
  api/          -> clientes HTTP tipados (usuarios, roles)
  components/   -> layout, tabla y modal reutilizables
  context/      -> AuthProvider (Basic Auth con persistencia en localStorage)
  hooks/        -> `useUsuarios` maneja estado de lista y CRUD
  pages/        -> pantallas Login y Usuarios
  types/        -> tipados compartidos (Usuario, Rol)
```

## Pendientes sugeridos

1. Integrar gestion de sesiones con tokens (por ejemplo JWT) en lugar de Basic Auth.
2. Añadir manejo de permisos/grupos en UI y módulos restantes (finanzas, reservas, IA).
3. Incorporar una librería de componentes (Material UI, Chakra, Tailwind) para escalabilidad del diseño.
4. Conectar notificaciones en tiempo real via WebSockets o servicios push.