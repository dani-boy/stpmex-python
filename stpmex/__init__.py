from .ordenes import Orden
from OpenSSL import crypto
from .base import STP_EMPRESA, STP_PREFIJO, STP_PRIVKEY, STP_PRIVKEY_PASSPHRASE
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport

DEFAULT_WSDL = 'https://demo.stpmex.com:7024/speidemo/webservices/SpeiActualizaServices?wsdl'


def configure(empresa: str, priv_key: str, priv_key_passphrase: str, prefijo: int, wsdl_path: str = DEFAULT_WSDL,
              proxy: str = None, proxy_user: str = None, proxy_password: str = None):
    base.STP_EMPRESA = empresa
    base.STP_PRIVKEY = crypto.load_privatekey(crypto.FILETYPE_PEM, priv_key, priv_key_passphrase.encode('ascii'))
    base.STP_PRIVKEY_PASSPHRASE = priv_key_passphrase
    base.STP_PREFIJO = prefijo
    base.WSDL_PATH = wsdl_path

    if proxy is not None:
        session = Session()
        session.proxies = {
            'https': proxy
        }
        session.auth = HTTPBasicAuth(proxy_user, proxy_password)
        base.ACTUALIZA_CLIENT = Client(wsdl_path, transport=Transport(session=session))
    else:
        base.ACTUALIZA_CLIENT = Client(wsdl_path)
