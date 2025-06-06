import datetime
from models.usuario import Usuario

class Pedidos:
    _pedidos = []
    _movimientos = []
    _ultimo_id_pedido = 0

    @classmethod
    def ingresar_pedido(cls, id_usuario, descripcion):
        cls._ultimo_id_pedido += 1
        pedido = {
            'id_pedido': cls._ultimo_id_pedido,
            'id_usuario': id_usuario,
            'fecha': datetime.datetime.now(),
            'estado': 'Pendiente',
            'descripcion': descripcion
        }
        cls._pedidos.append(pedido)
        cls.registrar_movimiento(pedido['id_pedido'], 'Ingreso')
        return True

    @classmethod
    def listar_pedidos_usuario(cls, id_usuario):
        pedidos_usuario = [p for p in cls._pedidos if p['id_usuario'] == id_usuario]
        resultado = []
        for p in pedidos_usuario:
            usuario = Usuario.obtener_por_id(p['id_usuario'])
            resultado.append({
                'id_pedido': p['id_pedido'],
                'nombre': usuario.nombre if usuario else 'Desconocido',
                'fecha': p['fecha'].strftime('%d/%m/%y'),
                'estado': p['estado'],
                'descripcion': p['descripcion']
            })
        return resultado

    @classmethod
    def listar_pedidos_todos(cls):
        resultado = []
        for p in sorted(cls._pedidos, key=lambda x: x['fecha'], reverse=True):
            usuario = Usuario.obtener_por_id(p['id_usuario'])
            resultado.append({
                'id_pedido': p['id_pedido'],
                'nombre': usuario.nombre if usuario else 'Desconocido',
                'fecha': p['fecha'].strftime('%d/%m/%y'),
                'estado': p['estado'],
                'descripcion': p['descripcion']
            })
        return resultado

    @classmethod
    def despachar_pedido(cls, id_pedido, id_usuario=None):
        for pedido in cls._pedidos:
            if pedido['id_pedido'] == id_pedido and (id_usuario is None or pedido['id_usuario'] == id_usuario):
                if pedido['estado'] == 'Despachado':
                    print("[WARN] Pedido ya despachado.")
                    return False
                pedido['estado'] = 'Despachado'
                cls.registrar_movimiento(id_pedido, 'Despacho')
                return True
        print("[WARN] Pedido no encontrado o sin permisos.")
        return False

    @classmethod
    def registrar_movimiento(cls, id_pedido, tipo):
        movimiento = {
            'id_pedido': id_pedido,
            'tipo': tipo,
            'fecha': datetime.datetime.now()
        }
        cls._movimientos.append(movimiento)
        return True

