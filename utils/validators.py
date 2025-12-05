"""
Sistema de validación para formularios
"""

import re
from typing import Tuple, Optional


class Validator:
    """Clase para validaciones de campos"""
    
    @staticmethod
    def validate_dni(dni: str) -> Tuple[bool, Optional[str]]:
        """Validar DNI peruano (8 dígitos)"""
        if not dni:
            return False, "El DNI es obligatorio"
        
        if not dni.isdigit():
            return False, "Solo números"
        
        if len(dni) != 8:
            return False, "Debe tener 8 dígitos"
        
        return True, None
    
    @staticmethod
    def validate_nombre(nombre: str, campo: str = "nombre") -> Tuple[bool, Optional[str]]:
        """Validar nombre (solo letras y espacios)"""
        if not nombre:
            return False, f"El {campo} es obligatorio"
        
        if len(nombre) < 2:
            return False, f"Mínimo 2 caracteres"
        
        if len(nombre) > 50:
            return False, f"Máximo 50 caracteres"
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            return False, f"Solo letras"
        
        return True, None
    
    @staticmethod
    def validate_phone(telefono: str) -> Tuple[bool, Optional[str]]:
        """Validar teléfono peruano (9 dígitos, empieza con 9)"""
        if not telefono:
            return False, "El teléfono es obligatorio"
        
        # Eliminar espacios
        telefono = telefono.strip()
        
        if not telefono.isdigit():
            return False, "Solo números"
        
        if len(telefono) != 9:
            return False, "Debe tener 9 dígitos"
        
        if not telefono.startswith('9'):
            return False, "Debe comenzar con 9"
        
        return True, None
    
    @staticmethod
    def validate_telefono(telefono: str) -> Tuple[bool, Optional[str]]:
        """Alias para validate_phone"""
        return Validator.validate_phone(telefono)
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """Validar email"""
        if not email:
            return False, "El email es obligatorio"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Email inválido"
        
        return True, None
    
    @staticmethod
    def validate_direccion(direccion: str) -> Tuple[bool, Optional[str]]:
        """Validar dirección"""
        if not direccion:
            return False, "La dirección es obligatoria"
        
        if len(direccion) < 5:
            return False, "Mínimo 5 caracteres"
        
        if len(direccion) > 200:
            return False, "Máximo 200 caracteres"
        
        return True, None
    
    @staticmethod
    def validate_peso(peso: str) -> Tuple[bool, Optional[str]]:
        """Validar peso (número decimal positivo)"""
        if not peso:
            return False, "El peso es obligatorio"
        
        try:
            peso_float = float(peso)
            if peso_float <= 0:
                return False, "El peso debe ser mayor a 0"
            if peso_float > 200:
                return False, "El peso no puede exceder 200 kg"
            return True, None
        except ValueError:
            return False, "El peso debe ser un número válido"
    
    @staticmethod
    def validate_edad(anios: str, meses: str) -> Tuple[bool, Optional[str]]:
        """Validar edad (años y meses)"""
        if not anios and not meses:
            return False, "Debe ingresar al menos años o meses"
        
        try:
            if anios:
                anios_int = int(anios)
                if anios_int < 0 or anios_int > 50:
                    return False, "Los años deben estar entre 0 y 50"
            
            if meses:
                meses_int = int(meses)
                if meses_int < 0 or meses_int > 11:
                    return False, "Los meses deben estar entre 0 y 11"
            
            return True, None
        except ValueError:
            return False, "La edad debe contener números válidos"
    
    @staticmethod
    def validate_colegiatura(colegiatura: str) -> Tuple[bool, Optional[str]]:
        """Validar número de colegiatura"""
        if not colegiatura:
            return False, "La colegiatura es obligatoria"
        
        if len(colegiatura) < 5:
            return False, "La colegiatura debe tener al menos 5 caracteres"
        
        return True, None
    
    @staticmethod
    def validate_fecha(fecha: str) -> Tuple[bool, Optional[str]]:
        """Validar formato de fecha YYYY-MM-DD"""
        if not fecha:
            return False, "La fecha es obligatoria"
        
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, fecha):
            return False, "Formato de fecha inválido (use YYYY-MM-DD)"
        
        return True, None
    
    @staticmethod
    def validate_hora(hora: str) -> Tuple[bool, Optional[str]]:
        """Validar formato de hora HH:MM"""
        if not hora:
            return False, "La hora es obligatoria"
        
        pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
        if not re.match(pattern, hora):
            return False, "Formato de hora inválido (use HH:MM)"
        
        return True, None