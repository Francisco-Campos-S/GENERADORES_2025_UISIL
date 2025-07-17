import pandas as pd
import random
import subprocess
from jinja2 import Environment, FileSystemLoader
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def formato_monto(valor):
    return "{:,.2f}".format(valor)

def generar_examen_unico(ruta_excel):
    try:
        # Leer sin encabezado para buscar la fila del encabezado real
        df = pd.read_excel(ruta_excel, header=None)
        fila_encabezado = None
        for i, row in df.iterrows():
            if row.astype(str).str.contains('Nombre', case=False, na=False).any():
                fila_encabezado = i
                break

        if fila_encabezado is None:
            messagebox.showerror("Error", "No se encontró la fila con el encabezado 'Nombre'")
            return

        df = pd.read_excel(ruta_excel, header=fila_encabezado)
        df.columns = df.columns.str.strip().str.lstrip(':').str.rstrip(':')

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo Excel:\n{e}")
        return

    if 'Nombre' not in df.columns:
        messagebox.showerror("Error", f"El archivo Excel debe tener una columna llamada 'Nombre'.\n"
                             f"Columnas encontradas: {df.columns.tolist()}")
        return

    env = Environment(loader=FileSystemLoader('.'))
    try:
        template = env.get_template('examen_template.tex')
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró la plantilla examen_template.tex:\n{e}")
        return

    # Carpeta y nombre del archivo único
    output_folder = 'examenes_unicos'
    os.makedirs(output_folder, exist_ok=True)
    archivo_tex_unico = os.path.join(output_folder, 'examen_completo.tex')

    # Armamos el preámbulo del documento completo (lo sacamos de la plantilla)
    # O podemos leer directamente el preámbulo de la plantilla para no repetir
    # Pero aquí asumimos que la plantilla solo tiene el cuerpo, así que vamos a escribir un preámbulo básico

    preambulo = r"""
\documentclass[14pt]{article}
\usepackage[a4paper, left=2cm, right=2cm, top=2cm, bottom=2cm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\lhead{UISIL \\ ISB-24 INGENIERÍA EN SISTEMAS}
\rhead{\today}
\renewcommand{\headrulewidth}{1pt}
\renewcommand{\footrulewidth}{0.5pt}
\lfoot{\textbf{Elaborado por: Francisco Campos S.}}
\cfoot{\thepage}

\begin{document}
"""

    cierre = r"\end{document}"

    # Aquí vamos a ir guardando el contenido para todos los estudiantes
    cuerpo_total = ""

    for index, row in df.iterrows():
        nombre_estudiante = str(row['Nombre']).strip()
        if not nombre_estudiante:
            continue

        datos = {
            "estudiante": nombre_estudiante,
            "e1_monto": formato_monto(random.randint(22000, 26000)),
            "e1_tasa": round(random.uniform(2.5, 3.5), 1),
            "e2_monto": formato_monto(random.randint(14000, 17000)),
            "e2_tasa": round(random.uniform(3.0, 4.0), 1),
            "e3_deuda1": formato_monto(random.randint(6000, 8000)),
            "e3_deuda2": formato_monto(random.randint(9000, 11000)),
            "e3_abono": formato_monto(random.randint(3000, 5000)),
            "e3_tasa": round(random.uniform(25, 35), 1),
            "e4_deposito": formato_monto(random.randint(140000, 160000)).replace(",", "."),
            "e4_tasa": round(random.uniform(14, 18), 1),
            "e5_capital": formato_monto(random.randint(30000, 35000)),
            "e5_tasa": round(random.uniform(4.0, 5.5), 1),
            "e6_capital": formato_monto(random.randint(60000, 70000)),
            "e6_tasa": round(random.uniform(2.0, 2.5), 1)
        }

        contenido = template.render(**datos)
        cuerpo_total += contenido + "\n\\newpage\n"  # Página nueva entre exámenes

    # Guardar el archivo tex completo
    with open(archivo_tex_unico, "w", encoding="utf-8") as f:
        f.write(preambulo)
        f.write(cuerpo_total)
        f.write(cierre)

    # Compilar el archivo tex completo
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", os.path.basename(archivo_tex_unico)],
            cwd=output_folder,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        messagebox.showinfo("Finalizado", f"Se generó el PDF con todos los exámenes en '{output_folder}'")
        # Abrir PDF automáticamente
        pdf_path = archivo_tex_unico.replace(".tex", ".pdf")
        abrir_pdf(pdf_path)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "No se pudo compilar el PDF final")

def abrir_pdf(ruta_pdf):
    import platform
    import subprocess
    import os
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(ruta_pdf)
        elif sistema == "Darwin":
            subprocess.run(["open", ruta_pdf])
        else:
            subprocess.run(["xdg-open", ruta_pdf])
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")

def seleccionar_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx *.xls")]
    )
    if ruta:
        generar_examen_unico(ruta)

def main():
    root = tk.Tk()
    root.title("Generador de Examen Único")
    root.geometry("400x150")
    root.resizable(False, False)

    label = tk.Label(root, text="Seleccione el archivo Excel con la lista de estudiantes", wraplength=350)
    label.pack(pady=20)

    btn = tk.Button(root, text="Cargar Excel y Generar PDF Único", command=seleccionar_archivo)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
