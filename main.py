"""
Sistema de Gestión Veterinaria - Módulo Recepcionista
Aplicación Desktop con CustomTkinter
"""

import customtkinter as ctk
from views.dashboard_view import DashboardView
from views.components.cliente_form_simple import ClienteFormDialog
from views.mascotas_view_simple import MascotasViewSimple
from views.citas_view_simple import CitasViewSimple
from views.veterinarios_view import VeterinariosView
from utils.theme import VeterinariaTheme
from utils.mock_data import CLIENTES
from views.components.data_table import DataTable
from utils.animations import NotificationManager
from utils.event_manager import AppContext, AppEvents

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class VeterinariaApp(ctk.CTk):
    """Aplicación principal del sistema veterinario"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Sistema Veterinaria - Recepcionista")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Centrar ventana
        self._center_window()
        
        # Variables
        self.current_view = None
        self.theme = VeterinariaTheme()
        
        # Crear interfaz
        self._create_widgets()
        
        # Mostrar vista inicial
        self.show_dashboard()
        
    def _center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = 1400
        height = 800
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def _create_widgets(self):
        """Crear los widgets principales"""
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Crear sidebar
        self._create_sidebar()
        
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self, fg_color=self.theme.COLORS["bg"])
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
    def _create_sidebar(self):
        """Crear barra lateral de navegación"""
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            fg_color=self.theme.COLORS["primary"],
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo y título
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="🏥 VETERINARIA",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Colitas Felices",
            font=ctk.CTkFont(size=14),
            text_color=self.theme.COLORS["text_light"]
        )
        subtitle_label.pack()
        
        # Información del usuario
        user_frame = ctk.CTkFrame(self.sidebar, fg_color=self.theme.COLORS["primary_dark"])
        user_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(
            user_frame,
            text="👤 RECEPCIONISTA",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        ).pack(pady=10)
        
        # Separador
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color=self.theme.COLORS["primary_dark"])
        separator.pack(fill="x", padx=20, pady=10)
        
        # Botones de navegación
        self.nav_buttons = {}
        
        nav_items = [
            ("🏠", "Inicio", "dashboard"),
            ("👥", "Clientes", "clientes"),
            ("🐾", "Mascotas", "mascotas"),
            ("📅", "Citas", "citas"),
            ("👨‍⚕️", "Veterinarios", "veterinarios"),
        ]
        
        for icon, text, view_name in nav_items:
            btn = self._create_nav_button(icon, text, view_name)
            self.nav_buttons[view_name] = btn
            
        # Espaciador
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(expand=True)
        
        # Botón de salir
        exit_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Salir",
            font=ctk.CTkFont(size=14),
            fg_color=self.theme.COLORS["danger"],
            hover_color=self.theme.COLORS["danger_hover"],
            height=45,
            command=self.quit
        )
        exit_btn.pack(pady=20, padx=20, fill="x")
        
    def _create_nav_button(self, icon, text, view_name):
        """Crear un botón de navegación"""
        btn = ctk.CTkButton(
            self.sidebar,
            text=f"{icon}  {text}",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=self.theme.COLORS["primary_dark"],
            anchor="w",
            height=45,
            command=lambda: self._on_nav_click(view_name)
        )
        btn.pack(pady=5, padx=20, fill="x")
        return btn
        
    def _on_nav_click(self, view_name):
        """Manejar clic en botón de navegación"""
        # Resetear colores de todos los botones
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.configure(fg_color=self.theme.COLORS["primary_dark"])
            else:
                btn.configure(fg_color="transparent")
        
        # Mostrar vista correspondiente
        if view_name == "dashboard":
            self.show_dashboard()
        elif view_name == "clientes":
            self.show_clientes()
        elif view_name == "mascotas":
            self.show_mascotas()
        elif view_name == "citas":
            self.show_citas()
        elif view_name == "veterinarios":
            self.show_veterinarios()
            
    def _clear_main_container(self):
        """Limpiar el contenedor principal"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
    def show_dashboard(self):
        """Mostrar vista de dashboard"""
        self._clear_main_container()
        self.current_view = DashboardView(self.main_container, self)
        self.current_view.pack(fill="both", expand=True)
        
    def show_clientes(self):
        """Mostrar vista de clientes"""
        self._clear_main_container()
        self.current_view = ClientesViewSimple(self.main_container, self)
        self.current_view.pack(fill="both", expand=True)
        
    def show_mascotas(self):
        """Mostrar vista de mascotas"""
        self._clear_main_container()
        self.current_view = MascotasViewSimple(self.main_container, self)
        self.current_view.pack(fill="both", expand=True)
        
    def show_citas(self):
        """Mostrar vista de citas"""
        self._clear_main_container()
        self.current_view = CitasViewSimple(self.main_container, self)
        self.current_view.pack(fill="both", expand=True)
        
    def show_veterinarios(self):
        """Mostrar vista de veterinarios"""
        self._clear_main_container()
        self.current_view = VeterinariosView(self.main_container, self)
        self.current_view.pack(fill="both", expand=True)


