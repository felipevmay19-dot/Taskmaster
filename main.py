import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

class TaskMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster - Gestor de Tareas")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")
        
        # Cargar tareas
        self.tasks = self.load_tasks()
        
        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        
        # Título
        title = tk.Label(root, text="TaskMaster", font=("Helvetica", 24, "bold"), bg="#f0f4f8", fg="#2c3e50")
        title.pack(pady=20)
        
        # Frame para agregar tarea
        add_frame = tk.Frame(root, bg="#f0f4f8")
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="Nueva tarea:", font=("Helvetica", 12), bg="#f0f4f8").pack(side=tk.LEFT, padx=10)
        
        self.task_entry = tk.Entry(add_frame, width=50, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT, padx=10)
        
        add_button = ttk.Button(add_frame, text="Agregar", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=10)
        
        # Tabla de tareas
        self.tree = ttk.Treeview(root, columns=("Tarea", "Fecha", "Estado"), show="headings", height=15)
        
        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Fecha", text="Fecha de creación")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("Tarea", width=400)
        self.tree.column("Fecha", width=150)
        self.tree.column("Estado", width=150)
        
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Botones de acción
        action_frame = tk.Frame(root, bg="#f0f4f8")
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text="Marcar como Completada", command=self.mark_complete).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Eliminar tarea", command=self.delete_task).pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="Guardar y Salir", command=self.save_and_exit).pack(side=tk.LEFT, padx=10)
        
        # Actualizar la tabla al iniciar
        self.update_treeview()

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Advertencia", "La tarea no puede estar vacía")
            return

        new_task = {
            "tarea": task_text,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completada": False
        }
        self.tasks.append(new_task)
        self.task_entry.delete(0, tk.END)
        self.update_treeview()

    def update_treeview(self):
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Llenar la tabla
        for task in self.tasks:
            estado = "Completada" if task["completada"] else "Pendiente"
            tag = "completed" if task["completada"] else "pending"
            self.tree.insert("", tk.END, values=(task["tarea"], task["fecha"], estado), tags=(tag,))

        # Colores según estado
        self.tree.tag_configure("completed", foreground="green")
        self.tree.tag_configure("pending", foreground="black")

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una tarea")
            return

        index = self.tree.index(selected[0])
        self.tasks[index]["completada"] = True
        self.update_treeview()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una tarea")
            return

        index = self.tree.index(selected[0])
        del self.tasks[index]
        self.update_treeview()

    def save_and_exit(self):
        self.save_tasks()
        self.root.quit()

# ¡Aquí empieza el programa!
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMaster(root)
    root.mainloop()