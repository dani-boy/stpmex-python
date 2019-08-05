from clabe import BANKS

from stpmex.orden import Orden


def test_orden(client):
    orden = Orden(
        conceptoPago='Prueba',
        cuentaBeneficiario='072691004495711499',
        institucionContraparte=BANKS['072'],
        monto=1.2,
        nombreBeneficiario='Ricardo Sanchez',
    )
    x = client.registrar_orden(orden)
    import ipdb; ipdb.set_trace()
