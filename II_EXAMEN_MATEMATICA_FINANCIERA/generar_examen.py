import pandas as pd
import random
import subprocess
from jinja2 import Environment, FileSystemLoader
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def formato_monto(valor):
    return "{:,.2f}".format(valor)

def escapar_latex(texto):
    if not isinstance(texto, str):
        texto = str(texto)
    caracteres = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    for c, r in caracteres.items():
        texto = texto.replace(c, r)
    return texto

def generar_examen_unico(ruta_excel):
    try:
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

    output_folder = 'examenes_unicos'
    os.makedirs(output_folder, exist_ok=True)
    archivo_tex_unico = os.path.join(output_folder, 'examen_completo.tex')

    preambulo = r"""
\documentclass[10pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{lmodern}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage{textcomp}
\pagestyle{fancy}
\fancyhf{}
\lhead{UISIL \\ ISB-24 INGENIERÍA EN SISTEMAS}
\rhead{\today}
\renewcommand{\headrulewidth}{1pt}
\renewcommand{\footrulewidth}{0.5pt}
\lfoot{\textbf{Elaborado por: Francisco Campos S.}}
\cfoot{\thepage}
\setlength{\headheight}{22.5pt}
\begin{document}
"""

    cierre = r"\end{document}"

    cuerpo_total = ""

    nombres_personas = [
        "Carmen Rojas",
        "Eduardo Morales",
        "María Pérez",
        "Jorge Sánchez",
        "Ana Vargas"
    ]

    nombres_empresas = [
        "Servicios Globales",
        "Distribuidora Omega",
        "Comercial ABC",
        "Tecnologías Avanzadas",
        "Importadora Central"
    ]

    for index, row in df.iterrows():
        nombre_estudiante = str(row['Nombre']).strip()
        if not nombre_estudiante:
            continue

        datos = {
            "estudiante": escapar_latex(nombre_estudiante),
            "nombre_persona1": escapar_latex(random.choice(nombres_personas)),
            "nombre_persona2": escapar_latex(random.choice(nombres_personas)),
            "nombre_empresa1": escapar_latex(random.choice(nombres_empresas)),
            "nombre_empresa2": escapar_latex(random.choice(nombres_empresas)),
            "nombre_empresa3": escapar_latex(random.choice(nombres_empresas)),
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
        cuerpo_total += contenido + "\n\\newpage\n"

    with open(archivo_tex_unico, "w", encoding="utf-8") as f:
        f.write(preambulo)
        f.write(cuerpo_total)
        f.write(cierre)

    print(f"Archivo TEX creado en: {archivo_tex_unico}")
    print(f"Archivos en carpeta '{output_folder}': {os.listdir(output_folder)}")

    try:
        log_path = os.path.join(output_folder, "compile.log")
        with open(log_path, "w", encoding="utf-8") as log_file:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", os.path.basename(archivo_tex_unico)],
                cwd=output_folder,
                stdout=log_file,
                stderr=log_file,
                check=True
            )
        print(f"Compilación exitosa, log en: {log_path}")
        messagebox.showinfo("Finalizado", f"Se generó el PDF con todos los exámenes en '{output_folder}'")
        pdf_path = archivo_tex_unico.replace(".tex", ".pdf")
        abrir_pdf(pdf_path)

    except subprocess.CalledProcessError:
        print(f"Error de compilación. Revisa el log en {log_path}")
        messagebox.showerror("Error", f"No se pudo compilar el PDF final.\nRevisa el archivo de log:\n{log_path}")

def abrir_pdf(ruta_pdf):
    import platform
    import subprocess
    import os
    sistema = platform.system()
    try:
        print(f"Intentando abrir PDF en: {ruta_pdf}")
        if sistema == "Windows":
            os.startfile(ruta_pdf)
        elif sistema == "Darwin":
            subprocess.run(["open", ruta_pdf], check=True)
        else:
            subprocess.run(["xdg-open", ruta_pdf], check=True)
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