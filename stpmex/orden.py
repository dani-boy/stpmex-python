import random
import time
from dataclasses import field
from typing import Optional

from pydantic import PositiveFloat, constr
from pydantic.dataclasses import dataclass

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
STP_BANK_CODE = '90646'


def truncated_str(length):
    return constr(strip_whitespace=True, min_length=1, curtail_length=length)


@dataclass
class Orden:
    nombreBeneficiario: truncated_str(39)
    cuentaBeneficiario: str  # TODO: validate
    institucionContraparte: str  # TODO: validate
    monto: PositiveFloat
    conceptoPago: truncated_str(39)

    institucionOperante: str = STP_BANK_CODE

    nombreOrdenante: Optional[truncated_str(39)] = None
    claveRastreo: truncated_str(29) = field(
        default_factory=lambda: f'CR{int(time.time())}'
    )
    referenciaNumerica: truncated_str(7) = field(
        default_factory=lambda: random.randint(10 ** 6, 10 ** 7)
    )
    rfcCurpBeneficiario: constr(max_length=18) = 'ND'
    rfcCurpOrdenante: Optional[constr(max_length=18)] = None
    tipoPago: constr(max_length=2) = '1'

    def __post_init__(self):
        if not isinstance(self.monto, float):
            raise ValueError('monto must be a float')

    @property
    def joined_fields(self):
        joined_fields = []
        for field in ORDEN_FIELDNAMES:
            value = getattr(self, field, None)
            if isinstance(value, float):
                value = f'{value:.2f}'
            joined_fields.append(str(value or ''))
        return ('||' + '|'.join(joined_fields) + '||').encode('utf-8')
