import os

import zeep


actualiza_client = zeep.Client(os.environ['STP_ACTUALIZA_WSDL'])
consulta_client = zeep.Client(os.environ['STP_CONSULTA_WSDL'])
