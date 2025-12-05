"""
Vista del Dashboard principal
"""

import customtkinter as ctk
from utils.mock_data import CLIENTES, MASCOTAS, CITAS, VETERINARIOS


class DashboardView(ctk.CTkScrollableFrame):
    """Vista del dashboard con estadísticas"""
    
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.theme.COLORS["bg"])
        self.app = app
        self.theme = app.theme
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crear los widgets del dashboard"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        # Título con bienvenida
        welcome_frame = ctk.CTkFrame(header, fg_color=self.theme.COLORS["bg_card"], corner_radius=15)
        welcome_frame.pack(fill="x", pady=(0, 20))
        
        welcome_content = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        welcome_content.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(
            welcome_content,
            text="BIENVENIDO/A 🤓",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme.COLORS["text"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            welcome_content,
            text="RECEPCIONISTA",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.theme.COLORS["primary"]
        ).pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(
            welcome_content,
            text="Colitas Felices - Veterinaria 🧑🏻‍💻",
            font=ctk.CTkFont(size=14),
            text_color=self.theme.COLORS["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        
        # Estadísticas
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=30, pady=20)
        
        # Grid para las tarjetas
        stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Calcular estadísticas
        stats_data = [
            {
                "title": "Mascotas registradas",
                "value": len([m for m in MASCOTAS if m["estado"] == "Activo"]),
                "icon": "🐾",
                "color": self.theme.get_stat_color("mascotas")
            },
            {
                "title": "Citas programadas",
                "value": len([c for c in CITAS if c["estado"] == "Programada"]),
                "icon": "📅",
                "color": self.theme.get_stat_color("citas")
            },
            {
                "title": "Clientes activos",
                "value": len([c for c in CLIENTES if c["estado"] == "Activo"]),
                "icon": "👥",
                "color": self.theme.get_stat_color("clientes")
            },
            {
                "title": "Veterinarios disponibles",
                "value": len([v for v in VETERINARIOS if v["estado"] == "Activo"]),
                "icon": "👨‍⚕️",
                "color": self.theme.get_stat_color("veterinarios")
            }
        ]
        
        for idx, stat in enumerate(stats_data):
            self._create_stat_card(stats_container, stat, idx)
            
        # Accesos rápidos
        quick_access_title = ctk.CTkLabel(
            self,
            text="Accesos Rápidos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.theme.COLORS["text"]
        )
        quick_access_title.pack(anchor="w", padx=30, pady=(30, 15))
        
        actions_container = ctk.CTkFrame(self, fg_color="transparent")
        actions_container.pack(fill="x", padx=30, pady=10)
        
        # Grid para acciones rápidas
        actions_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        actions = [
            ("Ver Clientes", "👥", self.app.show_clientes, self.theme.COLORS["primary"]),
            ("Ver Mascotas", "🐾", self.app.show_mascotas, self.theme.COLORS["success"]),
            ("Gestionar Citas", "📅", self.app.show_citas, "#8b5cf6"),
            ("Veterinarios", "👨‍⚕️", self.app.show_veterinarios, self.theme.COLORS["warning"])
        ]
        
        for idx, (text, icon, command, color) in enumerate(actions):
            self._create_action_button(actions_container, text, icon, command, color, idx)
            
    def _create_stat_card(self, parent, stat, column):
        """Crear una tarjeta de estadística"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme.COLORS["bg_card"],
            corner_radius=15
        )
        card.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Contenido
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono
        icon_label = ctk.CTkLabel(
            content,
            text=stat["icon"],
            font=ctk.CTkFont(size=40),
        )
        icon_label.pack(pady=(0, 10))
        
        # Valor
        value_label = ctk.CTkLabel(
            content,
            text=str(stat["value"]).zfill(2),
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=stat["color"]
        )
        value_label.pack()
        
        # Título
        title_label = ctk.CTkLabel(
            content,
            text=stat["title"],
            font=ctk.CTkFont(size=13),
            text_color=self.theme.COLORS["text_secondary"],
            wraplength=150
        )
        title_label.pack(pady=(5, 0))
        
    def _create_action_button(self, parent, text, icon, command, color, column):
        """Crear un botón de acción rápida"""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        btn = ctk.CTkButton(
            btn_frame,
            text=f"{icon}\n{text}",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=color,
            hover_color=self._darken_color(color),
            height=100,
            corner_radius=15,
            command=command
        )
        btn.pack(fill="both", expand=True)
        
    def _darken_color(self, color):
        """Oscurecer un color para el hover"""
        # Simplificación: devolver una versión más oscura
        color_map = {
            self.theme.COLORS["primary"]: self.theme.COLORS["primary_dark"],
            self.theme.COLORS["success"]: self.theme.COLORS["secondary_dark"],
            "#8b5cf6": "#7c3aed",
            self.theme.COLORS["warning"]: "#d97706"
        }
        return color_map.get(color, color)
