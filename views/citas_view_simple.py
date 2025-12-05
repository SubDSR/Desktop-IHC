"""
Vista de citas - Versión Completa Mejorada con diseño legible y Drag & Drop
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from utils.mock_data import CITAS, MASCOTAS, VETERINARIOS, get_mascota_by_id, get_veterinario_by_id
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
        
        # Fecha y Hora
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
            
            mascota = get_mascota_by_id(self.cita.get('id_mascota'))
            if mascota:
                valor = f"{mascota['nombre_mascota']} - {mascota['especie']} ({mascota['id_mascota']})"
                self.mascota_combo.set(valor)
            
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
        
        mascota_str = self.mascota_combo.get()
        id_mascota = int(mascota_str.split('(')[-1].replace(')', ''))
        
        vet_str = self.veterinario_combo.get()
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
    """Vista de citas con diseño mejorado y Drag & Drop"""
    
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
            text="💡 Arrastra las filas para reordenar las prioridades (mantén clic y arrastra)",
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
        self.table_container = ctk.CTkFrame(self, fg_color=self.theme.COLORS["surface"], corner_radius=10)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.count_label = ctk.CTkLabel(self.table_container, text="", font=ctk.CTkFont(size=12), text_color=self.theme.TEXT_SECONDARY)
        self.count_label.pack(pady=10)
        
        # Frame para las filas
        self.rows_frame = ctk.CTkFrame(self.table_container, fg_color="transparent")
        self.rows_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def _update_table(self):
        """Actualizar tabla con diseño mejorado"""
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        
        self.count_label.configure(text=f"📋 Mostrando {len(self.filtered_citas)} de {len(self.citas)} citas")
        
        # Header de la tabla
        header_row = ctk.CTkFrame(self.rows_frame, fg_color=self.theme.ACCENT, height=45, corner_radius=8)
        header_row.pack(fill="x", pady=(0, 5))
        header_row.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        headers = ["📅 Fecha", "⏰ Hora", "🐾 Mascota", "💬 Motivo", "📊 Estado", "⚙️ Acciones"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                header_row,
                text=header,
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=8, pady=10)
        
        # Renderizar filas
        for index, cita in enumerate(self.filtered_citas):
            self._create_row(index, cita)
    
    def _create_row(self, index, cita):
        """Crear una fila con diseño mejorado y bordes visibles"""
        mascota = get_mascota_by_id(cita['id_mascota'])
        mascota_nom = mascota['nombre_mascota'] if mascota else "Desconocido"
        
        # Color de borde según estado (más oscuros para mejor visibilidad)
        border_colors = {
            'Programada': "#2563eb",  # Azul oscuro
            'Atendida': "#059669",    # Verde oscuro
            'Cancelada': "#dc2626"    # Rojo oscuro
        }
        border = border_colors.get(cita['estado'], "#94a3b8")
        
        # Color de fondo con tinte según estado
        bg_colors = {
            'Programada': "#eff6ff",  # Azul muy claro
            'Atendida': "#f0fdf4",    # Verde muy claro
            'Cancelada': "#fef2f2"    # Rojo muy claro
        }
        bg_color = bg_colors.get(cita['estado'], "white")
        
        # Frame de la fila con borde grueso y visible
        row = ctk.CTkFrame(
            self.rows_frame,
            fg_color=bg_color,
            corner_radius=10,
            border_width=3,  # Borde más grueso
            border_color=border,
            height=65
        )
        row.pack(fill="x", pady=4, padx=5)  # Más espacio entre filas
        row.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Fecha con badge visual
        fecha_frame = ctk.CTkFrame(row, fg_color="transparent")
        fecha_frame.grid(row=0, column=0, pady=12, padx=8)
        
        ctk.CTkLabel(
            fecha_frame,
            text=cita['fecha'],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#1e293b"
        ).pack()
        
        # Hora
        ctk.CTkLabel(
            row,
            text=cita['hora'],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#475569"
        ).grid(row=0, column=1, pady=12, padx=8)
        
        # Mascota con ícono
        mascota_frame = ctk.CTkFrame(row, fg_color="transparent")
        mascota_frame.grid(row=0, column=2, pady=12, padx=8)
        
        ctk.CTkLabel(
            mascota_frame,
            text=f"🐾 {mascota_nom}",
            font=ctk.CTkFont(size=11),
            text_color="#475569"
        ).pack()
        
        # Motivo (truncado)
        motivo_corto = cita['motivo'][:22] + "..." if len(cita['motivo']) > 22 else cita['motivo']
        ctk.CTkLabel(
            row,
            text=motivo_corto,
            font=ctk.CTkFont(size=11),
            text_color="#64748b"
        ).grid(row=0, column=3, pady=12, padx=8)
        
        # Badge Estado con más contraste
        estado_colors = {
            "Programada": ("#2563eb", "white"),   # Azul oscuro
            "Atendida": ("#059669", "white"),     # Verde oscuro
            "Cancelada": ("#dc2626", "white")     # Rojo oscuro
        }
        bg_color_badge, text_color = estado_colors.get(cita['estado'], ("#64748B", "white"))
        
        badge = ctk.CTkLabel(
            row,
            text=cita['estado'],
            text_color=text_color,
            fg_color=bg_color_badge,
            corner_radius=15,
            width=95,
            height=30,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        badge.grid(row=0, column=4, pady=12, padx=8)
        
        # Botones de Acciones
        actions = ctk.CTkFrame(row, fg_color="transparent")
        actions.grid(row=0, column=5, pady=12, padx=8)
        
        # Botón Ver
        btn_view = ctk.CTkButton(
            actions,
            text="👁️",
            width=38,
            height=32,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=ctk.CTkFont(size=14),
            command=lambda: self._view_cita(cita)
        )
        btn_view.pack(side="left", padx=2)
        
        # Botón Editar
        btn_edit = ctk.CTkButton(
            actions,
            text="✏️",
            width=38,
            height=32,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=ctk.CTkFont(size=14),
            command=lambda: self._edit_cita(cita)
        )
        btn_edit.pack(side="left", padx=2)
        
        # Botón Eliminar
        btn_delete = ctk.CTkButton(
            actions,
            text="🗑️",
            width=38,
            height=32,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=ctk.CTkFont(size=14),
            command=lambda: self._delete_cita(cita)
        )
        btn_delete.pack(side="left", padx=2)
        
        # Setup Drag & Drop
        self._setup_drag_drop(row, cita, index)
        
        return row
    
    def _setup_drag_drop(self, row_frame, cita, index):
        """Configurar drag-and-drop con efectos visuales mejorados"""
        dragging_data = {"active": False, "start_y": 0, "start_index": index}
        
        # Guardar colores originales
        original_border_colors = {
            'Programada': "#2563eb",
            'Atendida': "#059669",
            'Cancelada': "#dc2626"
        }
        original_bg_colors = {
            'Programada': "#eff6ff",
            'Atendida': "#f0fdf4",
            'Cancelada': "#fef2f2"
        }
        
        def on_press(event):
            dragging_data["active"] = True
            dragging_data["start_y"] = event.y_root
            dragging_data["start_index"] = index
            self.dragging_row = cita
            self.drag_start_y = event.y_root
            
            # Efecto visual de arrastre: fondo amarillo claro y borde púrpura grueso
            row_frame.configure(
                cursor="fleur",
                fg_color="#fef3c7",  # Amarillo claro
                border_width=4,      # Borde más grueso
                border_color="#8b5cf6"  # Púrpura brillante
            )
            row_frame.lift()
        
        def on_motion(event):
            if dragging_data["active"]:
                delta_y = event.y_root - dragging_data["start_y"]
                
                # Cambiar color de borde según dirección
                if delta_y < -20:
                    row_frame.configure(border_color="#3b82f6")  # Azul (arriba)
                elif delta_y > 20:
                    row_frame.configure(border_color="#f59e0b")  # Naranja (abajo)
                else:
                    row_frame.configure(border_color="#8b5cf6")  # Púrpura (neutral)
        
        def on_release(event):
            if dragging_data["active"]:
                # Restaurar apariencia original
                original_border = original_border_colors.get(cita['estado'], "#94a3b8")
                original_bg = original_bg_colors.get(cita['estado'], "white")
                
                row_frame.configure(
                    cursor="arrow",
                    fg_color=original_bg,
                    border_width=3,
                    border_color=original_border
                )
                
                # Calcular movimiento
                delta_y = event.y_root - dragging_data["start_y"]
                
                if abs(delta_y) > 40:
                    rows_moved = int(delta_y / 69)  # ~69px por fila (65 altura + 4 padding)
                    new_index = max(0, min(
                        len(self.filtered_citas) - 1,
                        dragging_data["start_index"] + rows_moved
                    ))
                    
                    if new_index != dragging_data["start_index"]:
                        cita_to_move = self.filtered_citas.pop(dragging_data["start_index"])
                        self.filtered_citas.insert(new_index, cita_to_move)
                        
                        self._update_table()
                        
                        direction = "arriba ⬆️" if rows_moved < 0 else "abajo ⬇️"
                        NotificationManager.show_success(
                            self,
                            f"✓ Prioridad reordenada: {abs(rows_moved)} posición(es) hacia {direction}"
                        )
                
                self.dragging_row = None
                dragging_data["active"] = False
        
        def on_enter(event):
            if not dragging_data["active"]:
                row_frame.configure(cursor="hand2")  # Cambiado de "grab" a "hand2"
                # Efecto hover: aumentar grosor del borde
                row_frame.configure(border_width=4)
        
        def on_leave(event):
            if not dragging_data["active"]:
                row_frame.configure(cursor="arrow")
                # Restaurar grosor original
                row_frame.configure(border_width=3)
        
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