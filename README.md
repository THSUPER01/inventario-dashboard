# 📦 Dashboard Inventario — GitHub Pages

Dashboard de inventario que se actualiza automáticamente cada vez que subes el archivo Excel al repositorio.

## 🌐 Ver el Dashboard
Una vez configurado: `https://<tu-usuario>.github.io/<nombre-repo>/`

---

## 🚀 Configuración inicial (una sola vez)

### 1. Crea el repositorio en GitHub
```
New repository → nombre: inventario-dashboard → Public → Create
```

### 2. Sube estos archivos
```bash
git clone https://github.com/<tu-usuario>/inventario-dashboard.git
# Copia todos estos archivos en la carpeta
git add .
git commit -m "Configuración inicial del dashboard"
git push origin main
```

### 3. Activa GitHub Pages
```
Repositorio → Settings → Pages → Source: GitHub Actions → Save
```

### 4. Permite que Actions escriba en el repo
```
Repositorio → Settings → Actions → General → Workflow permissions
→ Selecciona "Read and write permissions" → Save
```

---

## 🔄 Cómo actualizar el inventario

**Simplemente sube el Excel actualizado al repositorio:**

```bash
# Reemplaza el Excel con el nuevo
cp /ruta/a/tu/nuevo/Inventario_20_marzo.xlsx .

git add Inventario_20_marzo.xlsx
git commit -m "Actualizar inventario $(date +'%Y-%m-%d')"
git push origin main
```

### ¿Qué pasa automáticamente?
1. GitHub detecta el nuevo Excel
2. `GitHub Actions` ejecuta `scripts/excel_to_json.py`
3. Se genera `data/inventario.json` actualizado
4. El dashboard se redespliega en GitHub Pages
5. En ~2 minutos el dashboard muestra los datos nuevos ✅

---

## 📁 Estructura del proyecto

```
inventario-dashboard/
├── index.html                          # Dashboard web
├── Inventario_20_marzo.xlsx            # Archivo Excel de inventario
├── data/
│   └── inventario.json                 # Datos generados automáticamente
├── scripts/
│   └── excel_to_json.py               # Convertidor Excel → JSON
├── .github/
│   └── workflows/
│       └── update-dashboard.yml       # Automatización
└── README.md
```

---

## 🎛️ Funcionalidades del Dashboard

| Función | Descripción |
|--------|-------------|
| 🔍 Búsqueda | Por descripción o código de material |
| 🏭 Filtro Centro | CPB2, CPS1, CPT2 |
| 🏪 Filtro Almacén | Por número de almacén |
| 📊 Filtro Stock | Con stock / Sin stock |
| 📈 Gráficas | Donut por centro, barras por almacén, top 15 materiales |
| 📋 Tabla | Paginada, ordenable por cualquier columna |
| 🎨 Indicadores | Verde = stock alto, Amarillo = stock bajo, Gris = sin stock |

---

## 🛠️ Ejecución local (opcional)

```bash
# Instalar dependencias
pip install pandas openpyxl

# Generar JSON manualmente
python scripts/excel_to_json.py

# Ver el dashboard (necesitas un servidor local)
python -m http.server 8000
# Abre: http://localhost:8000
```
