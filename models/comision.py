import datetime
from models.usuario import Usuario

class Comision:
    _comisiones = []
    _ultimo_id_comision = 0

    @classmethod
    def ingresar_comision(cls, id_usuario, descripcion):
        cls._ultimo_id_comision += 1
        comision = {
            'id_comision': cls._ultimo_id_comision,
            'id_usuario': id_usuario,
            'fecha': datetime.datetime.now(),
            'estado': 'Pendiente',
            'descripcion': descripcion
        }
        cls._comisiones.append(comision)
        return True

    @classmethod
    def listar_comisiones_usuario(cls, id_usuario):
        comisiones_usuario = [p for p in cls._comisiones if p['id_usuario'] == id_usuario]
        resultado = []
        for p in comisiones_usuario:
            usuario = Usuario.obtener_por_id(p['id_usuario'])
            resultado.append({
                'id_comision': p['id_comision'],
                'nombre': usuario.nombre if usuario else 'Desconocido',
                'fecha': p['fecha'].strftime('%d/%m/%y'),
                'estado': p['estado'],
                'descripcion': p['descripcion']
            })
        return resultado

    @classmethod
    def listar_comisiones_todos(cls):
        resultado = []
        for p in sorted(cls._comisiones, key=lambda x: x['fecha'], reverse=True):
            usuario = Usuario.obtener_por_id(p['id_usuario'])
            resultado.append({
                'id_comision': p['id_comision'],
                'nombre': usuario.nombre if usuario else 'Desconocido',
                'fecha': p['fecha'].strftime('%d/%m/%y'),
                'estado': p['estado'],
                'descripcion': p['descripcion']
            })
        return resultado

    @classmethod
    def despachar_comision(cls, id_comision, id_usuario=None):
        for comision in cls._comisiones:
            if comision['id_comision'] == id_comision and (id_usuario is None or comision['id_usuario'] == id_usuario):
                if comision['estado'] == 'Despachado':
                    print("[WARN] Comisión ya despachada.")
                    return False
                comision['estado'] = 'Despachado'
                return True
        print("[WARN] Comisión no encontrada o sin permisos.")
        return False

