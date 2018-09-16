import argparse
import json
import stpmex
from stpmex import Orden
from stpmex.types import Institucion

DEFAULT_FILE_NAME = 'stp.config'


def config():
    print('Configuring connection')
    print('It will create a stp.config file')

    pk_file = input('Route to private key: ')
    with open(pk_file) as fp:
        pk_value = fp.read()
    configuration = {
        'wsdl': input('WSDL: '),
        'private_key': pk_value,
        'pkey_passphrase': input('Private key passphrase: '),
        'empresa': input('Empresa: '),
        'prefijo': input('Prefijo: ')
    }
    use_proxy = input('Wish to use a proxy? (y/n): ').lower() == 'y'
    if use_proxy:
        configuration['proxy'] = input('Proxy: ')
        configuration['user'] = input('User: ')
        configuration['password'] = input('Password: ')

    with open(DEFAULT_FILE_NAME, 'w') as outfile:
        json.dump(configuration, outfile)

    print("Done...")


def order():
    try:
        with open(DEFAULT_FILE_NAME, 'r') as f:
            config = json.load(f)
    except:
        print("No configuration file found, use: stpmex config")
        return

    stpmex.configure(wsdl_path=config['wsdl'], empresa=config['empresa'], priv_key=config['private_key'],
                     priv_key_passphrase=config['pkey_passphrase'], prefijo=config['prefijo'],
                     proxy=None if 'proxy' not in config else config['proxy'],
                     proxy_user=None if 'user' not in config else config['user'],
                     proxy_password=None if 'password' not in config else config['password'])

    print("Connection established")

    order = Orden()
    order.institucionOperante= Institucion.STP.value
    order.nombreBeneficiario = input('Nombre del beneficiario: ')
    order.cuentaBeneficiario = input('CLABE del beneficiario: ')
    order.institucionContraparte = int(order.cuentaBeneficiario[:3])
    order.conceptoPago = input('Concepto de pago: ')
    order.monto = float(input('Monto: ')) # I assume you won't put a str here
    rfc = input('RFC o CURP de beneficiario (opcional): ')
    if rfc:
        order.rfcCurpBeneficiario = rfc
    num_reference = input('Referencia númerica (opcional): ')
    if num_reference:
        order.referenciaNumerica = num_reference
    track_code = input('Clave de rastreo (opcional): ')
    if track_code:
        order.claveRastreo = track_code

    print("Sending order....")
    r = order.registra()

    print("Finished")
    print(r)


def main():
    parser = argparse.ArgumentParser(description='Creates an order to STP')
    parser.add_argument('option', choices=['config', 'order'],
                        help="'config' to configure the client, 'order' for creating a new order")
    args = parser.parse_args()
    if args.option == 'config':
        config()
    if args.option == 'order':
        order()


if __name__ == '__main__':
    main()
