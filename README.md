# Instagram Scraper

## Cómo usar

### 1. Clonar el repositorio

```bash
git clone https://github.com/Marlonftc/scraping-instagram.git
cd scraping-instagram
```

---

### 2. Configurar backend (Python)

Activar el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
playwright install
```

---

### 3. Generar cookies (login una vez)

```powershell
python login.py
```

Inicia sesión manualmente en el navegador.
Esto generará el archivo `cookies.json`.

---

### 4. Ejecutar el backend

```powershell
uvicorn backend.api:app --reload --port 5000
```

---

### 5. Ejecutar el frontend

```bash
cd frontend
npm install
npm run dev
```

Abrir en el navegador:

```
http://localhost:5173
```

---

### 6. Usar la aplicación

* Ingresar un usuario de Instagram
* Presionar **Buscar**
* Esperar a que termine el scraping
* Ver los resultados en pantalla

---

## Archivos generados

* `scraping_data.json`
* `scraping_data.xlsx`
