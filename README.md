# Sistema de Administración de Condominios

Repositorio base para el proyecto multiplataforma (web + móvil) con backend en Django y PostgreSQL.

## Estructura

- `Backend/` – Proyecto Django/DRF con modelos y APIs para finanzas, seguridad, reservas y mantenimiento.
- `Frontend/` – Espacio reservado para la SPA en React.

## Requisitos iniciales

1. Crear entorno virtual en `Backend/` y activar.
2. Instalar dependencias: `pip install -r Backend/requirements.txt`.
3. Configurar variables de entorno (`Backend/.env`).
4. Ejecutar migraciones: `python manage.py migrate`.

Para más detalle consulta `Backend/README.md`.