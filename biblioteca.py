import json
import os

def cargar_usuarios():
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json", "w") as file:
            json.dump({"usuarios": []}, file)  # Estructura vacía inicial
        return []

    with open("usuarios.json", "r") as file:
        try:
            data = json.load(file)
            usuarios = data.get("usuarios", [])
            return usuarios if isinstance(usuarios, list) and all(isinstance(u, dict) for u in usuarios) else []
        except json.JSONDecodeError:
            return []

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w") as file:
        json.dump({"usuarios": usuarios}, file, indent=4)

def usuario_existe(email, documento, usuarios):
    return any(isinstance(u, dict) and (u.get("email") == email or u.get("documento") == documento) for u in usuarios)

def registrar_usuario():
    usuarios = cargar_usuarios()

    email = input("Ingrese su email: ")
    password = input("Ingrese su password: ")
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    documento = input("Ingrese su número de documento: ")
    telefono = input("Ingrese su teléfono: ")
    rol = input("Ingrese su rol (admin/user): ").lower()

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

def mostrar_menu():
    print("\nBienvenido a la Biblioteca")
    print("1. Ingresar")
    print("2. Registrarse")
    print("3. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Función de ingreso aún no implementada.")
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

main() 
