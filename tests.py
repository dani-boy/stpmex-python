from stpmex import Orden
from stpmex.types import Institucion
import vcr


@vcr.use_cassette()
def test_join_fields(initialize_stpmex, mock_orden):
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
    joined = ('||846|STP|20160810|1q2w33e|1q2w33e||121.00|1|40||||40|'
              'eduardo|846180000300000004| ND|fernanda.cedillo@stpmex.com|||||'
              'pago prueba||||||123123||T||3|0|||').encode('utf-8')

    assert orden._joined_fields == joined


@vcr.use_cassette()
def test_create_orden(initialize_stpmex):
    orden = Orden(
        conceptoPago='concepto',
        institucionOperante=Institucion.STP.value,
        cuentaBeneficiario='846180000400000001',
        institucionContraparte=846,
        monto=1234,
        nombreBeneficiario='Benito Juárez')
    resp = orden.registra()
    assert resp.descripcionError is None
    assert type(resp.id) is int
    assert resp.id > 0
    assert orden._id == resp.id
