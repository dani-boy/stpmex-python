import random
import time
import unicodedata
from dataclasses import field
from typing import ClassVar, Optional, Union

import clabe
from pydantic import PositiveFloat, conint, constr, validator
from pydantic.dataclasses import dataclass

from ..auth import ORDEN_FIELDNAMES, compute_signature, join_fields
from ..types import (
    Clabe,
    MXPhoneNumber,
    PaymentCardNumber,
    Prioridad,
    TipoCuenta,
    digits,
    truncated_str,
)
from .base import Resource

STP_BANK_CODE = '90646'


@dataclass
class Orden(Resource):
    """
    Base on:
    https://stpmex.zendesk.com/hc/es/articles/360002682851-RegistraOrden-Dispersi%C3%B3n-
    """

    _endpoint: ClassVar[str] = '/ordenPago'

    monto: PositiveFloat
    conceptoPago: truncated_str(39)

    cuentaBeneficiario: Union[Clabe, PaymentCardNumber, MXPhoneNumber]
    nombreBeneficiario: truncated_str(39)
    institucionContraparte: digits(5, 5)

    cuentaOrdenante: Clabe
    nombreOrdenante: Optional[truncated_str(39)] = None
    institucionOperante: digits(5, 5) = STP_BANK_CODE

    tipoCuentaBeneficiario: Optional[TipoCuenta] = None
    tipoCuentaOrdenante: TipoCuenta = TipoCuenta.clabe.value

    claveRastreo: truncated_str(29) = field(
        default_factory=lambda: f'CR{int(time.time())}'
    )
    referenciaNumerica: conint(gt=0, lt=10 ** 7) = field(
        default_factory=lambda: random.randint(10 ** 6, 10 ** 7)
    )
    rfcCurpBeneficiario: constr(max_length=18) = 'ND'
    rfcCurpOrdenante: Optional[constr(max_length=18)] = None

    prioridad: int = Prioridad.alta.value
    medioEntrega: int = 3
    tipoPago: int = 1
    topologia: str = 'T'
    iva: Optional[float] = None

    id: Optional[int] = None

    def __post_init__(self):
        # Test before Pydantic coerces it to a float
        if not isinstance(self.monto, float):
            raise ValueError('monto must be a float')
        cb = self.cuentaBeneficiario
        self.tipoCuentaBeneficiario = self.get_tipo_cuenta(cb)

    @classmethod
    def registra(cls, **kwargs) -> 'Orden':
        orden = cls(**kwargs)
        endpoint = orden._endpoint + '/registra'
        resp = orden._client.put(endpoint, orden.to_dict())
        orden.id = resp['id']
        return orden

    @property
    def firma(self) -> str:
        """
        Based on:
        https://stpmex.zendesk.com/hc/es/articles/360002796012-Firmas-Electr%C3%B3nicas-
        """
        joined_fields = join_fields(self, ORDEN_FIELDNAMES)
        return compute_signature(self._client.pkey, joined_fields)

    @staticmethod
    def get_tipo_cuenta(cuenta: str) -> Optional[TipoCuenta]:
        cuenta_len = len(cuenta)
        if cuenta_len == 18:
            tipo = TipoCuenta.clabe
        elif cuenta_len in {15, 16}:
            tipo = TipoCuenta.card
        elif cuenta_len == 10:
            tipo = TipoCuenta.phone_number
        else:
            tipo = None
        return tipo

    @validator('institucionContraparte')
    def _validate_institucion(cls, v: str) -> str:
        if v not in clabe.BANKS.values():
            raise ValueError(f'{v} no se corresponde a un banco')
        return v

    @validator(
        'nombreBeneficiario', 'nombreOrdenante', 'conceptoPago', each_item=True
    )
    def _unicode_to_ascii(cls, v):
        v = unicodedata.normalize('NFKD', v).encode('ascii', 'ignore')
        return v.decode('ascii')
