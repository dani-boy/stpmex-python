import random
import time
from dataclasses import field
from typing import Optional

from pydantic import PositiveFloat, constr
from pydantic.dataclasses import dataclass

STP_BANK_CODE = '90646'


def truncated_str(length):
    return constr(strip_whitespace=True, min_length=1, curtail_length=length)


@dataclass
class Orden:
    nombreBeneficiario: truncated_str(39)
    cuentaBeneficiario: str  # TODO: validate
    institucionContraparte: str  # TODO: validate
    tipoCuentaBeneficiario: int
    monto: PositiveFloat
    conceptoPago: truncated_str(39)

    nombreOrdenante: Optional[truncated_str(39)] = None
    cuentaOrdenante: Optional[str] = None
    tipoCuentaOrdenante: Optional[int] = None

    claveRastreo: truncated_str(29) = field(
        default_factory=lambda: f'CR{int(time.time())}'
    )
    referenciaNumerica: truncated_str(7) = field(
        default_factory=lambda: random.randint(10 ** 6, 10 ** 7)
    )
    rfcCurpBeneficiario: constr(max_length=18) = 'ND'
    rfcCurpOrdenante: Optional[constr(max_length=18)] = None
    medioEntrega: int = 3
    prioridad: int = 1
    tipoPago: int = 1
    topologia: str = 'T'
    iva: Optional[float] = None
    institucionOperante: str = STP_BANK_CODE

    def __post_init__(self):
        if not isinstance(self.monto, float):
            raise ValueError('monto must be a float')
