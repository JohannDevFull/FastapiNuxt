# Mini CargoFlow — Frontend Nuxt 3

Frontend administrativo y consulta pública para la API real de Mini CargoFlow V1. No incluye autenticación, base de datos propia ni datos simulados.

## Requisitos

- Node.js 20+
- npm 10+
- Backend FastAPI de `../minicargoflow` en ejecución con MySQL

## Instalación

```powershell
cd frontend
npm install
Copy-Item .env.example .env
```

`.env`:

```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api/v1
```

El backend debe estar escuchando en `http://127.0.0.1:8000`. Si usas otro host o puerto, ajusta la variable anterior.

## Ejecución

```powershell
cd ../minicargoflow
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

En otra terminal:

```powershell
cd frontend
npm run dev
```

URLs:

- Frontend: `http://localhost:3000`
- Consulta pública: `http://localhost:3000/track`
- Swagger: `http://127.0.0.1:8000/docs`

## Scripts

| Comando | Descripción |
| --- | --- |
| `npm run dev` | Servidor de desarrollo Nuxt |
| `npm run build` | Build de producción |
| `npm run preview` | Sirve el build de producción |
| `npm run typecheck` | Chequeo de tipos con `vue-tsc` |
| `npm run generate` | Genera sitio estático |

## Pantallas

| Ruta | Descripción |
| --- | --- |
| `/` | Dashboard con indicadores reales y últimos envíos |
| `/shipments` | Listado paginado, búsqueda por guía y filtro por estado |
| `/shipments/new` | Creación de envío |
| `/shipments/[id]` | Detalle, cambio de estado, cancelación y trazabilidad |
| `/shipments/[id]/edit` | Edición de datos del envío |
| `/track` | Consulta pública por número de guía |

## Endpoints integrados

Todas las rutas se construyen a partir de `NUXT_PUBLIC_API_BASE`.

| Método | Endpoint | Uso en el frontend |
| --- | --- | --- |
| `POST` | `/shipments` | Crear envío |
| `GET` | `/shipments?page&page_size` | Listado paginado, dashboard, filtro por estado |
| `GET` | `/shipments/tracking/{tracking_number}` | Búsqueda exacta y consulta pública |
| `GET` | `/shipments/{id}` | Detalle y formulario de edición |
| `PUT` | `/shipments/{id}` | Editar envío |
| `PATCH` | `/shipments/{id}/status` | Cambiar estado |
| `DELETE` | `/shipments/{id}` | Cancelar envío |
| `GET` | `/shipments/{id}/tracking` | Trazabilidad en el detalle |
| `GET` | `/tracking/{tracking_number}` | Trazabilidad en la consulta pública |

## Decisiones de integración

- El backend no expone un endpoint de estadísticas; el dashboard obtiene todas las páginas de `/shipments` y calcula los contadores a partir de esos registros reales.
- El listado usa la paginación del backend. La búsqueda por guía usa el endpoint exacto por número de guía. El backend no acepta `status` en el listado, por lo que el filtro por estado se aplica sobre los registros obtenidos de la API.
- Las transiciones de estado no se validan en Nuxt: se envía el estado elegido y el backend responde `409` con el mensaje correspondiente.
- La consulta pública llama únicamente a endpoints `GET` y construye una vista local con `tracking_number`, `status` y fechas. No renderiza nombres, teléfonos ni direcciones.
- Se agregó `CORSMiddleware` al backend porque el navegador necesita consumir la API desde otro origen. Se controla con `CORS_ALLOWED_ORIGINS` (por defecto, `*`).

## Estructura

```text
frontend/
├── components/    Componentes Vue reutilizables
├── composables/   Capa de servicios HTTP, errores, tema y notificaciones
├── layouts/       Shell administrativo y layout público
├── pages/         Rutas de la aplicación
├── services/      Constructores de rutas de la API
├── types/         Contratos TypeScript derivados de los esquemas Pydantic
└── utils/         Formato de fechas y presentación de estados
```

## Manejo de estados

- Carga: `LoadingState` y estados `pending` de `useFetch`/`useAsyncData`.
- Errores HTTP: `getApiErrorMessage` interpreta `detail` como texto o como errores de validación 422 de FastAPI.
- Respuestas vacías: `EmptyState`.
- Éxito: notificaciones globales de `ToastHost`.
- Tema: modo claro/oscuro persistido en `localStorage`.

## Pruebas realizadas

- `npm run typecheck`: correcto.
- `npm run build`: correcto.
- Integración real contra la API: creación de envío, listado paginado, búsqueda por guía, consulta pública por guía, cambio de estado, trazabilidad por ID y por guía, edición, cancelación y respuesta `409` en una transición inválida.
- Trazabilidad verificada: evento inicial `PENDING` y segundo evento `PICKED_UP` con su observación.
- Preflight CORS verificado: `OPTIONS /api/v1/shipments` responde `200` con `Access-Control-Allow-Origin`.
- Smoke test SSR con el build de producción: `/`, `/shipments`, `/shipments/new` y `/track` respondieron `200`; las pantallas con datos mostraron la guía creada (`MCF-20261121-879048`) y el destinatario actualizado (`Ana Ruiz`).
