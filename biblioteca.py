import json
import os

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

def menu_usuario(usuario):
    """Menú para usuarios después de iniciar sesión."""
    while True:
        print(f"\nBienvenido, {usuario['nombre']} {usuario['apellido']}!")
        print("1. Ver perfil")
        print("2. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            print("\n--- Perfil de Usuario ---")
            for key, value in usuario.items():
                print(f"{key.capitalize()}: {value}")
        elif opcion == "2":
            print("Cerrando sesión...\n")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def ingresar_usuario():
    usuarios = cargar_usuarios()

    email = input("Ingrese su email: ").strip().lower()
    password = input("Ingrese su password: ").strip()

    for usuario in usuarios:
        if usuario.get("email").lower() == email and usuario.get("password") == password:
            menu_usuario(usuario)  # Muestra el nuevo menú después del login
            return
    
    print("Email o password incorrectos.")

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
