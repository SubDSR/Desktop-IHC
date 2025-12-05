"""
Sistema de gestión de eventos y estado de la aplicación
"""

from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """Clase para representar un evento"""
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class EventManager:
    """Gestor central de eventos de la aplicación"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
    
    def subscribe(self, event_name: str, callback: Callable):
        """Suscribirse a un evento"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable):
        """Desuscribirse de un evento"""
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass
    
    def emit(self, event_name: str, data: Dict[str, Any] = None):
        """Emitir un evento"""
        event = Event(name=event_name, data=data or {})
        self._event_history.append(event)
        
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error en callback de evento {event_name}: {e}")
    
    def get_history(self, event_name: str = None) -> List[Event]:
        """Obtener historial de eventos"""
        if event_name:
            return [e for e in self._event_history if e.name == event_name]
        return self._event_history
    
    def clear_history(self):
        """Limpiar historial de eventos"""
        self._event_history.clear()


# Eventos predefinidos del sistema
class AppEvents:
    """Constantes para eventos de la aplicación"""
    
    # Navegación
    VIEW_CHANGED = "view_changed"
    
    # Clientes
    CLIENTE_ADDED = "cliente_added"
    CLIENTE_UPDATED = "cliente_updated"
    CLIENTE_DELETED = "cliente_deleted"
    CLIENTE_SELECTED = "cliente_selected"
    
    # Mascotas
    MASCOTA_ADDED = "mascota_added"
    MASCOTA_UPDATED = "mascota_updated"
    MASCOTA_DELETED = "mascota_deleted"
    MASCOTA_SELECTED = "mascota_selected"
    
    # Citas
    CITA_ADDED = "cita_added"
    CITA_UPDATED = "cita_updated"
    CITA_DELETED = "cita_deleted"
    CITA_SELECTED = "cita_selected"
    
    # Búsqueda y filtros
    SEARCH_CHANGED = "search_changed"
    FILTER_CHANGED = "filter_changed"
    
    # UI
    LOADING_START = "loading_start"
    LOADING_END = "loading_end"
    ERROR_OCCURRED = "error_occurred"
    SUCCESS_MESSAGE = "success_message"
    
    # Validación
    VALIDATION_ERROR = "validation_error"
    VALIDATION_SUCCESS = "validation_success"


class StateManager:
    """Gestor de estado global de la aplicación"""
    
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self._state: Dict[str, Any] = {
            "current_view": "dashboard",
            "selected_cliente": None,
            "selected_mascota": None,
            "selected_cita": None,
            "is_loading": False,
            "search_term": "",
            "active_filters": {},
            "user": {
                "name": "Recepcionista",
                "role": "recepcionista"
            }
        }
        self._state_history: List[Dict] = []
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtener valor del estado"""
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any, emit_event: bool = True):
        """Establecer valor en el estado"""
        old_value = self._state.get(key)
        self._state[key] = value
        
        # Guardar en historial
        self._state_history.append({
            "key": key,
            "old_value": old_value,
            "new_value": value,
            "timestamp": datetime.now()
        })
        
        # Emitir evento si es necesario
        if emit_event:
            self.event_manager.emit(
                f"state_changed:{key}",
                {"key": key, "value": value, "old_value": old_value}
            )
    
    def update(self, updates: Dict[str, Any], emit_event: bool = True):
        """Actualizar múltiples valores del estado"""
        for key, value in updates.items():
            self.set(key, value, emit_event)
    
    def get_all(self) -> Dict[str, Any]:
        """Obtener todo el estado"""
        return self._state.copy()
    
    def reset(self):
        """Resetear el estado a valores iniciales"""
        self._state = {
            "current_view": "dashboard",
            "selected_cliente": None,
            "selected_mascota": None,
            "selected_cita": None,
            "is_loading": False,
            "search_term": "",
            "active_filters": {},
            "user": {
                "name": "Recepcionista",
                "role": "recepcionista"
            }
        }
        self._state_history.clear()


class DataManager:
    """Gestor de datos con cache y sincronización"""
    
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self._cache: Dict[str, Any] = {}
        self._pending_changes: List[Dict] = []
    
    def get_cached(self, key: str) -> Any:
        """Obtener datos del cache"""
        return self._cache.get(key)
    
    def set_cache(self, key: str, data: Any):
        """Guardar datos en cache"""
        self._cache[key] = data
    
    def invalidate_cache(self, key: str = None):
        """Invalidar cache"""
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()
    
    def add_pending_change(self, change: Dict):
        """Agregar cambio pendiente (para sincronización futura)"""
        self._pending_changes.append(change)
        self.event_manager.emit("data_changed", {"change": change})
    
    def get_pending_changes(self) -> List[Dict]:
        """Obtener cambios pendientes"""
        return self._pending_changes.copy()
    
    def clear_pending_changes(self):
        """Limpiar cambios pendientes"""
        self._pending_changes.clear()


class UndoRedoManager:
    """Gestor de deshacer/rehacer"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self._undo_stack: List[Dict] = []
        self._redo_stack: List[Dict] = []
    
    def push(self, action: Dict):
        """Agregar acción al historial"""
        self._undo_stack.append(action)
        if len(self._undo_stack) > self.max_history:
            self._undo_stack.pop(0)
        
        # Limpiar redo stack cuando se hace una nueva acción
        self._redo_stack.clear()
    
    def undo(self) -> Dict:
        """Deshacer última acción"""
        if self._undo_stack:
            action = self._undo_stack.pop()
            self._redo_stack.append(action)
            return action
        return None
    
    def redo(self) -> Dict:
        """Rehacer última acción deshecha"""
        if self._redo_stack:
            action = self._redo_stack.pop()
            self._undo_stack.append(action)
            return action
        return None
    
    def can_undo(self) -> bool:
        """Verificar si se puede deshacer"""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Verificar si se puede rehacer"""
        return len(self._redo_stack) > 0
    
    def clear(self):
        """Limpiar historial"""
        self._undo_stack.clear()
        self._redo_stack.clear()


class AppContext:
    """Contexto global de la aplicación"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.event_manager = EventManager()
        self.state_manager = StateManager(self.event_manager)
        self.data_manager = DataManager(self.event_manager)
        self.undo_redo_manager = UndoRedoManager()
        
        self._initialized = True
    
    def reset(self):
        """Resetear todo el contexto"""
        self.event_manager.clear_history()
        self.state_manager.reset()
        self.data_manager.invalidate_cache()
        self.data_manager.clear_pending_changes()
        self.undo_redo_manager.clear()
