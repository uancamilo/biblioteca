import json
import os
from datetime import datetime, timedelta

# -------------------- FUNCIONES PARA MANEJO DE USUARIOS --------------------

def cargar_usuarios():
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json", "w", encoding="utf-8") as file:
            json.dump({"usuarios": []}, file, indent=4)
        return []

    with open("usuarios.json", "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            usuarios = data.get("usuarios", [])
            return usuarios if isinstance(usuarios, list) and all(isinstance(u, dict) for u in usuarios) else []
        except json.JSONDecodeError:
            return []

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w", encoding="utf-8") as file:
        json.dump({"usuarios": usuarios}, file, indent=4)

def usuario_existe(email, documento, usuarios):
    email = email.lower()
    return any(isinstance(u, dict) and (u.get("email").lower() == email or u.get("documento") == documento) for u in usuarios)

def registrar_usuario():
    usuarios = cargar_usuarios()

    email = input("Ingrese su email: ").strip().lower()
    password = input("Ingrese su password: ").strip()
    nombre = input("Ingrese su nombre: ").strip()
    apellido = input("Ingrese su apellido: ").strip()
    documento = input("Ingrese su número de documento: ").strip()
    telefono = input("Ingrese su teléfono: ").strip()
    rol = input("Ingrese su rol (admin/user): ").strip().lower()

    if rol not in ["admin", "user"]:
        print("Rol no válido.")
        return
    
    if usuario_existe(email, documento, usuarios):
        print("El usuario o el documento ya están registrados.")
        return
    
    nuevo_usuario = {
        "email": email,
        "password": password,
        "rol": rol,
        "nombre": nombre,
        "apellido": apellido,
        "documento": documento,
        "telefono": telefono
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    print("Usuario registrado con éxito.")

# -------------------- FUNCIONES PARA MANEJO DE LIBROS --------------------

def cargar_libros():
    """Carga los libros desde libros.json"""
    if not os.path.exists("libros.json"):
        with open("libros.json", "w", encoding="utf-8") as file:
            json.dump({"libros": []}, file, indent=4)
        return []
    
    with open("libros.json", "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data.get("libros", [])
        except json.JSONDecodeError:
            return []

def guardar_libros(libros):
    """Guarda los libros en libros.json"""
    with open("libros.json", "w", encoding="utf-8") as file:
        json.dump({"libros": libros}, file, indent=4, ensure_ascii=False)

def crear_libro(usuario):
    """Permite a un usuario admin registrar un nuevo libro."""
    if usuario["rol"] != "admin":
        print("No tienes permisos para agregar libros.")
        return

    libros = cargar_libros()

    titulo = input("Ingrese el título del libro: ").strip()
    autor = input("Ingrese el autor del libro: ").strip()
    isbn = input("Ingrese el ISBN del libro: ").strip()
    
    nuevo_libro = {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn
    }

    libros.append(nuevo_libro)
    guardar_libros(libros)
    print("Libro agregado con éxito.")

# -------------------- FUNCIONES PARA MANEJO DE PRÉSTAMOS --------------------

def cargar_libros():
    """Carga los libros disponibles desde libros.json"""
    if not os.path.exists("libros.json"):
        return []
    
    with open("libros.json", "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data.get("libros", [])
        except json.JSONDecodeError:
            return []

def guardar_prestamos(prestamos):
    with open("prestamos.json", "w", encoding="utf-8") as file:
        json.dump({"prestamos": prestamos}, file, indent=4, ensure_ascii=False)

def cargar_prestamos():
    if not os.path.exists("prestamos.json"):
        return []
    with open("prestamos.json", "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data.get("prestamos", [])
        except json.JSONDecodeError:
            return []

def crear_prestamo(usuario):
    """Permite a un usuario 'user' crear un préstamo con un libro disponible"""
    if usuario.get("rol") != "user":
        print("Solo los usuarios con rol 'user' pueden realizar préstamos.")
        return
    
    libros = cargar_libros()
    if not libros:
        print("No hay libros disponibles para préstamo.")
        return

    print("\nLibros disponibles:")
    for idx, libro in enumerate(libros, start=1):
        print(f"{idx}. {libro['titulo']} - {libro['autor']}")

    try:
        opcion = int(input("Seleccione el número del libro que desea prestar: "))
        if opcion < 1 or opcion > len(libros):
            print("Opción inválida.")
            return
    except ValueError:
        print("Ingrese un número válido.")
        return

    libro_seleccionado = libros[opcion - 1]

    fecha_creacion = datetime.today().strftime("%Y-%m-%d")
    fecha_devolucion = (datetime.today() + timedelta(days=6)).strftime("%Y-%m-%d")

    # Cargar préstamos existentes
    prestamos = cargar_prestamos()
    
    # Obtener el próximo ID
    nuevo_id = max((p.get("id", 0) for p in prestamos), default=0) + 1

    nuevo_prestamo = {
        "id": nuevo_id,
        "usuario": usuario["email"],
        "nombre": usuario["nombre"],
        "apellido": usuario["apellido"],
        "libro": libro_seleccionado["titulo"],
        "autor": libro_seleccionado["autor"],
        "fecha_prestamo": fecha_creacion,
        "fecha_devolucion": fecha_devolucion
    }

    prestamos.append(nuevo_prestamo)
    guardar_prestamos(prestamos)

    print(f"\n✅ Préstamo registrado con éxito. ID: {nuevo_id}")
    print(f"📅 Fecha de préstamo: {fecha_creacion}")
    print(f"📅 Fecha de devolución: {fecha_devolucion}")



# -------------------- MENÚ PARA USUARIOS --------------------

def menu_usuario(usuario):
    """Menú para usuarios después de iniciar sesión."""
    while True:
        print(f"\nBienvenido, {usuario['nombre']} {usuario['apellido']}!")
        print("1. Ver perfil")
        if usuario["rol"] == "admin":
            print("2. Agregar un libro")
        elif usuario["rol"] == "user":
            print("2. Solicitar préstamo")
        print("3. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            print("\n--- Perfil de Usuario ---")
            for key, value in usuario.items():
                print(f"{key.capitalize()}: {value}")
        elif opcion == "2" and usuario["rol"] == "admin":
            crear_libro(usuario)
        elif opcion == "2" and usuario["rol"] == "user":
            crear_prestamo(usuario)
        elif opcion == "3":
            print("Cerrando sesión...\n")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# -------------------- FUNCIÓN PARA INGRESAR --------------------

def ingresar_usuario():
    usuarios = cargar_usuarios()

    email = input("Ingrese su email: ").strip().lower()
    password = input("Ingrese su password: ").strip()

    for usuario in usuarios:
        if usuario.get("email").lower() == email and usuario.get("password") == password:
            menu_usuario(usuario) 
            return
    
    print("Email o password incorrectos.")

# -------------------- MENÚ PRINCIPAL --------------------

def mostrar_menu():
    print("\nBienvenido a la Biblioteca")
    print("1. Ingresar")
    print("2. Registrarse")
    print("3. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ingresar_usuario()
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

main()