import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from fpdf import FPDF
import datetime

class InformeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SGI LAB MANAGER - Informes")
        self.root.geometry("1000x600")
        
        # Configuración de la base de datos
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sgi'
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Generar Informe", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Tipo de informe
        ttk.Label(main_frame, text="Tipo de informe:").grid(row=1, column=0, sticky=tk.W, pady=5)
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
            main_frame,
            textvariable=self.tipo_informe,
            values=[opt[0] for opt in informe_options],  # Mostramos solo el texto visible
            state="readonly"  # Para que solo se puedan seleccionar valores de la lista
        )
        self.combo_informe.grid(row=2, column=0, sticky=tk.W, pady=5)

        # Mapear el texto visible a los valores
        self.opciones_informe = {opt[0]: opt[1] for opt in informe_options}

        # Configurar evento de selección
        self.combo_informe.bind("<<ComboboxSelected>>", self.on_informe_selected)

        # Añadir este método a tu clase:
        
        # Entrada para datos específicos
        self.entrada_frame = ttk.Frame(main_frame)
        self.entrada_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Label(self.entrada_frame, text="Nombre:").pack(side=tk.LEFT)
        self.entrada_dato = ttk.Entry(self.entrada_frame, width=30)
        self.entrada_dato.pack(side=tk.LEFT, padx=5)
        self.entrada_frame.grid_remove()  # Ocultar inicialmente
        
        # Botón de generación
        ttk.Button(main_frame, text="Generar Informe", command=self.generar_informe).grid(row=7, column=0, pady=20, sticky=tk.W)
        ttk.Button(main_frame, text="Exportar a PDF", command=self.exportar_pdf).grid(row=7, column=1, pady=20, sticky=tk.E)
        
        # Tabla de resultados
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.grid(row=8, column=0, columnspan=2, sticky=tk.NSEW)
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar expansión de filas/columnas
        main_frame.grid_rowconfigure(8, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
    
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
    
    def conectar_db(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
            return None
    
    def busqueda_informes(self, busqueda, dato=""):
        conn = self.conectar_db()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            if busqueda == '1':  # Inventario
                query = "SELECT nombre_implemento as Nombre, stock_implemento as Stock, stock_minimo as 'Stock Minimo' FROM implemento"
                cursor.execute(query)
            elif busqueda == '2':  # Prácticas donde se usa determinado insumo
                query = """SELECT p.id_practica as 'Id Práctica', g.nombre_guia as 'Título'
                          FROM practica p
                          JOIN guia g ON p.guia_fk = g.id_guia
                          JOIN implemento i ON p.implemento_fk = i.id_implemento
                          WHERE i.nombre_implemento LIKE %s"""
                cursor.execute(query, (f"{dato}%",))
            elif busqueda == '3':  # Implementos de determinada guía
                query = """SELECT i.nombre_implemento as 'Nombre del implemento', ip.cantidad as 'Cantidad'
                          FROM implemento AS i
                          JOIN practica AS ip ON i.id_implemento = ip.implemento_fk 
                          JOIN guia AS g ON g.id_guia = ip.guia_fk
                          WHERE g.nombre_guia LIKE %s"""
                cursor.execute(query, (f"{dato}%",))
            elif busqueda == '4':  # Movimientos
                query = """SELECT id_transaccion as 'Id Prestamo', fecha_hora as 'Fecha y Hora', 
                           tipo_transaccion as 'Tipo', i.nombre_implemento as 'Nombre Implemento', 
                           cantidad as 'Cantidad', user_fk as 'Usuario Prestador', 
                           nombre_recibe as 'Usuario Recibe', prestamo_fk as 'Prestamo Asociado' 
                           FROM transaccion
                           JOIN implemento AS i ON transaccion.implemento_transa_fk = i.id_implemento"""
                cursor.execute(query)
            
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en la consulta: {err}")
            return None
        finally:
            cursor.close()
            conn.close()
    
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
    
    def exportar_pdf(self):
        try:
            tipo = self.tipo_informe.get()
            if not tipo:
                messagebox.showwarning("Advertencia", "Seleccione un tipo de informe")
                return
            
            dato = self.entrada_dato.get() if tipo in ("2", "3") else ""
            
            resultados = self.busqueda_informes(tipo, dato)
            if not resultados:
                messagebox.showinfo("Información", "No hay datos para exportar")
                return
            
            # Crear PDF con estilo similar al ejemplo
            pdf = FPDF()
            pdf.add_page()
            
            # Usar fuentes estándar para evitar advertencias
            pdf.set_font("helvetica", size=12)
            
            # Título centrado y en negrita
            pdf.set_font("helvetica", 'B', 16)
            pdf.cell(0, 10, text="Informe", new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.ln(10)
            
            # Volver a fuente normal
            pdf.set_font("helvetica", size=12)
            
            # Obtener columnas
            columnas = list(resultados[0].keys())
            
            # Calcular ancho de columnas
            col_widths = [80, 30, 30, 50] if len(columnas) == 4 else [190 / len(columnas)] * len(columnas)
            
            # Encabezados en negrita
            pdf.set_font("helvetica", 'B', 12)
            for i, col in enumerate(columnas):
                pdf.cell(col_widths[i], 10, text=col, border=0, align='L')
            pdf.ln()
            
            # Línea divisoria
            pdf.cell(0, 0, text="", border="T")
            pdf.ln(8)
            
            # Datos en fuente normal
            pdf.set_font("helvetica", size=12)
            for row in resultados:
                for i, col in enumerate(columnas):
                    # Manejar valores None
                    valor = row[col] if row[col] is not None else ""
                    align = 'R' if isinstance(valor, (int, float)) else 'L'
                    pdf.cell(col_widths[i], 10, text=str(valor), border=0, align=align)
                pdf.ln()
                
                # Manejar estado de stock de forma segura
                if tipo == '1' and 'Stock' in row and 'Stock Minimo' in row:
                    stock = row['Stock'] or 0
                    stock_min = row['Stock Minimo'] or 0
                    
                    pdf.set_font("helvetica", 'I', 10)
                    if stock_min is None:  # Si no hay stock mínimo definido
                        estado = "Stock OK"
                    elif stock < stock_min:
                        estado = "Bajo stock"
                    elif stock <= (stock_min + 2):
                        estado = "Stock crítico"
                    else:
                        estado = "En stock"
                    
                    pdf.cell(col_widths[-1], 10, text=estado, border=0, align='R')
                    pdf.ln()
                    pdf.set_font("helvetica", size=12)
            
            # Guardar PDF
            pdf.output("informe.pdf")
            messagebox.showinfo("Éxito", "Informe exportado como informe.pdf")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el PDF: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InformeApp(root)
    root.mainloop()