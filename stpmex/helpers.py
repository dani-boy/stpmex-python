from clabe.banks import BankCode

from stpmex.types import Institucion


def spei_to_stp_bank_code(spei_code: str) -> Institucion:
    try:
        bank_name = BankCode(spei_code)
        return Institucion[bank_name.name]
    except (ValueError, KeyError):
        return None


def stp_to_spei_bank_code(stp_code: int) -> str:
    try:
        bank_name = Institucion(stp_code)
        return BankCode[bank_name.name].value
    except (ValueError, KeyError):
        return None
