#!/usr/bin/env python3
"""
Script de inicio para el Sistema Veterinario
Ejecuta: python run.py
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal"""
    print("=" * 60)
    print("🐾 SISTEMA DE GESTIÓN VETERINARIA")
    print("=" * 60)
    print()
    
    # Verificar Python
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: Python {version.major}.{version.minor}.{version.micro}")
        print()
        print("   Descarga Python desde: https://www.python.org/downloads/")
        return 1
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detectado")
    
    # Verificar customtkinter
    try:
        import customtkinter
        print(f"✓ CustomTkinter instalado")
    except ImportError:
        print()
        print("❌ ERROR: CustomTkinter no está instalado")
        print()
        print("   Para instalar, ejecuta:")
        print("   pip install customtkinter")
        print()
        return 1
    
    print()
    print("Iniciando aplicación...")
    print()
    
    # Importar y ejecutar
    try:
        from main import main as app_main
        app_main()
    except Exception as e:
        print()
        print("❌ ERROR al iniciar la aplicación:")
        print(f"   {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
