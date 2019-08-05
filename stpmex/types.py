from enum import Enum


class Prioridad(Enum):
    normal = 0
    alta = 1


class TipoCuenta(Enum):
    card = 3
    phone_number = 10
    clabe = 40
