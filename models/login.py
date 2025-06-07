import hashlib
from models.usuario import Usuario

class Login:
    def __init__(self):
        self.usuario_actual = None
        self.password_hash = None

    def encriptar_contrasena(self, passwd):
        return hashlib.sha256(passwd.encode()).hexdigest()

    def inicio_de_sesion(self, email, password):
        usuario = Usuario.obtener_por_email(email)
        if usuario:
            password_enc = self.encriptar_contrasena(password)
            if password_enc == usuario.contrasena:
                self.usuario_actual = usuario
                self.password_hash = password_enc
                return True
        return False

    def cambiar_pass(self, vieja_pass, nueva_pass):
        if self.encriptar_contrasena(vieja_pass) == self.password_hash:
            nueva_pass_enc = self.encriptar_contrasena(nueva_pass)
            self.usuario_actual.contrasena = nueva_pass_enc
            self.password_hash = nueva_pass_enc
            return True
        else:
            return False

    def cambiar_nombre(self, nuevo_nombre):
        self.usuario_actual.nombre = nuevo_nombre
        return True

