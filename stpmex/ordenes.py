import random
import time

from .base import ACTUALIZA_CLIENT, Resource, STP_EMPRESA
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
    __type__ = ACTUALIZA_CLIENT.get_type('ns0:ordenPagoWS')
    _id = None
    _defaults = ORDEN_DEFAULTS

    def registra(self):
        self.firma = self._compute_signature()
        resp = ACTUALIZA_CLIENT.service.registraOrden(self.__object__)
        self._id = resp.id
        return resp
