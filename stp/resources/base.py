import os
from base64 import b64encode

import zeep
from OpenSSL import crypto


STP_EMPRESA = os.environ['STP_EMPRESA']
STP_PEM_FILEPATH = os.environ['STP_PEM_FILEPATH']
STP_PEM_PASSPHRASE = os.environ['STP_PEM_PASSPHRASE'].encode('ascii')
STP_PREFIJO = int(os.environ['STP_PREFIJO'])
STP_WSDL = os.environ['STP_WSDL']

client = zeep.Client(STP_WSDL)
with open(STP_PEM_FILEPATH, 'rb') as pkey_file:
    pkey = crypto.load_privatekey(
        crypto.FILETYPE_PEM, pkey_file.read(), STP_PEM_PASSPHRASE)


class Resource:

    _field_names = None
    _submit_method = None
    _type = None

    def __init__(self, **kwargs):
        self._object = self._type(**kwargs)

    def _compute_signature(self):
        fields = '||'
        for fieldname in self._field_names:
            field = getattr(self._object, fieldname) or ''
            field = str(field)
            fields += '|' + field
        fields += '||'
        fields = fields.encode('ascii')
        signature = crypto.sign(pkey, fields, 'RSA-SHA256')
        return b64encode(signature).decode('ascii')

    def submit(self):
        self._object.firma = self._compute_signature()
        return self._submit_method(self._object)
