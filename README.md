# STP client python3.7+ client library

[![Build Status](https://travis-ci.com/cuenca-mx/stpmex-python.svg?branch=master)](https://travis-ci.com/cuenca-mx/stpmex-python)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/stpmex-python/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/stpmex-python?branch=master)
[![PyPI](https://img.shields.io/pypi/v/stpmex.svg)](https://pypi.org/project/stpmex/)

Cliente para el servicio SOAP de STP


## Requerimientos

Python v3.7 o superior.

## Instalación

```bash
pip install stpmex
```

## Test

```bash
make venv
source venv/bin/activate
make test
```

## Uso básico

```python
from stpmex import Client, Orden

client = Client(
    empresa='TU_EMPRESA',
    priv_key='PKEY_CONTENIDO',
    priv_key_passphrase='supersecret'
)
orden = Orden(
    institucionContraparte='40072',
    monto=1.2,
    nombreBeneficiario='Ricardo Sanchez',
    tipoCuentaBeneficiario=40,
    cuentaBeneficiario='072691004495711499',
    conceptoPago='Prueba',
)
resp = client.registrar_orden(orden)
orden_id = resp['id']
```