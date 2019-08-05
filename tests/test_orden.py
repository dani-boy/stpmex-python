from clabe import BANKS

from stpmex.orden import Orden


def test_registrar_orden(client):
    orden = Orden(
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

    x = client.registrar_orden(orden)
    import ipdb

    ipdb.set_trace()
