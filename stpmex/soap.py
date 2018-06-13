import os

import zeep


STP_WSDL = os.environ['STP_WSDL']
client = zeep.Client(STP_WSDL)
