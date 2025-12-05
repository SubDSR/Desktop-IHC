# 🐾 Sistema Veterinario - Desktop

## 🚀 Instalación

### Opción 1: Usando run.py (Recomendado)

```bash
pip install customtkinter
python run.py
```

El script `run.py` verificará automáticamente:
- ✓ Versión de Python (requiere 3.8+)
- ✓ CustomTkinter instalado
- ✓ Mostrará mensajes de error claros si falta algo

### Opción 2: Directo con main.py

```bash
pip install customtkinter
python main.py
```

## ✨ Funcionalidades

### ✅ Lo que SÍ funciona:

1. **Clientes (CRUD Completo)**
   - ➕ Agregar cliente con validación
   - 👁️ Ver detalles
   - ✏️ Editar información
   - 🗑️ Eliminar cliente
   - 🔍 Buscar por DNI o nombre
   - Filtrar por estado (Activo/Inactivo)

2. **Mascotas (CRUD Completo)**
   - ➕ Registrar mascota
   - 👁️ Ver información completa
   - ✏️ Modificar datos
   - 🗑️ Eliminar mascota
   - 🔍 Buscar por nombre
   - Filtrar por especie

3. **Citas (CRUD Completo + Drag & Drop)**
   - ➕ Agendar nueva cita
   - 👁️ Ver detalles de la cita
   - ✏️ Modificar cita
   - 🗑️ Cancelar cita
   - 🔍 Buscar
   - Filtrar por estado
   - **🎨 Drag & Drop**: Arrastra las filas para reorganizar prioridades

4. **Veterinarios (Solo lectura)**
   - 👁️ Ver lista de veterinarios
   - 🔍 Buscar
   - Filtrar por especialidad

5. **Dashboard**
   - Estadísticas generales
   - Tarjetas de resumen

## 🎨 Características

- **Validación en formularios**: Los campos se validan al enviar
- **Notificaciones**: Mensajes de éxito/error en esquina superior derecha
- **Drag & Drop**: En Citas puedes arrastrar filas para reorganizar
- **Búsqueda en tiempo real**: Busca mientras escribes
- **Filtros**: Filtra por estado, especie, etc.
- **Diseño moderno**: Interfaz limpia con CustomTkinter

## 🎯 Cómo usar Drag & Drop

1. Ve a **Citas**
2. **Haz clic** sobre una fila y **mantén presionado**
3. **Arrastra** hacia arriba o abajo
4. **Suelta** para reorganizar
5. Verás una notificación confirmando el cambio

## 📝 Notas

- Los datos son de ejemplo (mock data)
- No usa base de datos
- Perfecto para demos y prototipos

## 🐛 Problemas comunes

**"ModuleNotFoundError: customtkinter"**
```bash
pip install customtkinter
```

**"La ventana no abre"**
- Asegúrate de tener Python 3.8+
- Verifica que customtkinter esté instalado

## 📦 Estructura

```
veterinaria_desktop_enhanced/
├── main.py                          # Aplicación principal
├── utils/
│   ├── animations.py                # Notificaciones y animaciones
│   ├── event_manager.py             # Sistema de eventos
│   ├── mock_data.py                 # Datos de ejemplo
│   ├── theme.py                     # Colores y estilos
│   └── validators.py                # Validadores de campos
└── views/
    ├── dashboard_view.py            # Vista del dashboard
    ├── clientes_view_simple.py      # (integrado en main.py)
    ├── mascotas_view_simple.py      # Vista de mascotas
    ├── citas_view_simple.py         # Vista de citas
    ├── veterinarios_view.py         # Vista de veterinarios
    └── components/
        ├── cliente_form_simple.py   # Formulario de cliente
        └── data_table.py            # Componente de tabla
```

## ✅ Checklist de Pruebas

- [ ] Instalar customtkinter
- [ ] Ejecutar `python main.py`
- [ ] Ir a Clientes → Ver botón verde "➕ Nuevo Cliente"
- [ ] Crear un cliente → Ver notificación verde
- [ ] Ir a Mascotas → Ver botón verde "➕ Nueva Mascota"
- [ ] Crear una mascota → Ver notificación verde
- [ ] Ir a Citas → Ver botón morado "➕ Nueva Cita"
- [ ] Crear una cita → Ver notificación verde
- [ ] Arrastar una fila en Citas → Ver notificación de reordenamiento

**Si todo funciona → ¡Listo!** ✅

---

**Versión**: 2.0 Simplificada
**Última actualización**: Diciembre 2024
