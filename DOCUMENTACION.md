# Regresión Lineal Múltiple — Denuncias de Acoso Escolar en EE.UU.

## Descripción

Página web estática con análisis de regresión lineal múltiple sobre denuncias de acoso e intimidación en escuelas de EE.UU. durante el ciclo 2015–16. Los datos provienen del Departamento de Educación de EE.UU., Oficina de Derechos Civiles (OCR).

El modelo predice el **número total de acusaciones** por estado a partir de:

- **Número de escuelas** en el estado
- **Porcentaje de escuelas que informan** datos a la OCR

---

## Estructura del proyecto

```
Regresion lineal/
├── manage.py                  # Entry point de Django
├── requirements.txt           # Dependencias Python
├── runtime.txt                # Versión de Python (3.12.3)
├── Procfile                   # Despliegue en Heroku/Railway
├── index.html                 # Página web estática (documentación)
├── Ski-Learn.py               # Script de regresión lineal con scikit-learn
├── regresion_lineal.txt       # Documentación detallada del análisis
├── digitalocean_config.txt    # Configuración de despliegue
├── db.sqlite3                 # Base de datos SQLite (Django)
├── venv/                      # Entorno virtual
├── .git/                      # Repositorio git
├── .gitignore
├── ia_app/                    # Aplicación Django
│   ├── templates/ia_app/      # Templates HTML
│   ├── static/                # Archivos estáticos
│   ├── views.py               # Vista única que renderiza index.html
│   ├── models.py              # Modelos (vacíos)
│   ├── admin.py
│   ├── apps.py
│   └── migrations/
└── ia_project/                # Configuración Django
    ├── settings.py            # Settings con Whitenoise, SQLite
    ├── urls.py                # Ruta raíz → views.index
    ├── wsgi.py                # WSGI para producción
    └── asgi.py
```

---

## Requisitos

- Python 3.12.3
- Django 6.0.5
- scikit-learn 1.8.0
- pandas 3.0.3
- numpy 2.4.6
- gunicorn 23.0.0
- whitenoise 6.9.0

Ver `requirements.txt` para la lista completa.

---

## Instalación y ejecución local

```bash
# 1. Clonar o entrar al directorio
cd "Regresion lineal"

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar servidor de desarrollo
python manage.py runserver
```

Abrir `http://127.0.0.1:8000` en el navegador.

---

## Script de regresión lineal (`Ski-Learn.py`)

### Flujo

1. **Carga de datos** – Dataset embebido con 51 observaciones (50 estados + DC)
2. **Separación** – Predictoras (`Escuelas`, `Porcentaje_reporta`) y objetivo (`Total_acusaciones`)
3. **División** – 70% entrenamiento / 30% prueba (`random_state=42`)
4. **Escalado** – `StandardScaler` (media 0, desviación 1)
5. **Entrenamiento** – `LinearRegression` de scikit-learn
6. **Evaluación** – R², RMSE, MAE
7. **Validación cruzada** – 5 folds sobre entrenamiento
8. **Comparación** – Modelo simple solo con `Escuelas` vs modelo múltiple

### Resultados esperados

| Métrica | Valor esperado |
|---------|---------------|
| R² (test) | ~0.85–0.90 |
| RMSE | ~2500–3500 |
| MAE | ~1500–2500 |
| R² CV (5 folds) | ~0.80–0.88 |

### Ejecución

```bash
python Ski-Learn.py
```

---

## Despliegue

### Heroku / Railway

El `Procfile` incluye:

```
web: gunicorn ia_project.wsgi --bind 0.0.0.0:$PORT
release: python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

Pasos:

```bash
# Configurar variables de entorno en la plataforma
DJANGO_SECRET_KEY = <tu_secreto>
DJANGO_DEBUG = False
CSRF_TRUSTED_ORIGINS = https://tudominio.com
```

### DigitalOcean

Ver `digitalocean_config.txt` para configuración específica.

---

## Análisis de datos

### Variables

**Independientes (predictoras):**
- `Estado` – Categórica nominal (contexto fijo)
- `Num_escuelas` – Cuantitativa discreta (infraestructura)
- `Porc_escuelas_informan` – Cuantitativa continua (cobertura de reporte)

**Dependientes (respuesta):**
- `Total_acusaciones` – Variable objetivo principal
- 5 subtipos de intimidación (sexo/raza, discapacidad, orientación sexual, religión)

### Preprocesamiento detectado

| Problema | Solución |
|----------|----------|
| Coma decimal en lugar de punto | Reemplazar `,` → `.` |
| Espacios en nombres de columnas | `.strip()` |
| Marcador `!` en Distrito de Columbia | Advertencia de calidad |
| Florida: 149 acusaciones (sospechoso) | Investigar posible subreporte |
| Outlier: total nacional (z=6.92) | Excluir del modelo |
| Sin duplicados ni nulos | Dataset limpio |

---

## Rutas de la API (Django)

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/` | `views.index` | Página principal con análisis |
| `/admin/` | admin | Panel de administración Django |

---

## Licencia

Datos: Departamento de Educación de EE.UU., Oficina de Derechos Civiles, 2015–16.
