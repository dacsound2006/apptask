# Publicar el proyecto en Git y desplegarlo

## 1. Arranque rápido (sin MySQL, para verificar que funciona)

El proyecto cae automáticamente a SQLite si no hay archivo `.env`. Para probar de inmediato:

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_tasks
python manage.py runserver
```

> Importante: usa siempre `python -m pip` (no `pip` suelto), para instalar en el venv correcto.

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

## 2. Activar MySQL (cuando quieras)

Crea la base de datos:

```sql
CREATE DATABASE cloudtasks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copia `backend/.env.example` a `backend/.env` y completa credenciales. En cuanto exista `DB_NAME`,
el proyecto usa MySQL automáticamente (vía PyMySQL, sin compilar nada).

## 3. Subir a GitHub / GitLab

Desde la raíz del proyecto (`E:\repositorio\apptask` o donde lo tengas):

```powershell
git init
git add .
git commit -m "App de control de tareas Dual Cloud (Django + Vue)"
git branch -M main
```

Crea un repositorio vacío en GitHub (sin README ni .gitignore, para no chocar) y luego:

```powershell
git remote add origin https://github.com/TU_USUARIO/apptask.git
git push -u origin main
```

> El archivo `.env` NO se sube (está en `.gitignore`). Solo se publica `.env.example`.

## 4. Publicar en la web (despliegue gratuito)

### Backend (Railway o Render)
- Servicio web Python apuntando a `backend/`.
- Build: `pip install -r requirements.txt`
- Start: `gunicorn cloudtasks.wsgi --chdir backend`
- Variables de entorno: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=tu-dominio`,
  y las de MySQL (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
- Tras el primer deploy: ejecutar `python manage.py migrate` y `python manage.py seed_tasks`.

### Frontend (Vercel o Netlify)
- Build: `npm run build` (genera `dist/`).
- Antes de desplegar, en `src/api.js` cambia `baseURL` por la URL pública del backend.

## Checklist antes del push
- [ ] El backend arranca con `runserver` (aunque sea en SQLite).
- [ ] El frontend compila con `npm run build`.
- [ ] Existe `.env.example` y NO existe `.env` en el commit.
- [ ] `node_modules/`, `db.sqlite3` y `.env` están ignorados.
