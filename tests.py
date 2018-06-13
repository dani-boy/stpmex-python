from stpmex import Orden


def test_join_fields():
    orden = Orden(
        institucionContraparte='846',
        empresa='STP',
        fechaOperacion='20160810',
        folioOrigen='1q2w33e',
        claveRastreo='1q2w33e',
        monto='121.00',
        tipoPago='1',
        tipoCuentaOrdenante='40',
        tipoCuentaBeneficiario='40',
        nombreBeneficiario='eduardo',
        cuentaBeneficiario='846180000300000004',
        rfcCurpBeneficiario=' ND',
        emailBeneficiario='fernanda.cedillo@stpmex.com',
        conceptoPago='pago prueba',
        referenciaNumerica='123123',
        topologia='T',
        medioEntrega='3',
        prioridad='0'
    )
    joined = ('||846|STP|20160810|1q2w33e|1q2w33e|90646|121.00|1|40||||40|'
              'eduardo|846180000300000004| ND|fernanda.cedillo@stpmex.com|||||'
              'pago prueba||||||123123||T||3|0|||').encode('utf-8')

    assert orden._joined_fields == joined


def test_create_orden():
    orden = Orden(
        conceptoPago='concepto',
        cuentaBeneficiario='846180000400000001',
        institucionContraparte=846,
        monto=1234,
        nombreBeneficiario='Benito Juárez')
    resp = orden.registra()
    assert resp['descripcionError'] is None
