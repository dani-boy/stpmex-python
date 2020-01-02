import datetime as dt
from dataclasses import asdict
from typing import Any, ClassVar, Dict


class Resource:
    _client: ClassVar['stpmex.Client']  # type: ignore
    _endpoint: ClassVar[str]
    empresa: ClassVar[str]

    @property
    def firma(self):
        ...  # pragma: no cover

    def to_dict(self) -> Dict[str, Any]:
        base = dict()
        for k, v in asdict(self).items():
            if isinstance(v, dt.date):
                base[k] = v.strftime('%Y%m%d')
            elif v:
                base[k] = v
        return {**base, **dict(firma=self.firma, empresa=self.empresa)}
