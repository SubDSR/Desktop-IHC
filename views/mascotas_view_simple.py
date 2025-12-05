"""
Vista de mascotas - Versión Simplificada y FUNCIONAL
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.mock_data import MASCOTAS, CLIENTES, get_cliente_by_id, get_nombre_completo_cliente
from views.components.data_table import DataTable
from utils.animations import NotificationManager
from utils.event_manager import AppContext, AppEvents


class MascotaFormDialog(ctk.CTkToplevel):
    """Formulario simplificado de mascota"""
    
    def __init__(self, parent, mode, mascota, theme, event_manager):
        super().__init__(parent)
        
        self.mode = mode
        self.mascota = mascota
        self.theme = theme
        self.event_manager = event_manager
        self.result = None
        
        self.title({
            'add': '➕ Nueva Mascota',
            'edit': '✏️ Editar Mascota',
            'view': '👁️ Ver Mascota'
        }[mode])
        
        self.geometry("550x650")
        self.transient(parent)
        self.grab_set()
        
        # Centrar
        x = (self.winfo_screenwidth() // 2) - (275)
        y = (self.winfo_screenheight() // 2) - (325)
        self.geometry(f'550x650+{x}+{y}')
        
        self._create_widgets()
        
        if mode in ['edit', 'view'] and mascota:
            self._populate_data()
        
        if mode == 'view':
            self._disable_fields()
    
    def _create_widgets(self):
        """Crear widgets"""
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_frame = ctk.CTkFrame(main, fg_color=self.theme.PRIMARY)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text={'add': '➕ NUEVA MASCOTA', 'edit': '✏️ EDITAR MASCOTA', 'view': '👁️ VER MASCOTA'}[self.mode],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Formulario
        form = ctk.CTkScrollableFrame(main)
        form.pack(fill="both", expand=True)
        
        # Nombre
        ctk.CTkLabel(form, text="Nombre (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.nombre_entry = ctk.CTkEntry(form, height=40)
        self.nombre_entry.pack(fill="x", pady=(0, 10))
        
        # Especie
        ctk.CTkLabel(form, text="Especie (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.especie_combo = ctk.CTkComboBox(form, values=["Perro", "Gato", "Ave", "Conejo", "Otro"], state="readonly", height=40)
        self.especie_combo.set("Perro")
        self.especie_combo.pack(fill="x", pady=(0, 10))
        
        # Raza
        ctk.CTkLabel(form, text="Raza (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.raza_entry = ctk.CTkEntry(form, height=40)
        self.raza_entry.pack(fill="x", pady=(0, 10))
        
        # Sexo
        ctk.CTkLabel(form, text="Sexo (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.sexo_combo = ctk.CTkComboBox(form, values=["Macho", "Hembra"], state="readonly", height=40)
        self.sexo_combo.set("Macho")
        self.sexo_combo.pack(fill="x", pady=(0, 10))
        
        # Color
        ctk.CTkLabel(form, text="Color (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.color_entry = ctk.CTkEntry(form, height=40)
        self.color_entry.pack(fill="x", pady=(0, 10))
        
        # Edad
        edad_frame = ctk.CTkFrame(form, fg_color="transparent")
        edad_frame.pack(fill="x", pady=(5, 10))
        
        edad_left = ctk.CTkFrame(edad_frame, fg_color="transparent")
        edad_left.pack(side="left", fill="both", expand=True, padx=(0, 5))
        ctk.CTkLabel(edad_left, text="Edad (años) (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x")
        self.edad_años_entry = ctk.CTkEntry(edad_left, height=40)
        self.edad_años_entry.pack(fill="x")
        
        edad_right = ctk.CTkFrame(edad_frame, fg_color="transparent")
        edad_right.pack(side="right", fill="both", expand=True, padx=(5, 0))
        ctk.CTkLabel(edad_right, text="Meses", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x")
        self.edad_meses_entry = ctk.CTkEntry(edad_right, height=40)
        self.edad_meses_entry.insert(0, "0")
        self.edad_meses_entry.pack(fill="x")
        
        # Peso
        ctk.CTkLabel(form, text="Peso (kg) (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.peso_entry = ctk.CTkEntry(form, height=40)
        self.peso_entry.pack(fill="x", pady=(0, 10))
        
        # Cliente
        ctk.CTkLabel(form, text="Dueño (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        clientes_activos = [c for c in CLIENTES if c['estado'] == 'Activo']
        opciones = [f"{c['nombres']} {c['apellidos']} ({c['dni']})" for c in clientes_activos]
        self.cliente_combo = ctk.CTkComboBox(form, values=opciones, state="readonly", height=40)
        if opciones:
            self.cliente_combo.set(opciones[0])
        self.cliente_combo.pack(fill="x", pady=(0, 10))
        
        # Estado
        ctk.CTkLabel(form, text="Estado", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.estado_combo = ctk.CTkComboBox(form, values=["Activo", "Inactivo"], state="readonly", height=40)
        self.estado_combo.set("Activo")
        self.estado_combo.pack(fill="x", pady=(0, 10))
        
        # Botones
        if self.mode != 'view':
            btn_frame = ctk.CTkFrame(main)
            btn_frame.pack(fill="x", pady=(15, 0))
            
            ctk.CTkButton(btn_frame, text="❌ Cancelar", command=self.destroy, fg_color="#6b7280", hover_color="#4b5563", width=130).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="💾 Guardar", command=self._save, fg_color=self.theme.PRIMARY, hover_color=self.theme.PRIMARY_DARK, width=130).pack(side="right", padx=5)
        else:
            ctk.CTkButton(main, text="✓ Cerrar", command=self.destroy, fg_color=self.theme.PRIMARY, width=130).pack(pady=(15, 0))
    
    def _populate_data(self):
        """Rellenar con datos"""
        if self.mascota:
            self.nombre_entry.insert(0, self.mascota.get('nombre_mascota', ''))
            self.especie_combo.set(self.mascota.get('especie', 'Perro'))
            self.raza_entry.insert(0, self.mascota.get('raza', ''))
            self.sexo_combo.set(self.mascota.get('sexo', 'Macho'))
            self.color_entry.insert(0, self.mascota.get('color_pelaje', ''))
            self.edad_años_entry.insert(0, str(self.mascota.get('edad_años', 0)))
            self.edad_meses_entry.delete(0, 'end')
            self.edad_meses_entry.insert(0, str(self.mascota.get('edad_meses', 0)))
            self.peso_entry.insert(0, str(self.mascota.get('peso_kg', '')))
            self.estado_combo.set(self.mascota.get('estado', 'Activo'))
            
            # Seleccionar cliente
            cliente = get_cliente_by_id(self.mascota.get('id_cliente'))
            if cliente:
                valor = f"{cliente['nombres']} {cliente['apellidos']} ({cliente['dni']})"
                self.cliente_combo.set(valor)
    
    def _disable_fields(self):
        """Deshabilitar campos"""
        for widget in [self.nombre_entry, self.raza_entry, self.color_entry, self.edad_años_entry, self.edad_meses_entry, self.peso_entry]:
            widget.configure(state="disabled")
        for combo in [self.especie_combo, self.sexo_combo, self.cliente_combo, self.estado_combo]:
            combo.configure(state="disabled")
    
    def _save(self):
        """Guardar mascota"""
        # Validar campos básicos
        if not self.nombre_entry.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        if not self.raza_entry.get().strip():
            messagebox.showerror("Error", "La raza es obligatoria")
            return
        if not self.color_entry.get().strip():
            messagebox.showerror("Error", "El color es obligatorio")
            return
        
        try:
            edad_años = int(self.edad_años_entry.get())
            edad_meses = int(self.edad_meses_entry.get() or 0)
            peso = float(self.peso_entry.get())
        except:
            messagebox.showerror("Error", "Edad y peso deben ser números válidos")
            return
        
        # Obtener ID del cliente seleccionado
        cliente_str = self.cliente_combo.get()
        dni = cliente_str.split('(')[-1].replace(')', '')
        cliente = next((c for c in CLIENTES if c['dni'] == dni), None)
        
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        # Crear resultado
        self.result = {
            'nombre_mascota': self.nombre_entry.get().strip(),
            'especie': self.especie_combo.get(),
            'raza': self.raza_entry.get().strip(),
            'sexo': self.sexo_combo.get(),
            'color_pelaje': self.color_entry.get().strip(),
            'edad_años': edad_años,
            'edad_meses': edad_meses,
            'peso_kg': peso,
            'id_cliente': cliente['id'],
            'estado': self.estado_combo.get()
        }
        
        if self.mode == 'add':
            self.result['id_mascota'] = max([m.get('id_mascota', 0) for m in MASCOTAS] + [0]) + 1
            self.event_manager.emit(AppEvents.MASCOTA_ADDED, {'mascota': self.result})
            NotificationManager.show_success(self.master, "✓ Mascota agregada")
        else:
            self.result['id_mascota'] = self.mascota['id_mascota']
            self.event_manager.emit(AppEvents.MASCOTA_UPDATED, {'mascota': self.result})
            NotificationManager.show_success(self.master, "✓ Mascota actualizada")
        
        self.destroy()


class MascotasViewSimple(ctk.CTkScrollableFrame):
    """Vista simplificada de mascotas"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.theme.COLORS["bg"])
        self.app = app
        self.theme = app.theme
        self.mascotas = MASCOTAS.copy()
        self.filtered_mascotas = self.mascotas.copy()
        
        # Contexto
        self.context = AppContext()
        self.event_manager = self.context.event_manager
        
        # Suscribirse
        self.event_manager.subscribe(AppEvents.MASCOTA_ADDED, self._on_mascota_added)
        self.event_manager.subscribe(AppEvents.MASCOTA_UPDATED, self._on_mascota_updated)
        self.event_manager.subscribe(AppEvents.MASCOTA_DELETED, self._on_mascota_deleted)
        
        self._create_widgets()
        self._update_table()
    
    def _on_mascota_added(self, event):
        mascota = event.data.get('mascota')
        if mascota:
            self.mascotas.append(mascota)
            self._apply_filters()
    
    def _on_mascota_updated(self, event):
        mascota = event.data.get('mascota')
        if mascota:
            for i, m in enumerate(self.mascotas):
                if m['id_mascota'] == mascota['id_mascota']:
                    self.mascotas[i].update(mascota)
                    break
            self._apply_filters()
    
    def _on_mascota_deleted(self, event):
        mascota_id = event.data.get('mascota_id')
        if mascota_id:
            self.mascotas = [m for m in self.mascotas if m['id_mascota'] != mascota_id]
            self._apply_filters()
    
    def _create_widgets(self):
        """Crear interfaz"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(header, text="GESTIÓN DE MASCOTAS 🐾", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.theme.PRIMARY)
        title.pack(side="left")
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="🔄", command=self._refresh, width=50, fg_color=self.theme.ACCENT, hover_color="#6d28d9").pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="➕ Nueva Mascota", command=self._add_mascota, fg_color="#10b981", hover_color="#059669", width=160).pack(side="right", padx=5)
        
        # Búsqueda
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Buscar por nombre...", height=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self._apply_filters())
        
        self.filter_combo = ctk.CTkComboBox(search_frame, values=["Todas las especies", "Perro", "Gato", "Ave", "Conejo", "Otro"], command=lambda v: self._apply_filters(), width=200)
        self.filter_combo.set("Todas las especies")
        self.filter_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(search_frame, text="🗑️ Limpiar", command=self._clear_filters, fg_color="#6b7280", hover_color="#4b5563", width=100).pack(side="left", padx=5)
        
        # Contenedor tabla
        self.table_container = ctk.CTkFrame(self, fg_color=self.theme.COLORS["surface"])
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Contador
        self.count_label = ctk.CTkLabel(self.table_container, text="", font=ctk.CTkFont(size=12), text_color=self.theme.TEXT_SECONDARY)
        self.count_label.pack(pady=10)
    
    def _update_table(self):
        """Actualizar tabla"""
        # Limpiar tabla anterior
        for widget in self.table_container.winfo_children():
            if isinstance(widget, DataTable):
                widget.destroy()
        
        self.count_label.pack(pady=10)
        self.count_label.configure(text=f"Mostrando {len(self.filtered_mascotas)} de {len(self.mascotas)} mascotas")
        
        # Crear tabla
        columns = ["N°", "Nombre", "Especie", "Raza", "Sexo", "Edad", "Peso (kg)", "Dueño", "Estado", "Acciones"]
        
        self.table = DataTable(
            self.table_container,
            columns=columns,
            theme=self.theme,
            height=400
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Poblar datos
        for idx, mascota in enumerate(self.filtered_mascotas, 1):
            cliente = get_cliente_by_id(mascota['id_cliente'])
            cliente_nombre = get_nombre_completo_cliente(mascota['id_cliente']) if cliente else "N/A"
            edad_str = f"{mascota['edad_años']}a {mascota['edad_meses']}m"
            
            row_data = [
                str(idx),
                mascota['nombre_mascota'],
                mascota['especie'],
                mascota['raza'],
                mascota['sexo'],
                edad_str,
                f"{mascota['peso_kg']} kg",
                cliente_nombre,
                mascota['estado']
            ]
            
            actions = [
                ("👁️", lambda m=mascota: self._view_mascota(m), self.theme.INFO),
                ("✏️", lambda m=mascota: self._edit_mascota(m), self.theme.ACCENT),
                ("🗑️", lambda m=mascota: self._delete_mascota(m), self.theme.DANGER)
            ]
            
            self.table.add_row(row_data, actions)
    
    def _apply_filters(self):
        """Aplicar filtros"""
        search = self.search_entry.get().lower()
        especie = self.filter_combo.get()
        
        self.filtered_mascotas = [
            m for m in self.mascotas
            if (search in m['nombre_mascota'].lower() or search in m['raza'].lower())
            and (especie == "Todas las especies" or m['especie'] == especie)
        ]
        
        self._update_table()
    
    def _clear_filters(self):
        """Limpiar filtros"""
        self.search_entry.delete(0, 'end')
        self.filter_combo.set("Todas las especies")
        self._apply_filters()
    
    def _refresh(self):
        """Refrescar"""
        self.filtered_mascotas = self.mascotas.copy()
        self._update_table()
        NotificationManager.show_success(self, "✓ Datos actualizados")
    
    def _add_mascota(self):
        """Agregar mascota"""
        dialog = MascotaFormDialog(self, 'add', None, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _view_mascota(self, mascota):
        """Ver mascota"""
        dialog = MascotaFormDialog(self, 'view', mascota, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _edit_mascota(self, mascota):
        """Editar mascota"""
        dialog = MascotaFormDialog(self, 'edit', mascota, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _delete_mascota(self, mascota):
        """Eliminar mascota"""
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {mascota['nombre_mascota']}?"):
            self.event_manager.emit(AppEvents.MASCOTA_DELETED, {'mascota_id': mascota['id_mascota']})
            NotificationManager.show_success(self, "✓ Mascota eliminada")
