import random
import time

from stpmex import actualiza_client

from .base import Resource, STP_EMPRESA
from .types import AccountType, Prioridad


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
    empresa=STP_EMPRESA,
    rfcCurpBeneficiario='ND',
    tipoPago=1,
    tipoCuentaBeneficiario=AccountType.CLABE.value,
    topologia='T',
    medioEntrega=3,
    prioridad=Prioridad.alta.value,
    claveRastreo=lambda: f'CR{int(time.time())}',
    referenciaNumerica=lambda: random.randint(10 ** 6, 10 ** 7)
)


class Orden(Resource):

    __fieldnames__ = ORDEN_FIELDNAMES
    __type__ = actualiza_client.get_type('ns0:ordenPagoWS')
    _id = None
    _defaults = ORDEN_DEFAULTS
    _registra_method = actualiza_client.service.registraOrden

    def registra(self):
        resp = super(Orden, self).registra()
        self._id = resp.id
        return resp
