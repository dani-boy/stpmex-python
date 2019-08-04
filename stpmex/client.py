from OpenSSL import crypto
from zeep import Client as SoapClient

from .base import Resource
from .exc import InvalidPassphrase

DEFAULT_WSDL = (
    'https://demo.stpmex.com:7024/speidemo/webservices/SpeiActualizaServices?'
    'wsdl'
)


class Client:
    def __init__(
        self,
        empresa: str,
        priv_key: str,
        priv_key_passphrase: str,
        prefijo: int,
        wsdl_path: str = DEFAULT_WSDL
    ):
        self.empresa = empresa
        try:
            self.priv_key = crypto.load_privatekey(
                crypto.FILETYPE_PEM, priv_key,
                priv_key_passphrase.encode('ascii')
            )
        except crypto.Error:
            raise InvalidPassphrase
        self.prefijo = prefijo
        self.soap_client = SoapClient(wsdl_path)
        Resource._soap_client = self.soap_client
