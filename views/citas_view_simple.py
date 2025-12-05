"""
Vista de citas - Versión Simplificada con Drag & Drop FUNCIONAL
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from utils.mock_data import CITAS, MASCOTAS, VETERINARIOS, get_mascota_by_id, get_veterinario_by_id
from views.components.data_table import DataTable
from utils.animations import NotificationManager
from utils.event_manager import AppContext, AppEvents


class CitaFormDialog(ctk.CTkToplevel):
    """Formulario de cita"""
    
    def __init__(self, parent, mode, cita, theme, event_manager):
        super().__init__(parent)
        
        self.mode = mode
        self.cita = cita
        self.theme = theme
        self.event_manager = event_manager
        self.result = None
        
        self.title({
            'add': '➕ Nueva Cita',
            'edit': '✏️ Editar Cita',
            'view': '👁️ Ver Cita'
        }[mode])
        
        self.geometry("550x700")
        self.transient(parent)
        self.grab_set()
        
        x = (self.winfo_screenwidth() // 2) - (275)
        y = (self.winfo_screenheight() // 2) - (350)
        self.geometry(f'550x700+{x}+{y}')
        
        self._create_widgets()
        
        if mode in ['edit', 'view'] and cita:
            self._populate_data()
        
        if mode == 'view':
            self._disable_fields()
    
    def _create_widgets(self):
        """Crear widgets"""
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_frame = ctk.CTkFrame(main, fg_color=self.theme.ACCENT)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text={'add': '➕ NUEVA CITA', 'edit': '✏️ EDITAR CITA', 'view': '👁️ VER CITA'}[self.mode],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Formulario
        form = ctk.CTkScrollableFrame(main)
        form.pack(fill="both", expand=True)
        
        # Fecha
        fecha_frame = ctk.CTkFrame(form, fg_color="transparent")
        fecha_frame.pack(fill="x", pady=5)
        
        fecha_left = ctk.CTkFrame(fecha_frame, fg_color="transparent")
        fecha_left.pack(side="left", fill="both", expand=True, padx=(0, 5))
        ctk.CTkLabel(fecha_left, text="Fecha (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x")
        self.fecha_entry = ctk.CTkEntry(fecha_left, height=40, placeholder_text="YYYY-MM-DD")
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.fecha_entry.pack(fill="x")
        
        fecha_right = ctk.CTkFrame(fecha_frame, fg_color="transparent")
        fecha_right.pack(side="right", fill="both", expand=True, padx=(5, 0))
        ctk.CTkLabel(fecha_right, text="Hora (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x")
        self.hora_entry = ctk.CTkEntry(fecha_right, height=40, placeholder_text="HH:MM")
        self.hora_entry.insert(0, "09:00")
        self.hora_entry.pack(fill="x")
        
        # Mascota
        ctk.CTkLabel(form, text="Mascota (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(10, 2))
        mascotas_activas = [m for m in MASCOTAS if m['estado'] == 'Activo']
        opciones_mascotas = [f"{m['nombre_mascota']} - {m['especie']} ({m['id_mascota']})" for m in mascotas_activas]
        self.mascota_combo = ctk.CTkComboBox(form, values=opciones_mascotas, state="readonly", height=40)
        if opciones_mascotas:
            self.mascota_combo.set(opciones_mascotas[0])
        self.mascota_combo.pack(fill="x", pady=(0, 10))
        
        # Veterinario
        ctk.CTkLabel(form, text="Veterinario (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        vets_activos = [v for v in VETERINARIOS if v['estado'] == 'Activo']
        opciones_vets = [f"Dr(a). {v['nombres']} {v['apellidos']} - {v['especialidad']}" for v in vets_activos]
        self.veterinario_combo = ctk.CTkComboBox(form, values=opciones_vets, state="readonly", height=40)
        if opciones_vets:
            self.veterinario_combo.set(opciones_vets[0])
        self.veterinario_combo.pack(fill="x", pady=(0, 10))
        
        # Motivo
        ctk.CTkLabel(form, text="Motivo (*)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.motivo_entry = ctk.CTkEntry(form, height=40, placeholder_text="Ej: Consulta general, Vacunación...")
        self.motivo_entry.pack(fill="x", pady=(0, 10))
        
        # Observaciones
        ctk.CTkLabel(form, text="Observaciones", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.observaciones_text = ctk.CTkTextbox(form, height=100)
        self.observaciones_text.pack(fill="x", pady=(0, 10))
        
        # Estado
        ctk.CTkLabel(form, text="Estado", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", pady=(5, 2))
        self.estado_combo = ctk.CTkComboBox(form, values=["Programada", "Atendida", "Cancelada"], state="readonly", height=40)
        self.estado_combo.set("Programada")
        self.estado_combo.pack(fill="x", pady=(0, 10))
        
        # Botones
        if self.mode != 'view':
            btn_frame = ctk.CTkFrame(main)
            btn_frame.pack(fill="x", pady=(15, 0))
            
            ctk.CTkButton(btn_frame, text="❌ Cancelar", command=self.destroy, fg_color="#6b7280", hover_color="#4b5563", width=130).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="💾 Guardar", command=self._save, fg_color=self.theme.ACCENT, hover_color="#6d28d9", width=130).pack(side="right", padx=5)
        else:
            ctk.CTkButton(main, text="✓ Cerrar", command=self.destroy, fg_color=self.theme.ACCENT, width=130).pack(pady=(15, 0))
    
    def _populate_data(self):
        """Rellenar datos"""
        if self.cita:
            self.fecha_entry.delete(0, 'end')
            self.fecha_entry.insert(0, self.cita.get('fecha', ''))
            self.hora_entry.delete(0, 'end')
            self.hora_entry.insert(0, self.cita.get('hora', ''))
            self.motivo_entry.insert(0, self.cita.get('motivo', ''))
            self.observaciones_text.insert("1.0", self.cita.get('observaciones', ''))
            self.estado_combo.set(self.cita.get('estado', 'Programada'))
            
            # Mascota
            mascota = get_mascota_by_id(self.cita.get('id_mascota'))
            if mascota:
                valor = f"{mascota['nombre_mascota']} - {mascota['especie']} ({mascota['id_mascota']})"
                self.mascota_combo.set(valor)
            
            # Veterinario
            vet = get_veterinario_by_id(self.cita.get('id_veterinario'))
            if vet:
                valor = f"Dr(a). {vet['nombres']} {vet['apellidos']} - {vet['especialidad']}"
                self.veterinario_combo.set(valor)
    
    def _disable_fields(self):
        """Deshabilitar"""
        self.fecha_entry.configure(state="disabled")
        self.hora_entry.configure(state="disabled")
        self.motivo_entry.configure(state="disabled")
        self.observaciones_text.configure(state="disabled")
        for combo in [self.mascota_combo, self.veterinario_combo, self.estado_combo]:
            combo.configure(state="disabled")
    
    def _save(self):
        """Guardar"""
        if not self.fecha_entry.get().strip() or not self.hora_entry.get().strip():
            messagebox.showerror("Error", "Fecha y hora son obligatorias")
            return
        if not self.motivo_entry.get().strip():
            messagebox.showerror("Error", "El motivo es obligatorio")
            return
        
        # Extraer IDs
        mascota_str = self.mascota_combo.get()
        id_mascota = int(mascota_str.split('(')[-1].replace(')', ''))
        
        vet_str = self.veterinario_combo.get()
        # Buscar veterinario por nombre
        vet = next((v for v in VETERINARIOS if f"{v['nombres']} {v['apellidos']}" in vet_str), None)
        if not vet:
            messagebox.showerror("Error", "Veterinario no encontrado")
            return
        
        self.result = {
            'fecha': self.fecha_entry.get().strip(),
            'hora': self.hora_entry.get().strip(),
            'id_mascota': id_mascota,
            'id_veterinario': vet['id'],
            'motivo': self.motivo_entry.get().strip(),
            'observaciones': self.observaciones_text.get("1.0", "end-1c").strip(),
            'estado': self.estado_combo.get()
        }
        
        if self.mode == 'add':
            self.result['id_cita'] = max([c.get('id_cita', 0) for c in CITAS] + [0]) + 1
            self.event_manager.emit(AppEvents.CITA_ADDED, {'cita': self.result})
            NotificationManager.show_success(self.master, "✓ Cita agendada")
        else:
            self.result['id_cita'] = self.cita['id_cita']
            self.event_manager.emit(AppEvents.CITA_UPDATED, {'cita': self.result})
            NotificationManager.show_success(self.master, "✓ Cita actualizada")
        
        self.destroy()


class CitasViewSimple(ctk.CTkScrollableFrame):
    """Vista de citas con drag-and-drop"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.theme.COLORS["bg"])
        self.app = app
        self.theme = app.theme
        self.citas = CITAS.copy()
        self.filtered_citas = self.citas.copy()
        
        # Drag and drop
        self.dragging_row = None
        self.drag_start_y = 0
        
        # Contexto
        self.context = AppContext()
        self.event_manager = self.context.event_manager
        
        # Suscribirse
        self.event_manager.subscribe(AppEvents.CITA_ADDED, self._on_cita_added)
        self.event_manager.subscribe(AppEvents.CITA_UPDATED, self._on_cita_updated)
        self.event_manager.subscribe(AppEvents.CITA_DELETED, self._on_cita_deleted)
        
        self._create_widgets()
        self._update_table()
    
    def _on_cita_added(self, event):
        cita = event.data.get('cita')
        if cita:
            self.citas.append(cita)
            self._apply_filters()
    
    def _on_cita_updated(self, event):
        cita = event.data.get('cita')
        if cita:
            for i, c in enumerate(self.citas):
                if c['id_cita'] == cita['id_cita']:
                    self.citas[i].update(cita)
                    break
            self._apply_filters()
    
    def _on_cita_deleted(self, event):
        cita_id = event.data.get('cita_id')
        if cita_id:
            self.citas = [c for c in self.citas if c['id_cita'] != cita_id]
            self._apply_filters()
    
    def _create_widgets(self):
        """Crear interfaz"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(header, text="GESTIÓN DE CITAS 📅", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.theme.ACCENT)
        title.pack(side="left")
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="🔄", command=self._refresh, width=50, fg_color=self.theme.ACCENT, hover_color="#6d28d9").pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="➕ Nueva Cita", command=self._add_cita, fg_color=self.theme.ACCENT, hover_color="#6d28d9", width=150).pack(side="right", padx=5)
        
        # Tip de drag-drop
        tip_frame = ctk.CTkFrame(self, fg_color="#dbeafe", corner_radius=8)
        tip_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            tip_frame,
            text="💡 TIP: Haz clic sobre una fila, mantén presionado y arrastra para reorganizar las citas",
            font=ctk.CTkFont(size=12),
            text_color="#1e40af"
        ).pack(pady=10)
        
        # Búsqueda
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Buscar...", height=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self._apply_filters())
        
        self.filter_combo = ctk.CTkComboBox(
            search_frame,
            values=["Todos los estados", "Programada", "Atendida", "Cancelada"],
            command=lambda v: self._apply_filters(),
            width=200
        )
        self.filter_combo.set("Todos los estados")
        self.filter_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(search_frame, text="🗑️ Limpiar", command=self._clear_filters, fg_color="#6b7280", hover_color="#4b5563", width=100).pack(side="left", padx=5)
        
        # Contenedor tabla
        self.table_container = ctk.CTkFrame(self, fg_color=self.theme.COLORS["surface"])
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.count_label = ctk.CTkLabel(self.table_container, text="", font=ctk.CTkFont(size=12), text_color=self.theme.TEXT_SECONDARY)
        self.count_label.pack(pady=10)
    
    def _update_table(self):
        """Actualizar tabla"""
        for widget in self.table_container.winfo_children():
            if isinstance(widget, DataTable):
                widget.destroy()
        
        self.count_label.pack(pady=10)
        self.count_label.configure(text=f"Mostrando {len(self.filtered_citas)} de {len(self.citas)} citas")
        
        columns = ["N°", "Fecha", "Hora", "Mascota", "Veterinario", "Motivo", "Estado", "Acciones"]
        
        # Colores para badges de estado
        estado_colors = {
            "Programada": {"bg": "#3b82f6", "text": "white"},  # Azul
            "Atendida": {"bg": "#10b981", "text": "white"},    # Verde
            "Cancelada": {"bg": "#6b7280", "text": "white"}    # Gris
        }
        
        self.table = DataTable(self.table_container, columns=columns, theme=self.theme, height=400)
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for idx, cita in enumerate(self.filtered_citas, 1):
            mascota = get_mascota_by_id(cita['id_mascota'])
            vet = get_veterinario_by_id(cita['id_veterinario'])
            
            mascota_nombre = mascota['nombre_mascota'] if mascota else "N/A"
            vet_nombre = f"Dr. {vet['apellidos']}" if vet else "N/A"
            
            row_data = [
                str(idx),
                cita['fecha'],
                cita['hora'],
                mascota_nombre,
                vet_nombre,
                cita['motivo'][:30] + "..." if len(cita['motivo']) > 30 else cita['motivo'],
                cita['estado']
            ]
            
            actions = [
                ("👁️", lambda c=cita: self._view_cita(c), self.theme.INFO),
                ("✏️", lambda c=cita: self._edit_cita(c), self.theme.ACCENT),
                ("🗑️", lambda c=cita: self._delete_cita(c), self.theme.DANGER)
            ]
            
            # Agregar fila con colores de estado y binding para drag
            row_frame = self.table.add_row(row_data, actions, estado_colors)
            self._setup_drag_drop(row_frame, cita, idx - 1)
    
    def _setup_drag_drop(self, row_frame, cita, index):
        """Configurar drag-and-drop mejorado en una fila"""
        dragging_data = {"active": False, "start_y": 0, "start_index": index}
        
        def on_press(event):
            dragging_data["active"] = True
            dragging_data["start_y"] = event.y_root
            dragging_data["start_index"] = index
            self.dragging_row = cita
            self.drag_start_y = event.y_root
            
            # Efecto visual de inicio
            row_frame.configure(
                cursor="fleur",
                fg_color="#e0e7ff",
                border_width=2,
                border_color="#3b82f6"
            )
            row_frame.lift()  # Traer al frente
        
        def on_motion(event):
            if dragging_data["active"]:
                delta_y = event.y_root - dragging_data["start_y"]
                
                # Cambiar color del borde según dirección
                if delta_y < -20:
                    row_frame.configure(border_color="#8b5cf6")  # Púrpura arriba
                elif delta_y > 20:
                    row_frame.configure(border_color="#f59e0b")  # Naranja abajo
                else:
                    row_frame.configure(border_color="#3b82f6")  # Azul
        
        def on_release(event):
            if dragging_data["active"]:
                row_frame.configure(
                    cursor="arrow",
                    fg_color="transparent",
                    border_width=0
                )
                
                # Calcular movimiento
                delta_y = event.y_root - dragging_data["start_y"]
                
                if abs(delta_y) > 40:  # Umbral mínimo
                    # Calcular filas movidas (~60px por fila)
                    rows_moved = int(delta_y / 60)
                    new_index = max(0, min(
                        len(self.filtered_citas) - 1,
                        dragging_data["start_index"] + rows_moved
                    ))
                    
                    if new_index != dragging_data["start_index"]:
                        # Reordenar lista
                        cita_to_move = self.filtered_citas.pop(dragging_data["start_index"])
                        self.filtered_citas.insert(new_index, cita_to_move)
                        
                        # Actualizar vista
                        self._update_table()
                        
                        # Notificación
                        direction = "arriba" if rows_moved < 0 else "abajo"
                        NotificationManager.show_success(
                            self,
                            f"✓ Cita movida {abs(rows_moved)} posición(es) hacia {direction}"
                        )
                
                self.dragging_row = None
                dragging_data["active"] = False
        
        # Cambiar cursor al pasar
        def on_enter(event):
            if not dragging_data["active"]:
                row_frame.configure(cursor="grab")
        
        def on_leave(event):
            if not dragging_data["active"]:
                row_frame.configure(cursor="arrow")
        
        row_frame.bind("<Button-1>", on_press)
        row_frame.bind("<B1-Motion>", on_motion)
        row_frame.bind("<ButtonRelease-1>", on_release)
        row_frame.bind("<Enter>", on_enter)
        row_frame.bind("<Leave>", on_leave)
    
    def _apply_filters(self):
        """Aplicar filtros"""
        search = self.search_entry.get().lower()
        estado = self.filter_combo.get()
        
        self.filtered_citas = [
            c for c in self.citas
            if (search in c['motivo'].lower())
            and (estado == "Todos los estados" or c['estado'] == estado)
        ]
        
        self._update_table()
    
    def _clear_filters(self):
        """Limpiar filtros"""
        self.search_entry.delete(0, 'end')
        self.filter_combo.set("Todos los estados")
        self._apply_filters()
    
    def _refresh(self):
        """Refrescar"""
        self.filtered_citas = self.citas.copy()
        self._update_table()
        NotificationManager.show_success(self, "✓ Datos actualizados")
    
    def _add_cita(self):
        """Agregar"""
        dialog = CitaFormDialog(self, 'add', None, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _view_cita(self, cita):
        """Ver"""
        dialog = CitaFormDialog(self, 'view', cita, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _edit_cita(self, cita):
        """Editar"""
        dialog = CitaFormDialog(self, 'edit', cita, self.theme, self.event_manager)
        self.wait_window(dialog)
    
    def _delete_cita(self, cita):
        """Eliminar"""
        if messagebox.askyesno("Confirmar", f"¿Cancelar cita del {cita['fecha']} a las {cita['hora']}?"):
            self.event_manager.emit(AppEvents.CITA_DELETED, {'cita_id': cita['id_cita']})
            NotificationManager.show_success(self, "✓ Cita cancelada")
