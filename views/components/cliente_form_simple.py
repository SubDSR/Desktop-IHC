"""
Formulario de Cliente - Mejorado con validación en tiempo real
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.validators import Validator
from utils.animations import NotificationManager
from utils.event_manager import AppEvents
from utils.mock_data import MASCOTAS, get_mascotas_by_cliente


class ValidatedEntry(ctk.CTkEntry):
    """Entry con validación en tiempo real"""
    
    def __init__(self, parent, validator_func=None, validator_type=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.validator_func = validator_func
        self.validator_type = validator_type
        self.is_valid = False
        
        # Validar mientras escribe
        self.bind("<KeyRelease>", self._on_change)
    
    def _on_change(self, event=None):
        """Validar en tiempo real"""
        value = self.get().strip()
        
        # Si está vacío, borde gris
        if not value:
            self.configure(border_color="#cbd5e1", border_width=2)
            self.is_valid = False
            return
        
        # Aplicar validación específica
        if self.validator_func:
            is_valid, _ = self.validator_func(value)
            if is_valid:
                self.configure(border_color="#10b981", border_width=2)  # Verde
                self.is_valid = True
            else:
                self.configure(border_color="#ef4444", border_width=2)  # Rojo
                self.is_valid = False
        else:
            self.configure(border_color="#10b981", border_width=2)
            self.is_valid = True
    
    def validate(self):
        """Validar al enviar"""
        value = self.get().strip()
        
        if not value:
            self.configure(border_color="#ef4444", border_width=2)
            return False, "Este campo es obligatorio"
        
        if self.validator_func:
            is_valid, error_message = self.validator_func(value)
            if not is_valid:
                self.configure(border_color="#ef4444", border_width=2)
            return is_valid, error_message
        
        return True, None
    
    def reset_validation(self):
        """Resetear validación"""
        self.configure(border_color="#cbd5e1", border_width=2)
        self.is_valid = False


class ClienteFormDialog(ctk.CTkToplevel):
    """Formulario de cliente mejorado"""
    
    def __init__(self, parent, mode, cliente, theme, event_manager):
        super().__init__(parent)
        
        self.mode = mode  # "new", "edit", "view"
        self.cliente = cliente
        self.theme = theme
        self.event_manager = event_manager
        
        # Configuración de ventana
        self.title(self._get_title())
        self.geometry("650x750")
        self.resizable(False, False)
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.winfo_screenheight() // 2) - (750 // 2)
        self.geometry(f"650x750+{x}+{y}")
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if self.mode in ["edit", "view"]:
            self._load_data()
    
    def _get_title(self):
        """Obtener título según modo"""
        titles = {
            "new": "Registrar Nuevo Cliente",
            "edit": "Modificar Cliente",
            "view": "Detalles del Cliente"
        }
        return titles.get(self.mode, "Cliente")
    
    def _create_widgets(self):
        """Crear widgets del formulario"""
        # Contenedor principal con scroll
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="white"
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # SECCIÓN: DATOS PERSONALES
        personal_header = ctk.CTkFrame(
            main_container,
            fg_color="#5b9bd5",
            corner_radius=8,
            height=40
        )
        personal_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            personal_header,
            text="DATOS PERSONALES",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        ).pack(pady=8)
        
        # Grid para datos personales
        personal_grid = ctk.CTkFrame(main_container, fg_color="transparent")
        personal_grid.pack(fill="x", pady=(0, 20))
        personal_grid.grid_columnconfigure((0, 1), weight=1)
        
        # DNI
        self._create_field_label(personal_grid, "DNI DEL CLIENTE (*)", 0, 0)
        self.dni_entry = ValidatedEntry(
            personal_grid,
            validator_func=Validator.validate_dni,
            placeholder_text="DNI",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.dni_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 15), sticky="ew")
        
        # Nombres
        self._create_field_label(personal_grid, "NOMBRES (*)", 0, 1)
        self.nombres_entry = ValidatedEntry(
            personal_grid,
            validator_func=lambda x: (len(x) >= 2, "Mínimo 2 caracteres"),
            placeholder_text="Nombres",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.nombres_entry.grid(row=1, column=1, padx=(10, 0), pady=(0, 15), sticky="ew")
        
        # Apellido Paterno
        self._create_field_label(personal_grid, "APELLIDO PATERNO (*)", 2, 0)
        self.ap_paterno_entry = ValidatedEntry(
            personal_grid,
            validator_func=lambda x: (len(x) >= 2, "Mínimo 2 caracteres"),
            placeholder_text="Apellido Paterno",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.ap_paterno_entry.grid(row=3, column=0, padx=(0, 10), pady=(0, 15), sticky="ew")
        
        # Apellido Materno
        self._create_field_label(personal_grid, "APELLIDO MATERNO (*)", 2, 1)
        self.ap_materno_entry = ValidatedEntry(
            personal_grid,
            validator_func=lambda x: (len(x) >= 2, "Mínimo 2 caracteres"),
            placeholder_text="Apellido Materno",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.ap_materno_entry.grid(row=3, column=1, padx=(10, 0), pady=(0, 15), sticky="ew")
        
        # SECCIÓN: DATOS DE CONTACTO
        contact_header = ctk.CTkFrame(
            main_container,
            fg_color="#5b9bd5",
            corner_radius=8,
            height=40
        )
        contact_header.pack(fill="x", pady=(10, 15))
        
        ctk.CTkLabel(
            contact_header,
            text="DATOS DE CONTACTO",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        ).pack(pady=8)
        
        # Grid para contacto
        contact_grid = ctk.CTkFrame(main_container, fg_color="transparent")
        contact_grid.pack(fill="x", pady=(0, 20))
        contact_grid.grid_columnconfigure((0, 1), weight=1)
        
        # Teléfono
        self._create_field_label(contact_grid, "TELÉFONO (*)", 0, 0)
        self.telefono_entry = ValidatedEntry(
            contact_grid,
            validator_func=Validator.validate_phone,
            placeholder_text="Teléfono",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.telefono_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 15), sticky="ew")
        
        # Email
        self._create_field_label(contact_grid, "EMAIL (*)", 0, 1)
        self.email_entry = ValidatedEntry(
            contact_grid,
            validator_func=Validator.validate_email,
            placeholder_text="Email",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.email_entry.grid(row=1, column=1, padx=(10, 0), pady=(0, 15), sticky="ew")
        
        # Dirección (full width)
        self._create_field_label(contact_grid, "DIRECCIÓN (*)", 2, 0, columnspan=2)
        self.direccion_entry = ValidatedEntry(
            contact_grid,
            validator_func=lambda x: (len(x) >= 5, "Mínimo 5 caracteres"),
            placeholder_text="Dirección",
            height=35,
            border_width=2,
            border_color="#cbd5e1"
        )
        self.direccion_entry.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # SECCIÓN: MASCOTAS REGISTRADAS (solo en modo edit/view)
        if self.mode in ["edit", "view"] and self.cliente:
            mascotas_header = ctk.CTkFrame(
                main_container,
                fg_color="#5b9bd5",
                corner_radius=8,
                height=40
            )
            mascotas_header.pack(fill="x", pady=(10, 15))
            
            ctk.CTkLabel(
                mascotas_header,
                text="MASCOTAS REGISTRADAS",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white"
            ).pack(pady=8)
            
            # Tabla de mascotas
            mascotas_table = ctk.CTkFrame(main_container, fg_color="white")
            mascotas_table.pack(fill="x", pady=(0, 20))
            
            # Headers
            headers = ["NOMBRE", "ESPECIE", "RAZA"]
            for idx, header in enumerate(headers):
                ctk.CTkLabel(
                    mascotas_table,
                    text=header,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#64748b"
                ).grid(row=0, column=idx, padx=10, pady=5, sticky="w")
            
            # Datos de mascotas
            mascotas = get_mascotas_by_cliente(self.cliente['id'])
            if mascotas:
                for idx, mascota in enumerate(mascotas, 1):
                    ctk.CTkLabel(
                        mascotas_table,
                        text=mascota['nombre_mascota'],
                        font=ctk.CTkFont(size=11)
                    ).grid(row=idx, column=0, padx=10, pady=3, sticky="w")
                    
                    ctk.CTkLabel(
                        mascotas_table,
                        text=mascota['especie'],
                        font=ctk.CTkFont(size=11)
                    ).grid(row=idx, column=1, padx=10, pady=3, sticky="w")
                    
                    ctk.CTkLabel(
                        mascotas_table,
                        text=mascota['raza'],
                        font=ctk.CTkFont(size=11)
                    ).grid(row=idx, column=2, padx=10, pady=3, sticky="w")
            else:
                ctk.CTkLabel(
                    mascotas_table,
                    text="No hay mascotas registradas",
                    font=ctk.CTkFont(size=11),
                    text_color="#94a3b8"
                ).grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # Botones
        if self.mode != "view":
            buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(20, 0))
            
            # Botón Guardar/Finalizar
            save_btn = ctk.CTkButton(
                buttons_frame,
                text="FINALIZAR REGISTRO" if self.mode == "new" else "GUARDAR",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#10b981",
                hover_color="#059669",
                height=40,
                command=self._save
            )
            save_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
            
            # Botón Cancelar
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="CANCELAR",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#6b7280",
                hover_color="#4b5563",
                height=40,
                command=self.destroy
            )
            cancel_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))
        else:
            # Solo botón cerrar en modo view
            close_btn = ctk.CTkButton(
                main_container,
                text="CERRAR",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#6b7280",
                hover_color="#4b5563",
                height=40,
                command=self.destroy
            )
            close_btn.pack(fill="x", pady=(20, 0))
    
    def _create_field_label(self, parent, text, row, col, columnspan=1):
        """Crear etiqueta de campo"""
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#64748b",
            anchor="w"
        )
        label.grid(row=row, column=col, columnspan=columnspan, sticky="w", pady=(0, 5))
    
    def _load_data(self):
        """Cargar datos del cliente"""
        if not self.cliente:
            return
        
        self.dni_entry.insert(0, self.cliente.get('dni', ''))
        self.nombres_entry.insert(0, self.cliente.get('nombres', ''))
        
        # Separar apellidos
        apellidos = self.cliente.get('apellidos', '').split(' ', 1)
        if len(apellidos) >= 1:
            self.ap_paterno_entry.insert(0, apellidos[0])
        if len(apellidos) >= 2:
            self.ap_materno_entry.insert(0, apellidos[1])
        
        self.telefono_entry.insert(0, self.cliente.get('telefono', ''))
        self.email_entry.insert(0, self.cliente.get('email', ''))
        self.direccion_entry.insert(0, self.cliente.get('direccion', ''))
        
        # Validar campos inicialmente
        for entry in [self.dni_entry, self.nombres_entry, self.ap_paterno_entry,
                      self.ap_materno_entry, self.telefono_entry, self.email_entry,
                      self.direccion_entry]:
            entry._on_change()
        
        # Si es modo view, deshabilitar campos
        if self.mode == "view":
            for entry in [self.dni_entry, self.nombres_entry, self.ap_paterno_entry,
                          self.ap_materno_entry, self.telefono_entry, self.email_entry,
                          self.direccion_entry]:
                entry.configure(state="disabled")
    
    def _save(self):
        """Guardar cliente"""
        # Validar todos los campos
        fields = {
            "DNI": self.dni_entry,
            "Nombres": self.nombres_entry,
            "Apellido Paterno": self.ap_paterno_entry,
            "Apellido Materno": self.ap_materno_entry,
            "Teléfono": self.telefono_entry,
            "Email": self.email_entry,
            "Dirección": self.direccion_entry
        }
        
        errors = []
        for field_name, entry in fields.items():
            is_valid, error_msg = entry.validate()
            if not is_valid:
                errors.append(f"{field_name}: {error_msg}")
        
        if errors:
            messagebox.showerror(
                "Error de validación",
                "Por favor corrija los siguientes errores:\n\n" + "\n".join(errors)
            )
            return
        
        # Recopilar datos
        cliente_data = {
            "dni": self.dni_entry.get().strip(),
            "nombres": self.nombres_entry.get().strip(),
            "apellidos": f"{self.ap_paterno_entry.get().strip()} {self.ap_materno_entry.get().strip()}",
            "telefono": self.telefono_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "direccion": self.direccion_entry.get().strip(),
            "estado": "Activo"
        }
        
        if self.mode == "edit":
            cliente_data["id"] = self.cliente["id"]
        
        # Emitir evento
        event = AppEvents.CLIENTE_UPDATED if self.mode == "edit" else AppEvents.CLIENTE_CREATED
        self.event_manager.emit(event, cliente_data)
        
        # Mostrar notificación
        msg = "Cliente actualizado correctamente" if self.mode == "edit" else "Cliente agregado correctamente"
        NotificationManager.show_success(self.master, msg)
        
        self.destroy()
