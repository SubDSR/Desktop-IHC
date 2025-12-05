"""
Vista de veterinarios
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.mock_data import VETERINARIOS
from views.components.data_table import DataTable


class VeterinariosView(ctk.CTkScrollableFrame):
    """Vista para visualizar veterinarios"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.theme.COLORS["bg"])
        self.app = app
        self.theme = app.theme
        self.veterinarios = VETERINARIOS.copy()
        self.filtered_veterinarios = self.veterinarios.copy()
        
        self._create_widgets()
        self._update_table()
        
    def _create_widgets(self):
        """Crear los widgets de la vista"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        # Título
        ctk.CTkLabel(
            header,
            text="VETERINARIOS 👨‍⚕️",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.theme.COLORS["text"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Lista de veterinarios disponibles en la clínica",
            font=ctk.CTkFont(size=13),
            text_color=self.theme.COLORS["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        
        # Filtros
        filters_frame = ctk.CTkFrame(self, fg_color=self.theme.COLORS["bg_card"], corner_radius=15)
        filters_frame.pack(fill="x", padx=30, pady=(20, 20))
        
        filters_content = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_content.pack(fill="x", padx=20, pady=15)
        filters_content.grid_columnconfigure(0, weight=1)
        
        # Búsqueda
        search_frame = ctk.CTkFrame(filters_content, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self._apply_filters())
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar por nombre o especialidad...",
            height=40,
            font=ctk.CTkFont(size=13),
            textvariable=self.search_var
        )
        self.search_entry.pack(fill="x")
        
        # Filtro de estado
        estado_frame = ctk.CTkFrame(filters_content, fg_color="transparent")
        estado_frame.grid(row=0, column=1, padx=(0, 10))
        
        self.estado_var = ctk.StringVar(value="todos")
        estado_menu = ctk.CTkOptionMenu(
            estado_frame,
            values=["Todos los estados", "Activo", "Inactivo"],
            variable=self.estado_var,
            height=40,
            font=ctk.CTkFont(size=13),
            command=lambda x: self._apply_filters()
        )
        estado_menu.pack()
        
        # Botón limpiar filtros
        ctk.CTkButton(
            filters_content,
            text="Limpiar filtros",
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=self.theme.COLORS["text_secondary"],
            hover_color=self.theme.COLORS["border_dark"],
            command=self._clear_filters
        ).grid(row=0, column=2)
        
        # Tabla
        table_frame = ctk.CTkFrame(self, fg_color=self.theme.COLORS["bg_card"], corner_radius=15)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Título de la tabla
        table_header = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            table_header,
            text="LISTA DE VETERINARIOS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme.COLORS["text"]
        ).pack(side="left")
        
        self.results_label = ctk.CTkLabel(
            table_header,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=self.theme.COLORS["text_secondary"]
        )
        self.results_label.pack(side="right")
        
        # Contenedor de la tabla
        self.table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
    def _update_table(self):
        """Actualizar la tabla de veterinarios"""
        # Limpiar tabla anterior
        for widget in self.table_container.winfo_children():
            widget.destroy()
            
        # Definir columnas
        columns = ["N°", "DNI", "Nombre Completo", "Especialidad", "Colegiatura", "Teléfono", "Email", "Estado", "Acciones"]
        
        # Crear tabla
        self.table = DataTable(
            self.table_container,
            columns=columns,
            theme=self.theme,
            height=400
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Agregar filas
        for idx, vet in enumerate(self.filtered_veterinarios, 1):
            nombre_completo = f"{vet['nombres']} {vet['apellidos']}"
            
            row_data = [
                str(idx),
                vet.get('dni', 'N/A'),
                nombre_completo,
                vet['especialidad'],
                vet.get('num_colegiatura', 'N/A'),
                vet.get('telefono', 'N/A'),
                vet.get('email', 'N/A'),
                vet['estado']
            ]
            
            actions = [
                ("👁️", lambda v=vet: self._view_veterinario(v), self.theme.INFO)
            ]
            
            self.table.add_row(row_data, actions)
        
        # Actualizar etiqueta de resultados
        self._update_results_label()
        
    def _update_results_label(self):
        """Actualizar etiqueta de resultados"""
        total = len(self.veterinarios)
        filtered = len(self.filtered_veterinarios)
        
        if filtered < total:
            self.results_label.configure(text=f"Mostrando {filtered} de {total} veterinarios")
        else:
            self.results_label.configure(text=f"Total: {total} veterinarios")
            
    def _apply_filters(self):
        """Aplicar filtros a la lista de veterinarios"""
        search = self.search_var.get().lower()
        estado = self.estado_var.get()
        
        self.filtered_veterinarios = self.veterinarios.copy()
        
        # Filtro de búsqueda
        if search:
            self.filtered_veterinarios = [
                v for v in self.filtered_veterinarios
                if search in v['nombres'].lower() or
                   search in v['apellidos'].lower() or
                   search in v['especialidad'].lower()
            ]
            
        # Filtro de estado
        if estado in ["Activo", "Inactivo"]:
            self.filtered_veterinarios = [v for v in self.filtered_veterinarios if v['estado'] == estado]
            
        self._update_table()
        
    def _clear_filters(self):
        """Limpiar todos los filtros"""
        self.search_var.set("")
        self.estado_var.set("Todos los estados")
        self._apply_filters()
        
    def _view_veterinario(self, vet):
        """Ver detalles del veterinario"""
        nombre_completo = f"{vet['nombres']} {vet['apellidos']}"
        
        info = f"""
INFORMACIÓN DEL VETERINARIO

Nombre: {nombre_completo}
DNI: {vet.get('dni', 'N/A')}
Especialidad: {vet['especialidad']}
Colegiatura: {vet.get('num_colegiatura', 'N/A')}

CONTACTO
Teléfono: {vet.get('telefono', 'N/A')}
Email: {vet.get('email', 'N/A')}

ESTADO
{vet['estado']}
"""
        messagebox.showinfo("Detalles del Veterinario", info)
