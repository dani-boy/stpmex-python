import time

import pytest


@pytest.mark.vcr
def test_registrar_orden(client, orden):
    orden.claveRastreo = f'CR{int(time.time())}'
    resp = client.registrar_orden(orden)
    assert resp['descripcionError'] is None
    assert isinstance(resp['id'], int)
