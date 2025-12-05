"""
Sistema de animaciones y efectos visuales
"""

import customtkinter as ctk
from typing import Callable, Optional


class AnimationManager:
    """Gestor de animaciones para widgets"""
    
    @staticmethod
    def fade_in(widget: ctk.CTkBaseClass, duration: int = 300, callback: Optional[Callable] = None):
        """Efecto de aparición gradual"""
        steps = 20
        increment = 1.0 / steps
        delay = duration // steps
        
        def animate(step=0):
            if step <= steps:
                alpha = step * increment
                try:
                    widget.configure(fg_color=widget.cget("fg_color"))
                    widget.update()
                    widget.after(delay, lambda: animate(step + 1))
                except:
                    pass
            elif callback:
                callback()
        
        animate()
    
    @staticmethod
    def fade_out(widget: ctk.CTkBaseClass, duration: int = 300, callback: Optional[Callable] = None):
        """Efecto de desaparición gradual"""
        steps = 20
        delay = duration // steps
        
        def animate(step=0):
            if step <= steps:
                try:
                    widget.update()
                    widget.after(delay, lambda: animate(step + 1))
                except:
                    pass
            elif callback:
                callback()
        
        animate()
    
    @staticmethod
    def slide_in(widget: ctk.CTkBaseClass, direction: str = "left", duration: int = 300):
        """Efecto de deslizamiento hacia adentro"""
        # Para CustomTkinter, usamos pack/grid con after para simular
        if direction == "left":
            widget.pack(side="left", fill="both", expand=True)
        else:
            widget.pack(side="right", fill="both", expand=True)
    
    @staticmethod
    def shake(widget: ctk.CTkBaseClass, intensity: int = 5, duration: int = 300):
        """Efecto de sacudida (para errores)"""
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        steps = 10
        delay = duration // steps
        
        def animate(step=0):
            if step < steps:
                offset = intensity if step % 2 == 0 else -intensity
                try:
                    widget.place(x=original_x + offset, y=original_y)
                    widget.after(delay, lambda: animate(step + 1))
                except:
                    pass
            else:
                try:
                    widget.place(x=original_x, y=original_y)
                except:
                    pass
        
        animate()
    
    @staticmethod
    def pulse(widget: ctk.CTkBaseClass, scale: float = 1.1, duration: int = 200):
        """Efecto de pulso (para llamar atención)"""
        # Para botones, cambiar el hover_color temporalmente
        try:
            original_color = widget.cget("fg_color")
            widget.configure(fg_color=widget.cget("hover_color"))
            widget.after(duration, lambda: widget.configure(fg_color=original_color))
        except:
            pass
    
    @staticmethod
    def smooth_scroll(widget, target_y: int, duration: int = 300):
        """Scroll suave a una posición"""
        try:
            canvas = widget._parent_canvas
            current_y = canvas.yview()[0]
            steps = 20
            delay = duration // steps
            increment = (target_y - current_y) / steps
            
            def animate(step=0):
                if step <= steps:
                    canvas.yview_moveto(current_y + increment * step)
                    widget.after(delay, lambda: animate(step + 1))
            
            animate()
        except:
            pass


class HoverEffect:
    """Efectos de hover para widgets"""
    
    @staticmethod
    def apply_button_hover(button: ctk.CTkButton, scale: float = 1.05):
        """Aplicar efecto hover a botón"""
        original_color = button.cget("fg_color")
        hover_color = button.cget("hover_color")
        
        def on_enter(e):
            button.configure(cursor="hand2")
            AnimationManager.pulse(button, duration=100)
        
        def on_leave(e):
            button.configure(cursor="")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    @staticmethod
    def apply_card_hover(frame: ctk.CTkFrame):
        """Aplicar efecto hover a tarjeta"""
        original_color = frame.cget("fg_color")
        
        def on_enter(e):
            frame.configure(border_width=2, border_color="#3b82f6")
        
        def on_leave(e):
            frame.configure(border_width=0)
        
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)


class TooltipManager:
    """Gestor de tooltips (mensajes emergentes)"""
    
    @staticmethod
    def create_tooltip(widget, text: str, delay: int = 500):
        """Crear tooltip para un widget"""
        tooltip = None
        
        def on_enter(event):
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            def show():
                nonlocal tooltip
                tooltip = ctk.CTkToplevel(widget)
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{x}+{y}")
                
                label = ctk.CTkLabel(
                    tooltip,
                    text=text,
                    fg_color="#1e293b",
                    text_color="white",
                    corner_radius=6,
                    padx=10,
                    pady=5
                )
                label.pack()
            
            widget.after(delay, show)
        
        def on_leave(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)


class LoadingSpinner:
    """Spinner de carga animado"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.label = None
        self.animation_running = False
    
    def show(self, message: str = "Cargando..."):
        """Mostrar spinner"""
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color="rgba(0, 0, 0, 0.7)",
            corner_radius=10
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.label = ctk.CTkLabel(
            self.frame,
            text=message,
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        self.label.pack(padx=30, pady=20)
        
        self.animation_running = True
        self._animate()
    
    def _animate(self):
        """Animar el spinner"""
        if self.animation_running and self.label:
            current_text = self.label.cget("text")
            base_text = current_text.rstrip(".")
            dots = len(current_text) - len(base_text)
            
            if dots < 3:
                new_text = base_text + "." * (dots + 1)
            else:
                new_text = base_text
            
            self.label.configure(text=new_text)
            self.frame.after(300, self._animate)
    
    def hide(self):
        """Ocultar spinner"""
        self.animation_running = False
        if self.frame:
            self.frame.destroy()
            self.frame = None
            self.label = None


class NotificationManager:
    """Gestor de notificaciones toast"""
    
    @staticmethod
    def show_success(parent, message: str, duration: int = 3000):
        """Mostrar notificación de éxito"""
        NotificationManager._show_notification(parent, message, "#10b981", duration)
    
    @staticmethod
    def show_error(parent, message: str, duration: int = 3000):
        """Mostrar notificación de error"""
        NotificationManager._show_notification(parent, message, "#ef4444", duration)
    
    @staticmethod
    def show_warning(parent, message: str, duration: int = 3000):
        """Mostrar notificación de advertencia"""
        NotificationManager._show_notification(parent, message, "#f59e0b", duration)
    
    @staticmethod
    def show_info(parent, message: str, duration: int = 3000):
        """Mostrar notificación informativa"""
        NotificationManager._show_notification(parent, message, "#3b82f6", duration)
    
    @staticmethod
    def _show_notification(parent, message: str, color: str, duration: int):
        """Mostrar notificación con estilo"""
        notification = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=10
        )
        
        # Posicionar en la esquina superior derecha
        notification.place(relx=0.95, rely=0.05, anchor="ne")
        
        label = ctk.CTkLabel(
            notification,
            text=message,
            font=ctk.CTkFont(size=13),
            text_color="white"
        )
        label.pack(padx=20, pady=15)
        
        # Auto-ocultar después del duration
        def hide():
            try:
                notification.destroy()
            except:
                pass
        
        notification.after(duration, hide)
        
        # Efecto de entrada
        AnimationManager.fade_in(notification, duration=200)
