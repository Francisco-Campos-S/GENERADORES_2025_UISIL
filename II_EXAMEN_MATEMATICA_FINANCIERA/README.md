# 📘 GENERADORES_UISIL_2025

👨‍🏫 Repositorio oficial del proyecto **GENERADORES DE EXÁMENES UISIL 2025**, desarrollado por **CodeEduLab**. Esta herramienta está diseñada para facilitar la generación automatizada de exámenes personalizados en LaTeX para cursos universitarios, a partir de listas de estudiantes en Excel.

---

## 📂 Estructura del proyecto

```
GENERADORES_UISIL_2025/
├── examen_template.tex        # Plantilla LaTeX base del examen
├── generar_examen.py         # Script principal para generar los exámenes
├── lista_estudiantes.xlsx    # Lista de estudiantes (formato Excel)
├── examenes_unicos/          # Carpeta donde se guardan los exámenes generados
├── out/                      # Salida de compilaciones LaTeX
├── .idea/                    # Configuración del entorno (IDE)
└── README.md                 # Documentación del proyecto
```

---

## ⚙️ Requisitos

- Python 3.x
- Paquetes:
  - `pandas`
  - `jinja2`
  - `tkinter` (incluido en la mayoría de instalaciones de Python)
- Motor LaTeX instalado (por ejemplo, [TeX Live](https://www.tug.org/texlive/))

Instalación de dependencias (si es necesario):

```bash
pip install pandas jinja2
```

---

## 🚀 ¿Cómo usar el generador?

1. 📥 Coloca tu archivo `lista_estudiantes.xlsx` con una columna llamada `Nombre`.
2. 🧪 Personaliza tu examen en el archivo `examen_template.tex`. Puedes usar `{{ estudiante }}` para insertar automáticamente el nombre del estudiante.
3. ▶️ Ejecuta el script:

```bash
python generar_examen.py
```

4. 📂 Se generarán los exámenes únicos dentro de la carpeta `examenes_unicos/`.

---

## 📌 Formato del Excel de entrada

El archivo debe tener la siguiente estructura:

| Nombre                     |
|---------------------------|
| ARIAS MARIN KENDY DAYANA  |
| FERNANDEZ FLORES YOSEF    |
| VARGAS GUTIERREZ JAIRO    |

---

## ✍️ Personalización del examen

Utiliza etiquetas de Jinja2 dentro del archivo `.tex` para insertar información dinámica. Ejemplo:

```latex
\textbf{Estudiante:} \textbf{{{{ estudiante }}}}
```

Puedes añadir secciones nuevas o modificar el diseño del examen desde la plantilla.

---

## 📦 Salida esperada

Por cada estudiante, se generará un archivo `.tex` y un `.pdf` individual, con su nombre incrustado automáticamente.

---

## 🧠 Créditos y propósito académico

Este proyecto fue desarrollado por docentes y colaboradores de **CodeEduLab** como parte de una iniciativa para apoyar la docencia universitaria en la **UISIL** durante el 2025.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes abrir un Pull Request o reportar errores en la sección de Issues.

---

## 🧾 Licencia

Este proyecto es de uso libre para fines educativos 🎓 bajo la licencia MIT.
