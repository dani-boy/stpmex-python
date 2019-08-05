import pytest
from pydantic import ValidationError

from stpmex import Orden


ORDEN_KWARGS = dict(
    institucionContraparte='40072',
    claveRastreo='CR1564969083',
    monto=1.2,
    tipoPago=1,
    nombreOrdenante=None,
    cuentaOrdenante=None,
    tipoCuentaOrdenante=None,
    rfcCurpOrdenante=None,
    tipoCuentaBeneficiario=40,
    nombreBeneficiario='Ricardo Sanchez',
    cuentaBeneficiario='072691004495711499',
    rfcCurpBeneficiario='ND',
    conceptoPago='Prueba',
    referenciaNumerica=5273144,
    topologia='T',
    medioEntrega=3,
    prioridad=1,
    iva=None,
)


def test_empty_concepto():
    orden_kwargs = {**ORDEN_KWARGS, **dict(conceptoPago=' ')}
    with pytest.raises(ValidationError) as excinfo:
        Orden(**orden_kwargs)
    errors = excinfo.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('conceptoPago',)
    assert error['type'] == 'value_error.any_str.min_length'
