# COMANDOS.md — Despliegue paso a paso (Windows PowerShell)

Copia y pega cada bloque en orden. Reemplaza lo que esté en MAYÚSCULAS.

---

## 0. Prueba local antes de publicar (opcional pero recomendado)

```powershell
# Posicionarse en el backend
cd E:\repositorio\apptask\backend

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\Activate.ps1

# Instalar dependencias (SIEMPRE con python -m pip, no pip suelto)
python -m pip install -r requirements.txt

# Sin .env arranca en SQLite. Migrar, cargar tareas y correr
python manage.py migrate
python manage.py seed_tasks
python manage.py runserver
# -> http://localhost:8000/api/tasks/dashboard/   (Ctrl+C para parar)
```

Frontend en otra terminal:

```powershell
cd E:\repositorio\apptask\frontend
npm install
npm run dev
# -> http://localhost:5173
```

---

## 1. Cargar el código a GitHub

```powershell
# Posicionarse en la raíz del proyecto
cd E:\repositorio\apptask

# Inicializar git (si la carpeta NO viene ya con .git)
git init
git add .
git commit -m "App de control de tareas Dual Cloud (Django + Vue)"
git branch -M main

# Conectar el repositorio remoto (créalo VACÍO en GitHub primero)
git remote add origin https://github.com/TU_USUARIO/apptask.git

# Subir
git push -u origin main
```

> Si el ZIP ya traía `.git` con commits, omite `git init/add/commit` y ve directo a `git remote add` + `git push`.

Para cambios posteriores:

```powershell
git add .
git commit -m "Describe el cambio"
git push
```

---

## 2. Backend + MySQL en Railway

### Opción A — Desde GitHub (interfaz web, recomendado)
No requiere comandos: railway.app → New Project → Deploy from GitHub repo → tu repo →
New → Database → Add MySQL. Variables y dominio se configuran en la web
(ver `DESPLIEGUE_RAILWAY_VERCEL.md`).

### Opción B — Con la CLI de Railway (desde tu máquina)

```powershell
# Instalar la CLI (requiere Node)
npm i -g @railway/cli

# Iniciar sesión (abre el navegador)
railway login

# Posicionarse en la raíz del proyecto
cd E:\repositorio\apptask

# Crear/enlazar un proyecto
railway init

# Agregar el plugin de MySQL al proyecto
railway add --plugin mysql

# Definir variables de entorno del backend
railway variables --set "SECRET_KEY=PON_UNA_CLAVE_LARGA_ALEATORIA"
railway variables --set "DEBUG=False"
railway variables --set "ALLOWED_HOSTS=.railway.app"

# Desplegar el código actual
railway up

# Generar el dominio público (o hazlo en la web: Settings -> Networking)
railway domain
```

Ver logs y confirmar la carga a MySQL ("Tareas cargadas: 67"):

```powershell
railway logs
```

Crear superusuario para el panel /admin (opcional):

```powershell
railway run python backend/manage.py createsuperuser
```

Forzar recarga de tareas en MySQL manualmente (si lo necesitas):

```powershell
railway run python backend/manage.py seed_tasks
```

---

## 3. Frontend en Vercel

### Opción A — Desde GitHub (interfaz web, recomendado)
vercel.com → Add New → Project → importa el repo → **Root Directory = frontend** →
Environment Variables: `VITE_API_URL = https://TU-BACKEND.up.railway.app` → Deploy.

### Opción B — Con la CLI de Vercel

```powershell
# Instalar la CLI
npm i -g vercel

# Iniciar sesión
vercel login

# Posicionarse en el frontend
cd E:\repositorio\apptask\frontend

# Definir la URL del backend (sin /api al final)
vercel env add VITE_API_URL
# pega: https://TU-BACKEND.up.railway.app  (elige Production)

# Desplegar a producción
vercel --prod
```

---

## 4. Cerrar el círculo (CORS)

Una vez tengas la URL de Vercel, dásela al backend para que acepte sus peticiones:

```powershell
# Con la CLI de Railway, desde E:\repositorio\apptask
railway variables --set "FRONTEND_URL=https://TU-APP.vercel.app"
railway up
```

(O en la web: Railway → backend → Variables → `FRONTEND_URL`.)

---

## 5. Verificación final

```powershell
# El API responde JSON
curl https://TU-BACKEND.up.railway.app/api/tasks/dashboard/

# Abrir el frontend en el navegador
start https://TU-APP.vercel.app
```

Debes ver el dashboard con las 67 tareas cargadas desde MySQL en Railway.

---

## Recordatorios
- Usa **`python -m pip`**, no `pip` suelto (evita instalar en el venv equivocado).
- El archivo `.env` NUNCA se sube (está en `.gitignore`); en producción las variables van en Railway/Vercel.
- La carga a MySQL ocurre automáticamente en cada deploy vía `backend/start.sh`.
- Orden correcto: GitHub → Railway → Vercel → `FRONTEND_URL` en Railway.
