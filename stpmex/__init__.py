from .ordenes import Orden
from OpenSSL import crypto
from .base import STP_EMPRESA, STP_PREFIJO, STP_PRIVKEY, STP_PRIVKEY_PASSPHRASE, WSDL_PATH


def configure(wsdl_path:str, empresa:str, priv_key:str, priv_key_passphrase:str, prefijo: int):
    base.STP_EMPRESA = empresa
    base.STP_PRIVKEY = crypto.load_privatekey(crypto.FILETYPE_PEM, priv_key, priv_key_passphrase.encode('ascii'))
    base.STP_PRIVKEY_PASSPHRASE = priv_key_passphrase
    base.STP_PREFIJO = prefijo,
    base.WSDL_PATH = wsdl_path
