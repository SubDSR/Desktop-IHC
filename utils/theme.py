"""
Tema y estilos de la aplicación
"""


class VeterinariaTheme:
    """Clase para gestionar el tema de la aplicación"""
    
    # Atributos directos para acceso fácil
    PRIMARY = "#2563eb"
    PRIMARY_DARK = "#1e40af"
    PRIMARY_LIGHT = "#3b82f6"
    
    SECONDARY = "#10b981"
    SECONDARY_DARK = "#059669"
    
    ACCENT = "#8b5cf6"  # Púrpura para citas
    ACCENT_DARK = "#7c3aed"
    
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    DANGER = "#ef4444"
    DANGER_HOVER = "#dc2626"
    INFO = "#3b82f6"
    
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    
    COLORS = {
        # Colores principales
        "primary": "#2563eb",        # Azul principal
        "primary_dark": "#1e40af",   # Azul oscuro
        "primary_light": "#3b82f6",  # Azul claro
        
        # Colores secundarios
        "secondary": "#10b981",      # Verde
        "secondary_dark": "#059669",
        
        # Acento
        "accent": "#8b5cf6",         # Púrpura
        "accent_dark": "#7c3aed",
        
        # Estados
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "danger_hover": "#dc2626",
        "info": "#3b82f6",
        
        # Fondos
        "bg": "#f8fafc",            # Fondo claro
        "bg_dark": "#f1f5f9",       # Fondo gris claro
        "bg_card": "#ffffff",       # Fondo de tarjetas
        "surface": "#ffffff",       # Superficie
        
        # Texto
        "text": "#1e293b",          # Texto principal
        "text_secondary": "#64748b", # Texto secundario
        "text_light": "#e2e8f0",    # Texto claro
        
        # Bordes
        "border": "#e2e8f0",
        "border_dark": "#cbd5e1",
        
        # Hover
        "hover": "#f1f5f9",
    }
    
    FONTS = {
        "title": ("Segoe UI", 24, "bold"),
        "subtitle": ("Segoe UI", 18, "bold"),
        "heading": ("Segoe UI", 16, "bold"),
        "body": ("Segoe UI", 12),
        "body_bold": ("Segoe UI", 12, "bold"),
        "small": ("Segoe UI", 10),
    }
    
    @staticmethod
    def get_stat_color(stat_type):
        """Obtener color según el tipo de estadística"""
        colors = {
            "mascotas": "#3b82f6",    # Azul
            "citas": "#10b981",       # Verde
            "clientes": "#8b5cf6",    # Púrpura
            "veterinarios": "#f59e0b" # Naranja
        }
        return colors.get(stat_type, "#64748b")
