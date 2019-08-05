import random
import time
from dataclasses import field
from typing import Optional

import clabe
from pydantic import constr, PositiveFloat, validator
from pydantic.dataclasses import dataclass

from .types import Prioridad, TipoCuenta

STP_BANK_CODE = '90646'


def truncated_str(length):
    return constr(strip_whitespace=True, min_length=1, curtail_length=length)


def digits(min_length: Optional[int] = None, max_length: Optional[int] = None):
    return constr(regex=r'^\d+$', min_length=min_length, max_length=max_length)


@dataclass
class Orden:
    nombreBeneficiario: truncated_str(39)
    cuentaBeneficiario: digits(10, 19)
    institucionContraparte: digits(5, 5)
    tipoCuentaBeneficiario: int
    monto: PositiveFloat
    conceptoPago: truncated_str(39)

    nombreOrdenante: Optional[truncated_str(39)] = None
    cuentaOrdenante: Optional[str] = None
    tipoCuentaOrdenante: Optional[int] = None

    claveRastreo: truncated_str(29) = field(
        default_factory=lambda: f'CR{int(time.time())}'
    )
    referenciaNumerica: digits(1, 7) = field(
        default_factory=lambda: random.randint(10 ** 6, 10 ** 7)
    )
    rfcCurpBeneficiario: constr(max_length=18) = 'ND'
    rfcCurpOrdenante: Optional[constr(max_length=18)] = None
    medioEntrega: int = 3
    prioridad: int = Prioridad.alta.value
    tipoPago: int = 1
    topologia: str = 'T'
    iva: Optional[float] = None
    institucionOperante: str = STP_BANK_CODE

    def __post_init__(self):
        # Test before Pydantic coerces it to a float
        if not isinstance(self.monto, float):
            raise ValueError('monto must be a float')

    @validator('cuentaBeneficiario')
    def __validate_cuentaBeneficiario(cls, v):
        if len(v) == 10:
            pass  # phone number
        elif len(v) in {15, 16}:
            pass  # card
        elif len(v) == 18:
            if not clabe.validate_clabe(v):
                raise ValueError('cuentaBeneficiario no es una válida CLABE')
        else:
            raise ValueError('cuentaBeneficiario no es válida')


    @validator('institucionContraparte')
    def __validate_institucionContraparte(cls, v):
        if v not in clabe.BANKS.values():
            raise ValueError(f'{v} no se corresponde a un banco')
