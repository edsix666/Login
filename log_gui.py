import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login de Usuarios")
        self.root.geometry("400x300")

        self.conn = sqlite3.connect("usuarios.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            username TEXT PRIMARY KEY, 
                            nombre TEXT, 
                            apellido TEXT, 
                            telefono TEXT, 
                            correo TEXT, 
                            password TEXT, 
                            confirm_password TEXT)''')

        self.conn.commit()

        self.username_label = tk.Label(root, text="Usuario:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Contraseña:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.login_button.pack()
        self.registrar_button = tk.Button(root, text="Registrar Usuario", command=self.registrar_usuario)
        self.registrar_button.pack()

        self.tree = None
    
    def registrar_usuario(self):
        ventana_registro = tk.Toplevel(self.root)
        ventana_registro.title("Registrar Usuario")

        username_label = tk.Label(ventana_registro, text="Usuario:")
        username_label.pack()
        username_entry = tk.Entry(ventana_registro)
        username_entry.pack()

        nombre_label = tk.Label(ventana_registro, text="Nombre:")
        nombre_label.pack()
        nombre_entry = tk.Entry(ventana_registro)
        nombre_entry.pack()

        apellido_label = tk.Label(ventana_registro, text="Apellido:")
        apellido_label.pack()
        apellido_entry = tk.Entry(ventana_registro)
        apellido_entry.pack()

        telefono_label = tk.Label(ventana_registro, text="Teléfono:")
        telefono_label.pack()
        telefono_entry = tk.Entry(ventana_registro)
        telefono_entry.pack()

        correo_label = tk.Label(ventana_registro, text="Correo:")
        correo_label.pack()
        correo_entry = tk.Entry(ventana_registro)
        correo_entry.pack()

        password_label = tk.Label(ventana_registro, text="Contraseña:")
        password_label.pack()
        password_entry = tk.Entry(ventana_registro, show="*")
        password_entry.pack()

        confirm_password_label = tk.Label(ventana_registro, text="Confirmar Contraseña:")
        confirm_password_label.pack()
        confirm_password_entry = tk.Entry(ventana_registro, show="*")
        confirm_password_entry.pack()

        confirmar_button = tk.Button(ventana_registro, text="Registrar", command=lambda: self.registrar(username_entry.get(), nombre_entry.get(), apellido_entry.get(), telefono_entry.get(), correo_entry.get(), password_entry.get(), confirm_password_entry.get()))
        confirmar_button.pack()

    def iniciar_sesion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Debe ingresar su usuario y contraseña")
            return

        self.c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
        resultado = self.c.fetchone()

        if resultado:
            self.root.withdraw()
            self.mostrar_usuarios()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def mostrar_usuarios(self):
        ventana_principal = tk.Toplevel(self.root)
        ventana_principal.title("Lista de Usuarios")

        tree = ttk.Treeview(ventana_principal, columns=("nombre", "apellido", "telefono", "correo"))
        tree.heading("#0", text="Usuario")
        tree.heading("nombre", text="Nombre")
        tree.heading("apellido", text="Apellido")
        tree.heading("telefono", text="Teléfono")
        tree.heading("correo", text="Correo")

        self.c.execute("SELECT * FROM usuarios")
        usuarios = self.c.fetchall()
        for usuario in usuarios:
            tree.insert("", tk.END, text=usuario[0], values=(usuario[1], usuario[2], usuario[3], usuario[4]))

        tree.pack()

        botones_frame = tk.Frame(ventana_principal)
        botones_frame.pack()

        nuevo_button = tk.Button(botones_frame, text="Nuevo", command=self.registrar_usuario)
        nuevo_button.pack(side=tk.LEFT)

        actualizar_button = tk.Button(botones_frame, text="Actualizar", command=self.actualizar_usuario)
        actualizar_button.pack(side=tk.LEFT)

        eliminar_button = tk.Button(botones_frame, text="Eliminar", command=self.eliminar_usuario)
        eliminar_button.pack(side=tk.LEFT)

        cerrar_sesion_button = tk.Button(botones_frame, text="Cerrar Sesión", command=self.cerrar_sesion)
        cerrar_sesion_button.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(ventana_principal, columns=("nombre", "apellido", "telefono", "correo"))

    def registrar(self, username, nombre, apellido, telefono, correo, password, confirm_password):
        if not all([username, nombre, apellido, telefono, correo, password, confirm_password]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        if len(password) > 8 or len(confirm_password) > 8:
            messagebox.showerror("Error", "La contraseña debe tener máximo 8 caracteres")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        try:
            self.c.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?, ?)", (username, nombre, apellido, telefono, correo, password, confirm_password))
            self.conn.commit()
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe en la base de datos")

    def actualizar_usuario(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario para actualizar")
            return

        ventana_actualizar = tk.Toplevel(self.root)
        ventana_actualizar.title("Actualizar Usuario")

        usuario_seleccionado = self.tree.item(seleccion[0])
        username = usuario_seleccionado["text"]

        self.c.execute("SELECT * FROM usuarios WHERE username=?", (username,))
        usuario = self.c.fetchone()

        nombre_label = tk.Label(ventana_actualizar, text="Nombre:")
        nombre_label.pack()
        nuevo_nombre_entry = tk.Entry(ventana_actualizar)
        nuevo_nombre_entry.pack()
        nuevo_nombre_entry.insert(0, usuario[1])

        apellido_label = tk.Label(ventana_actualizar, text="Apellido:")
        apellido_label.pack()
        nuevo_apellido_entry = tk.Entry(ventana_actualizar)
        nuevo_apellido_entry.pack()
        nuevo_apellido_entry.insert(0, usuario[2])

        telefono_label = tk.Label(ventana_actualizar, text="Teléfono:")
        telefono_label.pack()
        nuevo_telefono_entry = tk.Entry(ventana_actualizar)
        nuevo_telefono_entry.pack()
        nuevo_telefono_entry.insert(0, usuario[3])

        correo_label = tk.Label(ventana_actualizar, text="Correo:")
        correo_label.pack()
        nuevo_correo_entry = tk.Entry(ventana_actualizar)
        nuevo_correo_entry.pack()
        nuevo_correo_entry.insert(0, usuario[4])

        confirmar_button = tk.Button(ventana_actualizar, text="Actualizar", command=lambda: self.actualizar(username, nuevo_nombre_entry.get(), nuevo_apellido_entry.get(), nuevo_telefono_entry.get(), nuevo_correo_entry.get()))
        confirmar_button.pack()

    def eliminar_usuario(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este usuario?")
        if respuesta:
            usuario_seleccionado = self.tree.item(seleccion[0])
            username = usuario_seleccionado["text"]

            try:
                self.c.execute("DELETE FROM usuarios WHERE username=?", (username,))
                self.conn.commit()
                messagebox.showinfo("Eliminación exitosa", "Usuario eliminado correctamente")
                self.mostrar_usuarios()  # Actualizar la vista después de eliminar el usuario
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {str(e)}")

    def actualizar(self, username, nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_correo):
        if not all([nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_correo]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        try:
            self.c.execute("UPDATE usuarios SET nombre=?, apellido=?, telefono=?, correo=? WHERE username=?", (nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_correo, username))
            self.conn.commit()
            messagebox.showinfo("Actualización exitosa", "Usuario actualizado correctamente")
            self.mostrar_usuarios()  # Actualizar la vista después de actualizar el usuario
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {str(e)}")

    def cerrar_sesion(self):
        self.conn.close()
        self.root.destroy()

root = tk.Tk()
app = LoginApp(root)
root.mainloop()
