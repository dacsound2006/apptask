# Despliegue: Backend en Railway + Frontend en Vercel

Arquitectura: **Backend Django + MySQL en Railway**, **Frontend Vue en Vercel**.

---

## PARTE 1 — Backend + MySQL en Railway

### 1. Subir el repo a GitHub
(Si aún no lo has hecho — ver `PUBLICAR.md`.)

### 2. Crear el proyecto en Railway
1. Entra a https://railway.app → **New Project** → **Deploy from GitHub repo**.
2. Selecciona tu repositorio `apptask`.
3. Railway detecta `nixpacks.toml` / `railway.json` y construye el backend automáticamente.

### 3. Agregar MySQL
1. Dentro del proyecto: **New** → **Database** → **Add MySQL**.
2. Railway crea la base y expone automáticamente las variables `MYSQLHOST`, `MYSQLPORT`,
   `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`.
3. El backend ya está preparado para leerlas: **no tienes que copiar nada manualmente**,
   siempre que ambos servicios estén en el mismo proyecto y se compartan las variables.
   - Si el servicio backend no ve las variables del MySQL, ve a su pestaña **Variables** →
     **Add Reference** → selecciona las `MYSQL*` del plugin.

### 4. Variables de entorno del backend
En el servicio backend → **Variables**, agrega:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | una clave larga aleatoria |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.railway.app` (o tu dominio) |
| `FRONTEND_URL` | la URL de Vercel (la tendrás tras la Parte 2; puedes ponerla después) |

> `RAILWAY_PUBLIC_DOMAIN` la inyecta Railway sola; el backend la agrega a `ALLOWED_HOSTS` y CSRF automáticamente.

### 5. Generar dominio público
En el servicio backend → **Settings** → **Networking** → **Generate Domain**.
Te dará algo como `https://apptask-production.up.railway.app`.

### 6. Carga de datos
El script `backend/start.sh` ejecuta en cada deploy, **en MySQL**:
- `migrate` (crea tablas)
- `seed_tasks` (carga las 67 tareas, es idempotente: no duplica)
- `collectstatic`

Así que la carga a MySQL es automática en el primer despliegue. Para revisarla:
Railway → servicio backend → pestaña **Deployments** → **View Logs**, busca
`Tareas cargadas: 67`.

### 7. Crear superusuario (opcional, para el /admin)
En Railway, pestaña del backend → **Settings** → **Service** → ejecuta un comando one-off,
o desde la CLI de Railway:

```bash
railway run python backend/manage.py createsuperuser
```

---

## PARTE 2 — Frontend en Vercel

### 1. Importar el repo
1. https://vercel.com → **Add New** → **Project** → importa `apptask`.
2. En **Root Directory** selecciona **`frontend`**.
3. Framework: **Vite** (lo detecta solo). Build: `npm run build`. Output: `dist`.

### 2. Variable de entorno
En el proyecto de Vercel → **Settings** → **Environment Variables**:

| Variable | Valor |
|---|---|
| `VITE_API_URL` | la URL pública del backend en Railway (sin `/api`), p.ej. `https://apptask-production.up.railway.app` |

### 3. Deploy
**Deploy**. Vercel te dará una URL como `https://apptask.vercel.app`.

### 4. Cerrar el círculo (CORS)
Vuelve a Railway → backend → **Variables** → pon `FRONTEND_URL` con la URL de Vercel
(`https://apptask.vercel.app`). Railway redeploya y el backend aceptará peticiones del frontend.

---

## Verificación final
1. Abre la URL de Vercel → el dashboard debe cargar las 67 tareas desde Railway/MySQL.
2. Crea/edita una tarea → debe persistir (recarga y sigue ahí).
3. `https://TU-BACKEND.up.railway.app/api/tasks/dashboard/` debe responder JSON.
4. `https://TU-BACKEND.up.railway.app/admin/` debe abrir el admin.

## Notas
- La carga inicial a MySQL la hace `start.sh` automáticamente en cada deploy.
- Para recargar/forzar el seed manualmente: `railway run python backend/manage.py seed_tasks`.
- El frontend en desarrollo local sigue usando el proxy de Vite (`npm run dev`), sin variable.
