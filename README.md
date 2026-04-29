# Instagram Scraper

Aplicación de web scraping que extrae información de perfiles públicos de Instagram utilizando Python y Playwright, y muestra los resultados en una interfaz web desarrollada con React y Vite.

---

## Cómo usar

### 1. Clonar el repositorio

```bash id="6y3ktw"
git clone https://github.com/Marlonftc/scraping-instagram.git
cd scraping-instagram
```

---

### 2. Configurar backend (Python)

Activar el entorno virtual:

```powershell id="ozg7fi"
.\venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell id="nb7o2s"
pip install -r requirements.txt
playwright install
```

---

### 3. Generar cookies (login una vez)

```powershell id="9xfwsi"
python login.py
```

Inicia sesión manualmente en el navegador.
Esto generará el archivo `cookies.json`.

---

### 4. Ejecutar el backend

```powershell id="3z6f5l"
uvicorn backend.api:app --reload --port 5000
```

---

### 5. Ejecutar el frontend

```bash id="w3whgl"
cd frontend
npm install
npm run dev
```

Abrir en el navegador:

```id="9x5y6j"
http://localhost:5173
```

---

### 6. Usar la aplicación

* Ingresar un usuario de Instagram
* Presionar **Buscar**
* Esperar a que termine el scraping
* Visualizar los resultados en pantalla

---

## Funcionamiento

El scraping se realiza mediante Playwright, que permite automatizar un navegador real (Chromium) para acceder a la página de Instagram y extraer la información desde el contenido renderizado (DOM).

En lugar de utilizar solicitudes HTTP directas, se simula el comportamiento de un usuario real, lo que permite acceder a contenido dinámico cargado con JavaScript.

Para mantener la sesión iniciada sin exponer credenciales, se utiliza un archivo `cookies.json`, generado previamente mediante un proceso de login manual.

---

## Archivos generados

* `scraping_data.json`: archivo con los datos obtenidos del scraping
* `scraping_data.xlsx`: archivo en formato Excel con la información estructurada

---

## Limitaciones

Instagram restringe el acceso a ciertos datos debido a su estructura dinámica y a las políticas de la plataforma.

Durante el desarrollo se identificó una limitación importante al intentar extraer información de los reels, ya que este tipo de contenido utiliza una estructura diferente y no siempre expone los datos en el DOM de forma accesible.

Además, fue necesario ajustar tiempos de espera (`wait_for_timeout`) y realizar desplazamientos (scroll) para permitir que la página cargue correctamente los datos antes de extraerlos. Esto se debe a que Instagram carga el contenido de manera dinámica, lo que puede provocar que algunos elementos no estén disponibles inmediatamente.

Por estas razones, el sistema se enfoca en publicaciones estándar (posts), donde los datos son más consistentes y accesibles.
