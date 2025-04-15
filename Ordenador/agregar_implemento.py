import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import conexion

class AgregarImplemento:
    def __init__(self, contenedor):
        self.frame = tk.Frame(contenedor, bg="#D3D3D3")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        titulo = tk.Label(self.frame, text="Registro de Implemento", font=("Arial", 16, "bold"), 
                         fg="blue", bg="#D3D3D3")
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Formulario
        self.crear_formulario()

        # Botón de registro
        btn_registrar = tk.Button(self.frame, text="Registrar", command=self.registrar_implemento,
                                 bg="#007bff", fg="white", font=("Arial", 12))
        btn_registrar.grid(row=8, column=0, columnspan=2, pady=20)

        # Cargar opciones de combobox
        self.cargar_ubicaciones()
        self.cargar_unidades_medida()

    def crear_formulario(self):
        # Nombre del implemento
        tk.Label(self.frame, text="Nombre del implemento:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.nombre_implemento = tk.Entry(self.frame, font=("Arial", 10))
        self.nombre_implemento.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Stock
        tk.Label(self.frame, text="Stock:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.stock = tk.Entry(self.frame, font=("Arial", 10))
        self.stock.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # Stock mínimo
        tk.Label(self.frame, text="Stock mínimo:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.stock_minimo = tk.Entry(self.frame, font=("Arial", 10))
        self.stock_minimo.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        # Foto
        tk.Label(self.frame, text="Enlace a Foto del implemento:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.foto = tk.Entry(self.frame, font=("Arial", 10))
        self.foto.grid(row=4, column=1, sticky="ew", padx=10, pady=5)

        # Ubicación (Combobox)
        tk.Label(self.frame, text="Ubicación:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.ubicacion = ttk.Combobox(self.frame, font=("Arial", 10), state="readonly")
        self.ubicacion.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        # Unidad de medida (Combobox)
        tk.Label(self.frame, text="Unidad de Medida:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.unidad_medida = ttk.Combobox(self.frame, font=("Arial", 10), state="readonly")
        self.unidad_medida.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

        # Ficha técnica
        tk.Label(self.frame, text="Ficha técnica:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.ficha_tecnica = tk.Entry(self.frame, font=("Arial", 10))
        self.ficha_tecnica.grid(row=7, column=1, sticky="ew", padx=10, pady=5)

        # Guía de uso
        tk.Label(self.frame, text="Guía de Uso:", bg="#D3D3D3", 
                font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.guia_uso = tk.Entry(self.frame, font=("Arial", 10))
        self.guia_uso.grid(row=8, column=1, sticky="ew", padx=10, pady=5)

    def cargar_ubicaciones(self):
        try:
            mydb = conexion.conectar()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT id_ubicacion FROM ubicacion ORDER BY id_ubicacion ASC")
            ubicaciones = [str(row[0]) for row in mycursor.fetchall()]
            self.ubicacion['values'] = ubicaciones
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar ubicaciones: {err}")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                mycursor.close()
                mydb.close()

    def cargar_unidades_medida(self):
        try:
            mydb = conexion.conectar()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT id_medida, nombre_medida FROM unidad_medida ORDER BY id_medida ASC")
            unidades = [f"{row[0]} - {row[1]}" for row in mycursor.fetchall()]
            self.unidad_medida['values'] = unidades
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar unidades de medida: {err}")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                mycursor.close()
                mydb.close()

    def registrar_implemento(self):
        # Obtener valores del formulario
        nombre = self.nombre_implemento.get()
        stock = self.stock.get()
        stock_min = self.stock_minimo.get()
        foto = self.foto.get()
        ubicacion = self.ubicacion.get().split()[0]  # Obtener solo el ID
        unidad_medida = self.unidad_medida.get().split()[0]  # Obtener solo el ID
        ficha_tecnica = self.ficha_tecnica.get()
        guia_uso = self.guia_uso.get()

        # Validaciones básicas
        if not nombre:
            messagebox.showerror("Error", "El nombre del implemento es requerido")
            return

        try:
            mydb = conexion.conectar()
            mycursor = mydb.cursor()

            sql = """INSERT INTO implemento 
                    (nombre_implemento, stock_implemento, stock_minimo, ficha_tecnica, 
                     foto, guia_uso_lab, ubicacion_fk, und_medida_fk) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            valores = (
                nombre,
                int(stock) if stock else None,
                int(stock_min) if stock_min else None,
                ficha_tecnica if ficha_tecnica else None,
                foto if foto else None,
                guia_uso if guia_uso else None,
                ubicacion if ubicacion else None,
                int(unidad_medida) if unidad_medida else None
            )

            mycursor.execute(sql, valores)
            mydb.commit()

            messagebox.showinfo("Éxito", "Implemento registrado correctamente")
            self.limpiar_formulario()

        except mysql.connector.Error as err:
            mydb.rollback()
            messagebox.showerror("Error", f"Error al registrar implemento: {err}")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                mycursor.close()
                mydb.close()

    def limpiar_formulario(self):
        self.nombre_implemento.delete(0, tk.END)
        self.stock.delete(0, tk.END)
        self.stock_minimo.delete(0, tk.END)
        self.foto.delete(0, tk.END)
        self.ubicacion.set('')
        self.unidad_medida.set('')
        self.ficha_tecnica.delete(0, tk.END)
        self.guia_uso.delete(0, tk.END)