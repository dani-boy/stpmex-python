from base64 import b64encode

from OpenSSL import crypto

ORDEN_FIELDNAMES = """
    institucionContraparte
    empresa
    fechaOperacion
    folioOrigen
    claveRastreo
    institucionOperante
    monto
    tipoPago
    tipoCuentaOrdenante
    nombreOrdenante
    cuentaOrdenante
    rfcCurpOrdenante
    tipoCuentaBeneficiario
    nombreBeneficiario
    cuentaBeneficiario
    rfcCurpBeneficiario
    emailBeneficiario
    tipoCuentaBeneficiario2
    nombreBeneficiario2
    cuentaBeneficiario2
    rfcCurpBeneficiario2
    conceptoPago
    conceptoPago2
    claveCatUsuario1
    claveCatUsuario2
    clavePago
    referenciaCobranza
    referenciaNumerica
    tipoOperacion
    topologia
    usuario
    medioEntrega
    prioridad
    iva
    """.split()
SIGN_DIGEST = 'RSA-SHA256'


def join_fields(orden) -> bytes:
    joined_fields = []
    for field in ORDEN_FIELDNAMES:
        value = getattr(orden, field, None)
        if isinstance(value, float):
            value = f'{value:.2f}'
        joined_fields.append(str(value or ''))
    return ('||' + '|'.join(joined_fields) + '||').encode('utf-8')


def compute_signature(pkey: crypto.PKey, text: bytes) -> str:
    signature = crypto.sign(pkey, text, SIGN_DIGEST)
    return b64encode(signature).decode('ascii')
