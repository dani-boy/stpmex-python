import os
from base64 import b64encode

from OpenSSL import crypto


STP_EMPRESA = os.environ['STP_EMPRESA']
STP_PEM_FILEPATH = os.environ['STP_PEM_FILEPATH']
STP_PEM_PASSPHRASE = os.environ['STP_PEM_PASSPHRASE'].encode('ascii')
STP_PREFIJO = int(os.environ['STP_PREFIJO'])
SIGN_DIGEST = 'RSA-SHA256'

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
    __object__ = None
    __type__ = None
    _registra_method = None

    def __init__(self, **kwargs):
        self.__object__ = self.__type__(**kwargs)

    def __dir__(self):
        return dir(super(Resource, self)) + dir(self.__object__)

    def __eq__(self, other):
        return all(getattr(self, name) ==
                   getattr(other, name) for name in self.__fieldnames__)

    def __getattr__(self, item):
        if item.startswith('_'):
            return self.__getattribute__(item)
        return getattr(self.__object__, item)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        indent = ' ' * 4
        rv = f'{self.__class__.__name__}(\n'
        for name in self.__fieldnames__:
            rv += f'{indent}{name}={repr(getattr(self, name))},\n'
        rv += ')'
        return rv

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(Resource, self).__setattr__(key, value)
        else:
            setattr(self.__object__, key, value)

    def __str__(self):
        return self.__object__.__str__()

    @property
    def _joined_fields(self):
        return _join_fields(self, self.__fieldnames__)

    def _compute_signature(self):
        signature = crypto.sign(pkey, self._joined_fields, SIGN_DIGEST)
        return b64encode(signature).decode('ascii')

    def registra(self):
        self.firma = self._compute_signature()
        return self._registra_method(self.__object__)
