# Control de Tareas — Despliegue Dual Cloud (INTERNEXA)

App de control y seguimiento de tareas para los proyectos **Renovación Thunder Cloud** (cloud privado)
e **Internexa–Check Point / BEC** (cloud público). Stack **Django REST Framework + Vue 3**.

## Qué incluye

- **Backend Django** con API REST: CRUD de tareas, endpoints de dashboard, tareas de la semana y atrasadas.
- **Frontend Vue 3 (Vite)**: dashboard con KPIs, gráficos (Chart.js), tabla con filtros, búsqueda, orden, y edición de tareas.
- **67 tareas precargadas** del plan (fuente única `tasks_seed.json`), con fechas del acta y cierres ajustados:
  cloud privado **01-jul-2026**, cloud público **31-jul-2026**.
- Panel de **administración Django** para edición masiva.

## KPIs del dashboard
Total · Esta semana (vencen ≤7 días) · Atrasadas (vencidas y no completadas) · Pendientes · En curso · Completadas (% avance).

## Vistas del frontend
- **Dashboard**: KPIs, gráfico de avance por fase, dona de estado, tabla con filtros/búsqueda/orden y CRUD.
- **% de avance**: anillo global + barras por proyecto (privado/público) con tareas hechas, atrasadas y días al cierre.
- **Gantt**: cronograma enero–julio 2026, barras por tarea con % de avance, línea de "hoy" y líneas de cierre de cada proyecto.
- **Críticas y recomendaciones**: ranking de tareas críticas (por atraso, bloqueo de dependientes y cercanía al cierre) con recomendaciones accionables priorizadas.

### Endpoint adicional
| GET | `/api/tasks/critical/` | Tareas críticas con score y recomendaciones |

## Requisitos
- Python 3.11+
- Node 18+
- **MySQL 8.0+** (servidor propio, ya existente)
- Para compilar `mysqlclient`: en Debian/Ubuntu `sudo apt install default-libmysqlclient-dev build-essential pkg-config`; en Windows usar el wheel de `mysqlclient`.

## Base de datos MySQL

El backend se alimenta de **MySQL** mediante variables de entorno. Crea la base de datos en tu servidor:

```sql
CREATE DATABASE cloudtasks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copia `backend/.env.example` a `backend/.env` y completa tus credenciales:

```
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=cloudtasks
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

## Backend (local)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# asegúrate de tener backend/.env con las credenciales MySQL
python manage.py migrate
python manage.py seed_tasks          # carga las 67 tareas del plan en MySQL
python manage.py createsuperuser     # opcional, para el admin
python manage.py runserver           # http://localhost:8000
```

API disponible en `http://localhost:8000/api/tasks/`
Admin en `http://localhost:8000/admin/`

### Endpoints principales
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/tasks/` | Lista (filtros: `?project=PRIV&status=pending&phase=...`, `?search=`, `?ordering=due`) |
| POST | `/api/tasks/` | Crear tarea |
| PATCH | `/api/tasks/{id}/` | Modificar tarea |
| DELETE | `/api/tasks/{id}/` | Eliminar tarea |
| GET | `/api/tasks/dashboard/` | KPIs y avance por fase |
| GET | `/api/tasks/week/` | Tareas que vencen en 7 días |
| GET | `/api/tasks/late/` | Tareas atrasadas |

## Frontend (local)

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173 (proxy /api -> :8000)
```

Para producción: `npm run build` genera `dist/`.

## Despliegue gratuito (Railway / Render)

1. Sube este repo a GitHub.
2. **Backend**: crea un servicio web Python apuntando a `backend/`.
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn cloudtasks.wsgi --chdir backend`
   - Variables: `DEBUG=False`, `SECRET_KEY=...`, `ALLOWED_HOSTS=tu-dominio`, y las de MySQL (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
   - Tras el primer deploy: `python manage.py migrate && python manage.py seed_tasks`.
3. **Frontend**: build estático (`npm run build`) servido en Vercel/Netlify, apuntando `baseURL` de `src/api.js` a la URL del backend.

## Integración con el resto del plan
`tasks_seed.json` es la **misma fuente** que alimenta el dashboard inmediato (`dashboard_dual_cloud.html`)
y se corresponde con el WBS en Excel y el documento maestro de arquitectura.
