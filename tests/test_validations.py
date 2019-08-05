import clabe
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


def create_orden(**kwargs) -> Orden:
    return Orden(**{**ORDEN_KWARGS, **kwargs})


def test_empty_concepto():
    with pytest.raises(ValidationError) as exc_info:
        create_orden(conceptoPago=' ')
    errors = exc_info.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('conceptoPago',)
    assert error['type'] == 'value_error.any_str.min_length'


def test_strip_spaces():
    orden = create_orden(conceptoPago=' hello ')
    assert orden.conceptoPago == 'hello'


def test_into_monto():
    with pytest.raises(ValueError):
        create_orden(monto=5)


def test_truncate_nombre_beneficiario():
    nombre = 'x' * 50
    orden = create_orden(nombreBeneficiario=nombre)
    assert len(orden.nombreBeneficiario) == 39


def test_invalid_clabe():
    invalid_clabe = '072691004495711490'
    assert not clabe.validate_clabe(invalid_clabe)
    with pytest.raises(ValidationError) as exc_info:
        create_orden(cuentaBeneficiario=invalid_clabe)
    errors = exc_info.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('cuentaBeneficiario',)
    assert error['type'] == 'value_error'


def test_wrong_length_cuentaBeneficiario():
    with pytest.raises(ValidationError) as exc_info:
        create_orden(cuentaBeneficiario='1' * 14)
    errors = exc_info.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('cuentaBeneficiario',)
    assert error['type'] == 'value_error'


def test_digits():
    with pytest.raises(ValidationError) as exc_info:
        create_orden(referenciaNumerica='9üey')
    errors = exc_info.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('referenciaNumerica',)
    assert error['type'] == 'value_error.str.regex'


def test_invalid_bank():
    with pytest.raises(ValidationError) as exc_info:
        create_orden(institucionContraparte='11111')
    errors = exc_info.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('institucionContraparte',)
    assert error['type'] == 'value_error'


def test_tipo_cuenta():
    with pytest.raises(ValidationError) as exc_info:
        create_orden(tipoCuentaBeneficiario=3)
    errors = exc_info.value.errors()
    assert len(errors) == 1
    error = errors[0]
    assert error['loc'] == ('tipoCuentaBeneficiario',)
    assert error['type'] == 'value_error'


def test_replace_unicode():
    orden = create_orden(
        nombreBeneficiario='Ricardo Sánchez', conceptoPago='está bien, güey'
    )
    assert orden.nombreBeneficiario == 'Ricardo Sanchez'
    assert orden.conceptoPago == 'esta bien, guey'
