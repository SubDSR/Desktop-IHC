"""
Componente de tabla de datos - Simple y funcional
"""

import customtkinter as ctk


class DataTable(ctk.CTkFrame):
    """Tabla de datos con método add_row"""
    
    def __init__(self, parent, columns, theme=None, height=400):
        super().__init__(parent, fg_color="transparent")
        
        self.columns = columns
        self.theme = theme
        self.rows = []
        
        # Contenedor scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.COLORS["surface"] if theme else "white",
            height=height
        )
        self.scroll_frame.pack(fill="both", expand=True)
        
        # Crear header
        self._create_header()
    
    def _create_header(self):
        """Crear encabezado"""
        header = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.theme.PRIMARY if self.theme else "#2563eb",
            corner_radius=10
        )
        header.pack(fill="x", pady=(0, 10))
        
        for idx, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                anchor="center"
            )
            label.grid(row=0, column=idx, padx=5, pady=10, sticky="ew")
            header.grid_columnconfigure(idx, weight=1)
    
    def add_row(self, data, actions=None, estado_colors=None):
        """
        Agregar fila
        
        Args:
            data: Lista con datos de la fila
            actions: Lista de tuplas (icon, callback, color)
            estado_colors: Diccionario {estado: {"bg": color, "text": color}}
        
        Returns:
            Frame de la fila (para drag & drop)
        """
        row_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.theme.COLORS["bg_card"] if self.theme else "white",
            corner_radius=8
        )
        row_frame.pack(fill="x", pady=2, padx=5)
        
        # Datos
        for idx, value in enumerate(data):
            if idx >= len(self.columns) - (1 if actions else 0):
                break
            
            col_name = self.columns[idx]
            
            if col_name == "Estado":
                # Badge de estado con colores personalizables
                if estado_colors and value in estado_colors:
                    colors = estado_colors[value]
                    bg_color = colors["bg"]
                    text_color = colors["text"]
                elif self.theme:
                    bg_color = self.theme.SUCCESS if value == "Activo" else self.theme.TEXT_SECONDARY
                    text_color = "white"
                else:
                    bg_color = "#10b981" if value == "Activo" else "#64748b"
                    text_color = "white"
                
                badge = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=text_color,
                    fg_color=bg_color,
                    corner_radius=12,
                    height=25,
                    width=100
                )
                badge.grid(row=0, column=idx, padx=5, pady=8)
            else:
                # Texto normal
                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    font=ctk.CTkFont(size=11),
                    text_color=self.theme.TEXT_PRIMARY if self.theme else "#1e293b",
                    anchor="center"
                )
                label.grid(row=0, column=idx, padx=5, pady=8, sticky="ew")
            
            row_frame.grid_columnconfigure(idx, weight=1)
        
        # Botones de acción
        if actions:
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=len(data), padx=5, pady=8)
            
            for icon, callback, color in actions:
                btn = ctk.CTkButton(
                    actions_frame,
                    text=icon,
                    width=35,
                    height=30,
                    fg_color=color,
                    hover_color=color,
                    command=callback
                )
                btn.pack(side="left", padx=2)
        
        self.rows.append(row_frame)
        return row_frame
    
    def clear(self):
        """Limpiar todas las filas"""
        for row in self.rows:
            row.destroy()
        self.rows = []
