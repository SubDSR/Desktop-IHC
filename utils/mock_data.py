"""
Datos de prueba para la aplicación
"""

# Clientes
CLIENTES = [
    {
        "id": 1,
        "dni": "12345678",
        "nombres": "Juan",
        "apellidos": "Pérez García",
        "telefono": "987654321",
        "email": "juan.perez@email.com",
        "direccion": "Av. Principal 123, Lima",
        "estado": "Activo"
    },
    {
        "id": 2,
        "dni": "87654321",
        "nombres": "María",
        "apellidos": "López Silva",
        "telefono": "912345678",
        "email": "maria.lopez@email.com",
        "direccion": "Jr. Los Olivos 456, San Isidro",
        "estado": "Activo"
    },
    {
        "id": 3,
        "dni": "45678912",
        "nombres": "Carlos",
        "apellidos": "Mendoza Ruiz",
        "telefono": "965432178",
        "email": "carlos.mendoza@email.com",
        "direccion": "Calle Las Flores 789, Miraflores",
        "estado": "Activo"
    },
    {
        "id": 4,
        "dni": "78912345",
        "nombres": "Ana",
        "apellidos": "Torres Vega",
        "telefono": "923456789",
        "email": "ana.torres@email.com",
        "direccion": "Av. Arequipa 321, Lima",
        "estado": "Activo"
    },
    {
        "id": 5,
        "dni": "32165498",
        "nombres": "Roberto",
        "apellidos": "Sánchez Castro",
        "telefono": "987123456",
        "email": "roberto.sanchez@email.com",
        "direccion": "Jr. Huancayo 654, Surco",
        "estado": "Activo"
    },
    {
        "id": 6,
        "dni": "11223344",
        "nombres": "Lucia",
        "apellidos": "Flores Ramos",
        "telefono": "999888777",
        "email": "lucia.flores@email.com",
        "direccion": "Av. Larco 888, Miraflores",
        "estado": "Inactivo"
    }
]

# Mascotas
MASCOTAS = [
    {
        "id_mascota": 1,
        "id_cliente": 1,
        "nombre_mascota": "Max",
        "especie": "Perro",
        "raza": "Labrador",
        "sexo": "Macho",
        "edad_años": 3,
        "edad_meses": 6,
        "peso_kg": 28.5,
        "color_pelaje": "Dorado",
        "estado": "Activo"
    },
    {
        "id_mascota": 2,
        "id_cliente": 2,
        "nombre_mascota": "Luna",
        "especie": "Gato",
        "raza": "Siamés",
        "sexo": "Hembra",
        "edad_años": 2,
        "edad_meses": 3,
        "peso_kg": 4.2,
        "color_pelaje": "Crema con puntos oscuros",
        "estado": "Activo"
    },
    {
        "id_mascota": 3,
        "id_cliente": 3,
        "nombre_mascota": "Rocky",
        "especie": "Perro",
        "raza": "Pastor Alemán",
        "sexo": "Macho",
        "edad_años": 4,
        "edad_meses": 2,
        "peso_kg": 35.0,
        "color_pelaje": "Negro y marrón",
        "estado": "Activo"
    },
    {
        "id_mascota": 4,
        "id_cliente": 4,
        "nombre_mascota": "Michi",
        "especie": "Gato",
        "raza": "Persa",
        "sexo": "Hembra",
        "edad_años": 1,
        "edad_meses": 8,
        "peso_kg": 3.8,
        "color_pelaje": "Blanco",
        "estado": "Activo"
    },
    {
        "id_mascota": 5,
        "id_cliente": 5,
        "nombre_mascota": "Toby",
        "especie": "Perro",
        "raza": "Beagle",
        "sexo": "Macho",
        "edad_años": 2,
        "edad_meses": 0,
        "peso_kg": 12.5,
        "color_pelaje": "Tricolor",
        "estado": "Activo"
    },
    {
        "id_mascota": 6,
        "id_cliente": 1,
        "nombre_mascota": "Bella",
        "especie": "Perro",
        "raza": "Golden Retriever",
        "sexo": "Hembra",
        "edad_años": 5,
        "edad_meses": 1,
        "peso_kg": 30.0,
        "color_pelaje": "Dorado claro",
        "estado": "Activo"
    }
]

