# 🎨 Instagram Scraper - Frontend React

Dashboard moderno para visualizar los datos extraídos del scraper de Instagram.

## 🚀 Instalación

### 1. Instalar dependencias
```bash
npm install
```

### 2. Ejecutar en desarrollo
```bash
npm run dev
```

Esto abrirá automáticamente `http://localhost:3000` en tu navegador.

## 📊 Características

- ✨ Dashboard moderno y responsivo
- 👥 Selector de múltiples usuarios
- 📱 Visualización de posts con estadísticas
- 💾 Lee datos del JSON generado por el scraper
- 🔄 Auto-refresh cada 5 segundos
- 📊 Estadísticas agregadas (totales y promedios)

## 📁 Estructura

- `src/App.jsx` - Componente principal
- `src/index.css` - Estilos globales
- `index.html` - Página HTML principal

## 🔗 Flujo de datos

1. Ejecuta `python main.py` en la carpeta padre
2. El scraper actualiza `scraping_data.json`
3. El frontend React lee esos archivos automáticamente
4. Los datos se muestran en el dashboard

## 📦 Build para producción

```bash
npm run build
```

Esto genera la carpeta `dist/` lista para desplegar.

## 🛠️ Tecnologías

- React 18
- Vite
- CSS3 (Grid, Flexbox)
- Axios (para fetch de datos)
