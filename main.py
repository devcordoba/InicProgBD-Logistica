from models.login import Login
from menu.menu import Menu
from models.comision import Comision
from models.usuario import Usuario
from utils.utils import validar_contrasena

if len(Usuario._usuarios) == 0:
    Usuario.registrar_usuario('Admin', 'admin@abc.com', 'admin', 'admin123')
    Usuario.registrar_usuario('Juan', 'juan@abc.com', 'usuario', 'user123')

def main():
    while True:
        login = Login()
        print("\n=== Sistema de gestión de comisiones (LogistiCom) ===")
        print("\n=== Iniciar sesión ===\n")
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()

        if login.inicio_de_sesion(email, password):
            menu = Menu(login)
            while True:
                menu.ver_menu()
                opcion = input("\nOpción: ").strip()
                if opcion == '0':
                    print("\nSaliendo del sistema ...")
                    break
                elif opcion == '1':
                    desc = input("\nDescripción de la comisión: ").strip()
                    if Comision.ingresar_comision(login.usuario_actual.id_usuario, desc):
                        print("\nComisión ingresada.")
                    else:
                        print("Error.")
                elif opcion == '2':
                    comision = Comision.listar_comisiones_usuario(login.usuario_actual.id_usuario)
                    for p in comision:
                        print(f"\nID: {p['id_comision']}, Usuario: {p['nombre']}, Fecha: {p['fecha']}, Estado: {p['estado']}, Descripción: {p['descripcion']}")
                elif opcion == '3':
                    nuevo = input("\nNuevo nombre: ").strip()
                    if login.cambiar_nombre(nuevo):
                        print("Nombre actualizado.\n")
                    else:
                        print("Error.")
                elif opcion == '4':
                    vieja = input("Contraseña actual: ").strip()

                    while True:
                        nueva = input("Nueva contraseña: ").strip()
                        if not validar_contrasena(nueva):
                            print("La contraseña debe tener al menos 6 caracteres, incluir letras y números.")
                            continue

                        nueva_confirm = input("Confirmar contraseña: ").strip()
                        if nueva != nueva_confirm:
                            print("Las contraseñas no coinciden. Intente de nuevo.")
                            continue

                        break

                    if login.cambiar_pass(vieja, nueva):
                        print("Contraseña actualizada.\n")
                    else:
                        print("Error: contraseña actual incorrecta.")
                elif opcion == '5' and login.usuario_actual.rol == 'admin':
                    menu.registrar_usuario_admin()
                elif opcion == '6' and login.usuario_actual.rol == 'admin':
                    todos = Comision.listar_comisiones_todos()
                    for p in todos:
                        print(f"\nID: {p['id_comision']}, Usuario: {p['nombre']}, Fecha: {p['fecha']}, Estado: {p['estado']}, Descripción: {p['descripcion']}")
                elif opcion == '7' and login.usuario_actual.rol == 'admin':
                    try:
                        idp = int(input("\nID de la comision a despachar: "))
                        if Comision.despachar_comision(idp):
                            print("\nDespachado correctamente.")
                        else:
                            print("Error.\n")
                    except ValueError:
                        print("ID inválido.\n")
                elif opcion == '8' and login.usuario_actual.rol == 'admin':
                    usuarios = Usuario.listar_todos()
                    print("\n=== Lista de usuarios ===")
                    for u in usuarios:
                        print(f"ID: {u['id_usuario']}, Nombre: {u['nombre']}, Email: {u['email']}, Rol: {u['rol']}")
                elif opcion == '9' and login.usuario_actual.rol == 'admin':
                    menu.cambiar_rol_usuario()

                elif opcion == '10' and login.usuario_actual.rol == 'admin':
                    menu.eliminar_usuario()
                else:
                    print("Opción no válida.\n")
        else:
            print("Credenciales incorrectas. Intente de nuevo.\n")

if __name__ == "__main__":
    main()

