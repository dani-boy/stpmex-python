import os

import zeep

from .resources import Orden


wsdl_path = os.path.join(os.path.dirname(__file__), 'SpeiServices.wsdl')
actualiza_client = zeep.Client(wsdl_path)