# Veterinarios
VETERINARIOS = [
    {
        "id": 1,
        "nombres": "Pedro",
        "apellidos": "Ramírez López",
        "dni": "98765432",
        "telefono": "987111222",
        "email": "pedro.ramirez@vetclinic.com",
        "especialidad": "Medicina General",
        "num_colegiatura": "CMP-12345",
        "estado": "Activo"
    },
    {
        "id": 2,
        "nombres": "Carmen",
        "apellidos": "Gonzales Díaz",
        "dni": "87654321",
        "telefono": "987222333",
        "email": "carmen.gonzales@vetclinic.com",
        "especialidad": "Cirugía",
        "num_colegiatura": "CMP-23456",
        "estado": "Activo"
    },
    {
        "id": 3,
        "nombres": "Miguel",
        "apellidos": "Torres Vega",
        "dni": "76543210",
        "telefono": "987333444",
        "email": "miguel.torres@vetclinic.com",
        "especialidad": "Dermatología",
        "num_colegiatura": "CMP-34567",
        "estado": "Activo"
    }
]

# Citas
CITAS = [
    {
        "id_cita": 1,
        "fecha": "2024-12-06",
        "hora": "09:00",
        "id_mascota": 1,
        "id_veterinario": 1,
        "motivo": "Consulta general y vacunación",
        "observaciones": "Revisar peso y aplicar vacuna antirrábica",
        "estado": "Programada"
    },
    {
        "id_cita": 2,
        "fecha": "2024-12-06",
        "hora": "10:30",
        "id_mascota": 2,
        "id_veterinario": 2,
        "motivo": "Control post-operatorio",
        "observaciones": "Revisión de sutura",
        "estado": "Programada"
    },
    {
        "id_cita": 3,
        "fecha": "2024-12-06",
        "hora": "11:00",
        "id_mascota": 3,
        "id_veterinario": 1,
        "motivo": "Consulta por cojera",
        "observaciones": "Revisión de pata derecha trasera",
        "estado": "Programada"
    },
    {
        "id_cita": 4,
        "fecha": "2024-12-05",
        "hora": "14:00",
        "id_mascota": 4,
        "id_veterinario": 3,
        "motivo": "Dermatología - Revisión de piel",
        "observaciones": "Problema de alergia",
        "estado": "Atendida"
    },
    {
        "id_cita": 5,
        "fecha": "2024-12-04",
        "hora": "09:30",
        "id_mascota": 5,
        "id_veterinario": 1,
        "motivo": "Vacunación múltiple",
        "observaciones": "Vacunas sextuple",
        "estado": "Atendida"
    },
    {
        "id_cita": 6,
        "fecha": "2024-12-03",
        "hora": "16:00",
        "id_mascota": 6,
        "id_veterinario": 2,
        "motivo": "Esterilización",
        "observaciones": "Cirugía programada cancelada por cliente",
        "estado": "Cancelada"
    }
]


# Funciones auxiliares
def get_cliente_by_id(cliente_id):
    """Obtener cliente por ID"""
    for cliente in CLIENTES:
        if cliente['id'] == cliente_id:
            return cliente
    return None


def get_mascota_by_id(mascota_id):
    """Obtener mascota por ID"""
    for mascota in MASCOTAS:
        if mascota['id_mascota'] == mascota_id:
            return mascota
    return None


def get_veterinario_by_id(vet_id):
    """Obtener veterinario por ID"""
    for vet in VETERINARIOS:
        if vet['id'] == vet_id:
            return vet
    return None


def get_mascotas_by_cliente(cliente_id):
    """Obtener mascotas de un cliente"""
    return [m for m in MASCOTAS if m['id_cliente'] == cliente_id]


def get_nombre_completo_cliente(cliente_id):
    """Obtener nombre completo del cliente"""
    cliente = get_cliente_by_id(cliente_id)
    if cliente:
        return f"{cliente['nombres']} {cliente['apellidos']}"
    return "N/A"


def get_citas_by_mascota(mascota_id):
    """Obtener citas de una mascota"""
    return [c for c in CITAS if c['id_mascota'] == mascota_id]


def get_citas_by_veterinario(vet_id):
    """Obtener citas de un veterinario"""
    return [c for c in CITAS if c['id_veterinario'] == vet_id]