class ClientesViewSimple(ctk.CTkScrollableFrame):
    """Vista simplificada de clientes"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.theme.COLORS["bg"])
        self.app = app
        self.theme = app.theme
        self.clientes = CLIENTES.copy()
        self.filtered_clientes = self.clientes.copy()
        
        self.context = AppContext()
        self.event_manager = self.context.event_manager
        
        self.event_manager.subscribe(AppEvents.CLIENTE_ADDED, self._on_cliente_added)
        self.event_manager.subscribe(AppEvents.CLIENTE_UPDATED, self._on_cliente_updated)
        self.event_manager.subscribe(AppEvents.CLIENTE_DELETED, self._on_cliente_deleted)
        
        self._create_widgets()
        self._update_table()
    
    def _on_cliente_added(self, event):
        cliente = event.data.get('cliente')
        if cliente:
            cliente['id'] = max([c.get('id', 0) for c in self.clientes] + [0]) + 1
            self.clientes.append(cliente)
            self._apply_filters()
    
    def _on_cliente_updated(self, event):
        cliente = event.data.get('cliente')
        if cliente:
            for i, c in enumerate(self.clientes):
                if c['id'] == cliente['id']:
                    self.clientes[i].update(cliente)
                    break
            self._apply_filters()
    
    def _on_cliente_deleted(self, event):
        cliente_id = event.data.get('cliente_id')
        if cliente_id:
            self.clientes = [c for c in self.clientes if c['id'] != cliente_id]
            self._apply_filters()
    
    def _create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(header, text="GESTIÓN DE CLIENTES 👥", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.theme.PRIMARY)
        title.pack(side="left")
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="🔄", command=self._refresh, width=50, fg_color=self.theme.ACCENT, hover_color="#6d28d9").pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="➕ Nuevo Cliente", command=self._add_cliente, fg_color="#10b981", hover_color="#059669", width=160).pack(side="right", padx=5)
        
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Buscar por DNI o nombre...", height=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self._apply_filters())
        
        self.filter_combo = ctk.CTkComboBox(search_frame, values=["Todos", "Activos", "Inactivos"], command=lambda v: self._apply_filters(), width=150)
        self.filter_combo.set("Todos")
        self.filter_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(search_frame, text="🗑️ Limpiar", command=self._clear_filters, fg_color="#6b7280", hover_color="#4b5563", width=100).pack(side="left", padx=5)
        
        self.table_container = ctk.CTkFrame(self, fg_color=self.theme.COLORS["surface"])
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.count_label = ctk.CTkLabel(self.table_container, text="", font=ctk.CTkFont(size=12), text_color=self.theme.TEXT_SECONDARY)
        self.count_label.pack(pady=10)
    
    def _update_table(self):
        for widget in self.table_container.winfo_children():
            if isinstance(widget, DataTable):
                widget.destroy()
        
        self.count_label.pack(pady=10)
        self.count_label.configure(text=f"Mostrando {len(self.filtered_clientes)} de {len(self.clientes)} clientes")
        
        columns = ["N°", "DNI", "Nombres", "Apellidos", "Teléfono", "Email", "Estado", "Acciones"]
        
        self.table = DataTable(self.table_container, columns=columns, theme=self.theme, height=400)
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for idx, cliente in enumerate(self.filtered_clientes, 1):
            row_data = [
                str(idx),
                cliente['dni'],
                cliente['nombres'],
                cliente['apellidos'],
                cliente['telefono'],
                cliente.get('email', 'N/A'),
                cliente['estado']
            ]
            
            actions = [
                ("👁️", lambda c=cliente: self._view_cliente(c), self.theme.INFO),
                ("✏️", lambda c=cliente: self._edit_cliente(c), self.theme.ACCENT),
                ("🗑️", lambda c=cliente: self._delete_cliente(c), self.theme.DANGER)
            ]
            
            self.table.add_row(row_data, actions)
    
    def _apply_filters(self):
        search = self.search_entry.get().lower()
        estado_filter = self.filter_combo.get()
        
        self.filtered_clientes = [
            c for c in self.clientes
            if (search in c['dni'].lower() or search in c['nombres'].lower() or search in c['apellidos'].lower())
            and (estado_filter == "Todos" or (estado_filter == "Activos" and c['estado'] == "Activo") or (estado_filter == "Inactivos" and c['estado'] == "Inactivo"))
        ]
        
        self._update_table()
    
    def _clear_filters(self):
        self.search_entry.delete(0, 'end')
        self.filter_combo.set("Todos")
        self._apply_filters()
    
    def _refresh(self):
        self.filtered_clientes = self.clientes.copy()
        self._update_table()
        NotificationManager.show_success(self, "✓ Datos actualizados")
    
    def _add_cliente(self):
        dialog = ClienteFormDialog(self, 'add', None, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _view_cliente(self, cliente):
        dialog = ClienteFormDialog(self, 'view', cliente, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _edit_cliente(self, cliente):
        dialog = ClienteFormDialog(self, 'edit', cliente, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _delete_cliente(self, cliente):
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {cliente['nombres']} {cliente['apellidos']}?"):
            self.event_manager.emit(AppEvents.CLIENTE_DELETED, {'cliente_id': cliente['id']})
            NotificationManager.show_success(self, "✓ Cliente eliminado")


def main():
    """Función principal"""
    app = VeterinariaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
