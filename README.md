# Encuesta

Aplicación web de encuestas desarrollada con **Django REST Framework** y **React**.  
Permite crear encuestas, votar y visualizar resultados agregados en tiempo real.

---

# Tecnologías utilizadas

## Backend
- Python
- Django
- Django REST Framework
- drf-yasg (Swagger)
- PosgreSQL

## Frontend
- React
- Vite
- Axios

---

# Funcionalidades

## Backend
- Crear encuestas
- Listar encuestas
- Registrar votos
- Consultar resultados agregados
- Middleware personalizado para medir tiempo de respuesta
- Optimización de queries usando:
  - `prefetch_related`
  - `annotate`
  - `Count`

## Frontend
- Crear encuestas dinámicamente
- Agregar múltiples opciones
- Votar indicando identificador de usuario
- Ver resultados de encuestas
- Barras visuales de porcentaje
- Diseño responsive
- Manejo de errores y estados de carga

---

# Instalación

# 1. Clonar repositorio

```bash
git clone <repo-url>
cd project
```

---

# Backend

## Crear entorno virtual

Linux / Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar migraciones

```bash
python manage.py migrate
```

---

## Ejecutar servidor backend

```bash
python manage.py runserver
```

Backend disponible en:

```txt
http://localhost:8000
```

Swagger disponible en:

```txt
http://localhost:8000/swagger/
```

---

# Frontend

## Entrar al directorio

```bash
cd front
```

---

## Instalar dependencias

```bash
npm install
```

---

## Ejecutar frontend

```bash
npm run dev
```

Frontend disponible en:

```txt
http://localhost:9000
```

---

# API Endpoints

## Crear encuesta

```http
POST /questionnaire/polls/
```

### Body

```json
{
  "question": "¿Lenguaje favorito?",
  "choices": ["Python", "JavaScript", "Go"]
}
```

---

## Listar encuestas

```http
GET /questionnaire/polls/
```

---

## Registrar voto

```http
POST /questionnaire/vote/
```

### Body

```json
{
  "choice_id": 1,
  "user_identifier": "ariel"
}
```

---

## Obtener resultados

```http
GET /questionnaire/polls/{id}/results/
```

### Respuesta

```json
{
  "question": "¿Lenguaje favorito?",
  "total_votes": 10,
  "choices": [
    {
      "text": "Python",
      "votes": 6
    },
    {
      "text": "JavaScript",
      "votes": 4
    }
  ]
}
```

---

# Consideraciones técnicas

## ORM Optimization

Para evitar problemas de rendimiento y N+1 queries se utilizaron:

```python
prefetch_related()
annotate()
Count()
```

---

## Middleware personalizado

Cada respuesta incluye:

```txt
X-Process-Time
```

Ejemplo:

```txt
X-Process-Time: 120ms
```

---

# Validaciones implementadas

- Una encuesta debe tener mínimo 2 opciones
- Validación de opciones vacías
- Validación de existencia de `choice_id`
- Validación de identificador de usuario

---

# Posibles mejoras futuras

- Autenticación JWT
- Paginación
- Tests automatizados
- Docker
- PostgreSQL
- WebSockets para resultados en tiempo real
- Tema oscuro
- Estadísticas globales
- Rate limiting

---

# Autor

Ariel Plasencia Díaz

