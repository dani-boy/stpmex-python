from dataclasses import asdict

from OpenSSL import crypto
from zeep import Client as SoapClient

from .auth import compute_signature, join_fields
from .exc import InvalidPassphrase, StpmexException
from .orden import Orden

DEMO_BASE_URL = 'demo.stpmex.com:7024/speidemo'
PROD_BASE_URL = 'prod.stpmex.com/spei'


class Client:
    def __init__(
        self,
        empresa: str,
        priv_key: str,
        priv_key_passphrase: str,
        demo: bool = False,
    ):
        self.empresa = empresa
        try:
            self._pkey = crypto.load_privatekey(
                crypto.FILETYPE_PEM,
                priv_key,
                priv_key_passphrase.encode('ascii'),
            )
        except crypto.Error:
            raise InvalidPassphrase
        if demo:
            base_url = DEMO_BASE_URL
        else:
            base_url = PROD_BASE_URL
        wsdl = f'https://{base_url}/webservices/SpeiActualizaServices?wsdl'
        self.soap_client = SoapClient(wsdl)

    def soap_orden(self, orden: Orden) -> 'zeep.objects.ordenPagoWS':
        SoapOrden = self.soap_client.get_type('ns0:ordenPagoWS')
        soap_orden = SoapOrden(**asdict(orden))
        soap_orden.empresa = self.empresa
        return soap_orden

    def registrar_orden(
            self, orden: Orden) -> 'zeep.objects.speiServiceResponse':
        soap_orden = self.soap_orden(orden)
        joined_fields = join_fields(soap_orden)
        soap_orden.firma = compute_signature(self._pkey, joined_fields)
        resp = self.soap_client.service['registraOrden'](soap_orden)
        if 'descripcionError' in resp and resp.descripcionError:
            raise StpmexException(**resp.__values__)
        return resp
