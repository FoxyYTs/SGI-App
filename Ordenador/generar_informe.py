import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from fpdf import FPDF
import datetime
import conexion

class GenerarInforme:
    def __init__(self, contenedor):
        self.frame = tk.Frame(contenedor, bg="gray")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        label_informe = tk.Label(self.frame, bg="#D3D3D3")
        label_informe.grid(row=0, column=0, padx=10, pady=10)

        # Título
        titulo = tk.Label(label_informe, text="Generar Informe", font=("Arial", 16, "bold"), fg="blue", bg="#D3D3D3")
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Formulario
        label_campos = tk.Label(label_informe, bg="#D3D3D3")
        label_campos.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Tipo de informe combobox
        tk.Label(label_campos, text="Tipo de informe:", bg="#D3D3D3").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.tipo_informe = tk.StringVar()

        # Opciones para el ComboBox (formato: [texto visible, valor asociado])
        informe_options = [
            ("Inventario", "1"),
            ("Prácticas por insumo", "2"),
            ("Implementos por guía", "3"),
            ("Movimientos", "4")
        ]

        # Crear el ComboBox
        self.combo_informe = ttk.Combobox(
            label_campos,
            textvariable=self.tipo_informe,
            values=[opt[0] for opt in informe_options],  # Mostramos solo el texto visible
            state="readonly"  # Para que solo se puedan seleccionar valores de la lista
        )
        self.combo_informe.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # Mapear el texto visible a los valores
        self.opciones_informe = {opt[0]: opt[1] for opt in informe_options}

        # Configurar evento de selección
        self.combo_informe.bind("<<ComboboxSelected>>", self.on_informe_selected)

        self.entrada_frame = ttk.Frame(label_campos)
        self.entrada_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Label(self.entrada_frame, text="Nombre:").pack(side=tk.LEFT)
        self.entrada_dato = ttk.Entry(self.entrada_frame, width=30)
        self.entrada_dato.pack(side=tk.LEFT, padx=5)
        self.entrada_frame.grid_remove()  # Ocultar inicialmente
        # Botón de registro
        btn_registrar = tk.Button(label_informe, text="Generar Informe", command=self.generar_informe, bg="#007bff", fg="white", font=("Arial", 12))
        btn_registrar.grid(row=2, column=0, columnspan=2, pady=20)

    def on_informe_selected(self, event=None):
        """Método que se ejecuta cuando se selecciona un informe del ComboBox"""
        texto_seleccionado = self.combo_informe.get()
        if texto_seleccionado in self.opciones_informe:
            self.tipo_informe.set(self.opciones_informe[texto_seleccionado])
            self.actualizar_entrada()

    def actualizar_entrada(self):
        tipo = self.tipo_informe.get()
        if tipo in ("2", "3"):
            self.entrada_frame.grid()
        else:
            self.entrada_frame.grid_remove()
    
    def generar_informe(self):
        tipo = self.tipo_informe.get()
        if not tipo:
            messagebox.showwarning("Advertencia", "Seleccione un tipo de informe")
            return
        
        dato = self.entrada_dato.get() if tipo in ("2", "3") else ""
        resultados = self.busqueda_informes(tipo, dato)
        if resultados is None:
            return
        
        # Configurar las columnas del Treeview
        self.tree.delete(*self.tree.get_children())
        
        if resultados:
            # Obtener nombres de columnas del primer resultado
            columnas = list(resultados[0].keys())
            self.tree["columns"] = columnas
            
            # Configurar encabezados
            for col in columnas:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor=tk.W)
            
            # Insertar datos
            for row in resultados:
                valores = [row[col] if row[col] is not None else "" for col in columnas]
                item = self.tree.insert("", tk.END, values=valores)
                
                # Resaltar filas para el informe de inventario
                if tipo == '1':
                    stock = row['Stock'] if row['Stock'] is not None else 0
                    stock_min = row['Stock Minimo'] if row['Stock Minimo'] is not None else 0
                    
                    # Solo aplicar colores si hay un stock mínimo definido
                    if stock_min > 0:  # Solo comparar si stock_min tiene un valor significativo
                        if stock < stock_min:
                            self.tree.tag_configure('bajo_stock', background='red', foreground='white')
                            self.tree.item(item, tags=('bajo_stock',))
                        elif stock <= (stock_min + 2):
                            self.tree.tag_configure('alerta_stock', background='yellow', foreground='black')
                            self.tree.item(item, tags=('alerta_stock',))
                    else:
                        # Opcional: mostrar un estado diferente cuando no hay stock mínimo definido
                        self.tree.tag_configure('sin_minimo', background='lightgray')
                        self.tree.item(item, tags=('sin_minimo',))
        else:
            messagebox.showinfo("Información", "No se encontraron resultados")