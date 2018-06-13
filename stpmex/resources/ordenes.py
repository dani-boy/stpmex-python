import random
import time

from stpmex.soap import client

from .base import Resource, STP_EMPRESA


ORDEN_FIELDNAMES = """
    institucionContraparte
    empresa
    fechaOperacion
    folioOrigen
    claveRastreo
    institucionOperante
    monto
    tipoPago
    tipoCuentaOrdenante
    nombreOrdenante
    cuentaOrdenante
    rfcCurpOrdenante
    tipoCuentaBeneficiario
    nombreBeneficiario
    cuentaBeneficiario
    rfcCurpBeneficiario
    emailBeneficiario
    tipoCuentaBeneficiario2
    nombreBeneficiario2
    cuentaBeneficiario2
    rfcCurpBeneficiario2
    conceptoPago
    conceptoPago2
    claveCatUsuario1
    claveCatUsuario2
    clavePago
    referenciaCobranza
    referenciaNumerica
    tipoOperacion
    topologia
    usuario
    medioEntrega
    prioridad
    iva
    """.split()


ORDEN_DEFAULTS = dict(
    institucionOperante=90646,
    empresa=STP_EMPRESA,
    rfcCurpBeneficiario='ND',
    tipoPago=1,
    tipoCuentaBeneficiario=40,
    topologia='T',
    medioEntrega=3,
    claveRastreo=lambda: f'CR{int(time.time())}',
    referenciaNumerica=lambda: random.randint(10 ** 6, 10 ** 7)
)


class Orden(Resource):

    __fieldnames__ = ORDEN_FIELDNAMES
    __type__ = client.get_type('ns0:ordenPagoWS')
    _registra_method = client.service.registraOrden

    def __init__(self, **kwargs):
        for default, value in ORDEN_DEFAULTS.items():
            if default not in kwargs:
                if callable(value):
                    kwargs[default] = value()
                else:
                    kwargs[default] = value
        super(Orden, self).__init__(**kwargs)
