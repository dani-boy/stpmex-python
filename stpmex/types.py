from enum import Enum


class AccountType(Enum):
    card = 3
    phone_number = 10
    clabe = 40


class Prioridad(Enum):
    normal = 0
    alta = 1
