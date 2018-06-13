import os
from base64 import b64encode

import zeep
from OpenSSL import crypto


STP_EMPRESA = os.environ['STP_EMPRESA']
STP_PEM_FILEPATH = os.environ['STP_PEM_FILEPATH']
STP_PEM_PASSPHRASE = os.environ['STP_PEM_PASSPHRASE'].encode('ascii')
STP_PREFIJO = int(os.environ['STP_PREFIJO'])
STP_WSDL = os.environ['STP_WSDL']
SIGN_DIGEST = 'RSA-SHA256'

client = zeep.Client(STP_WSDL)
with open(STP_PEM_FILEPATH, 'rb') as pkey_file:
    pkey = crypto.load_privatekey(
        crypto.FILETYPE_PEM, pkey_file.read(), STP_PEM_PASSPHRASE)


def _join_fields(obj, fieldnames):
    fields = []
    for name in fieldnames:
        if name in ['monto', 'iva'] and not getattr(obj, name) in ['', None]:
            field = float(getattr(obj, name))
            field = f'{field:.2f}'
        else:
            field = getattr(obj, name) or ''
        fields.append(str(field))
    return ('||' + '|'.join(fields) + '||').encode('utf-8')


class Resource:

    __fieldnames__ = None
    __type__ = None
    _submit_method = None

    def __init__(self, **kwargs):
        self.__object__ = self.__type__(**kwargs)

    def __getattr__(self, item):
        if item.startswith('_'):
            return self.__getattribute__(item)
        return getattr(self.__object__, item)

    def __repr__(self):
        return self.__object__.__repr__()

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(Resource, self).__setattr__(key, value)
        else:
            setattr(self.__object__, key, value)

    def __str__(self):
        return self.__object__.__str__()

    def _compute_signature(self):
        fields_str = _join_fields(self, self.__fieldnames__)
        signature = crypto.sign(pkey, fields_str, SIGN_DIGEST)
        return b64encode(signature).decode('ascii')

    def submit(self):
        self.firma = self._compute_signature()
        return self._submit_method(self.__object__)
