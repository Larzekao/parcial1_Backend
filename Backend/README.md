# Backend - Administrador de Condominios

Proyecto Django + Django REST Framework para la aplicacion movil y web de administracion de condominios. El diseno se basa en el diagrama entidad-relacion provisto e incluye dominios de finanzas, seguridad, reservas y mantenimiento.

## Requisitos

- Python 3.11+
- PostgreSQL 14+
- Entorno virtual recomendado (`python -m venv .venv`)

## Instalacion rapida

```bash
cd Backend
python -m venv .venv
.venv\\Scripts\\activate  # En Windows
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ajusta `.env` con las credenciales reales de tu instancia de PostgreSQL.

## Apps y modelos

- `core`
  - Usuario (modelo personalizado con rol, telefono, estado)
  - Rol, Residencia, Residente, Vehiculo, Mascota, Visitante
  - AreaComun, Horario, Regla, Reserva
  - Factura, DetalleFactura, ConceptoPago
  - Personal, Tarea

La migracion inicial se encuentra en `core/migrations/0001_initial.py`.

## Endpoints (`/api/`)

| Recurso | Ruta base |
| --- | --- |
| Roles | `/api/roles/` |
| Usuarios | `/api/usuarios/` |
| Residencias | `/api/residencias/` |
| Residentes | `/api/residentes/` |
| Mascotas | `/api/mascotas/` |
| Vehiculos | `/api/vehiculos/` |
| Visitantes | `/api/visitantes/` |
| Areas comunes | `/api/areas-comunes/` |
| Horarios | `/api/horarios/` |
| Reglas | `/api/reglas/` |
| Reservas | `/api/reservas/` |
| Conceptos de pago | `/api/conceptos-pago/` |
| Facturas | `/api/facturas/` |
| Detalles de factura | `/api/detalles-factura/` |
| Personal | `/api/personal/` |
| Tareas | `/api/tareas/` |

Todos los viewsets ofrecen operaciones CRUD, filtros basicos (`?estado=`, `?residente=`) y paginacion (20 items por pagina).

## Autenticacion

Por defecto se habilita autenticacion de sesion y basica de Django. Para clientes moviles se sugiere agregar `djangorestframework-simplejwt` u otro proveedor de tokens.

## Integracion con IA

- `Visitante` y `Vehiculo` incluyen campos preparados para almacenar capturas de vision artificial.
- `Reserva` y `Factura` proveen la base para analitica y prediccion de morosidad.
- Agrega un app dedicada (por ejemplo `ai_services`) para integrar SDKs de Microsoft, Amazon o Google.

## Pruebas

```bash
python manage.py test core
```

Se incluye una prueba basica que confirma que los endpoints requieren autenticacion.

## Proximos pasos sugeridos

1. Configurar autenticacion JWT y refresh tokens.
2. Implementar servicios de vision artificial (facial, OCR) y enlazarlos con los modelos ya creados.
3. Automatizar notificaciones (correo, push) usando Celery o servicios en la nube.