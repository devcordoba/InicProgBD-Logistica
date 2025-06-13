from models.usuario import Usuario
from models.login import Login
from models.comision import Comision
from utils.utils import validar_contrasena

class Menu:
    def __init__(self, login: Login):
        self.login = login

    def cambiar_rol_usuario(self):
        print("\nCambiar rol de usuario")
        email = input("Email del usuario a modificar: ").strip()
        usuario = Usuario.obtener_por_email(email)
        if not usuario:
            print("Usuario no encontrado.")
            return

        nuevo_rol = input("Nuevo rol (admin/usuario): ").strip()
        if nuevo_rol not in ('admin', 'usuario'):
            print("Rol inválido.")
            return

        if Usuario.cambiar_rol(usuario.id_usuario, nuevo_rol):
            print("Rol cambiado correctamente.")
        else:
            print("Error al cambiar rol.")

    def eliminar_usuario(self):
        print("\nEliminar usuario")
        email = input("Email del usuario a eliminar: ").strip()
        usuario = Usuario.obtener_por_email(email)
        if not usuario:
            print("Usuario no encontrado.")
            return

        confirm = input(f"¿Seguro que desea eliminar al usuario {usuario.nombre} ({usuario.email})? (s/n): ").strip().lower()
        if confirm == 's':
            if Usuario.eliminar_usuario(usuario.id_usuario):
                print("Usuario eliminado correctamente.")
            else:
                print("Error al eliminar usuario.")
        else:
            print("Eliminación cancelada.")

    def registrar_usuario_admin(self):
        print("\nRegistrar nuevo usuario")
        nombre = input("Nombre: ").strip()
        email = input("Email: ").strip()
        rol = input("Rol (admin/usuario): ").strip()
        if rol not in ('admin', 'usuario'):
            print("Rol inválido.")
            return

        while True:
            password = input("Contraseña inicial: ").strip()
            if not validar_contrasena(password):
                print("La contraseña debe tener al menos 6 caracteres, incluir letras y números.")
                continue

            password_confirm = input("Confirmar contraseña: ").strip()
            if password != password_confirm:
                print("Las contraseñas no coinciden. Intente de nuevo.")
                continue

            break

        if Usuario.registrar_usuario(nombre, email, rol, password):
            print("Usuario registrado correctamente.")
        else:
            print("Error al registrar usuario.")

    def ver_menu(self):
        usuario = self.login.usuario_actual
        print(f"\nBienvenido/a, {usuario.nombre} ({usuario.rol})\n")
        print("1. Ingresar comision")
        print("2. Ver mis comisiones")
        print("3. Cambiar nombre")
        print("4. Cambiar contraseña")
        if usuario.rol == 'admin':
            print("\n====== Menu administrativo ======\n")
            print("5. Registrar nuevo usuario")
            print("6. Ver todos las comisiones")
            print("7. Despachar comisión")
            print("8. Ver todos los usuarios")
            print("9. Cambiar rol de usuario")
            print("10. Eliminar usuario")
            print("\n=================================\n")
        print("0. Salir")

