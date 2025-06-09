import hashlib

class Usuario:
    _usuarios = []
    _ultimo_id = 0

    def __init__(self, id_usuario, nombre, email, rol, contrasena_hash=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.contrasena = contrasena_hash

    @classmethod
    def registrar_usuario(cls, nombre, email, rol, password):
        if any(u.email == email for u in cls._usuarios):
            print("[ERROR] El email ya está registrado.")
            return False
        cls._ultimo_id += 1
        password_enc = hashlib.sha256(password.encode()).hexdigest()
        nuevo_usuario = Usuario(cls._ultimo_id, nombre, email, rol, password_enc)
        cls._usuarios.append(nuevo_usuario)
        return True

    @classmethod
    def listar_todos(cls):
        return [
            {
                'id_usuario': u.id_usuario,
                'nombre': u.nombre,
                'email': u.email,
                'rol': u.rol
            }
            for u in cls._usuarios
        ]

    @classmethod
    def obtener_por_email(cls, email):
        for u in cls._usuarios:
            if u.email == email:
                return u
        return None

    @classmethod
    def obtener_por_id(cls, id_usuario):
        for u in cls._usuarios:
            if u.id_usuario == id_usuario:
                return u
        return None

    @classmethod
    def cambiar_rol(cls, id_usuario, nuevo_rol):
        usuario = cls.obtener_por_id(id_usuario)
        if usuario:
            usuario.rol = nuevo_rol
            return True
        return False

    @classmethod
    def eliminar_usuario(cls, id_usuario):
        usuario = cls.obtener_por_id(id_usuario)
        if usuario:
            cls._usuarios.remove(usuario)
            return True
        return False