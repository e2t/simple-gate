import sys
from typing import NoReturn

from dry.l10n import AddMsgL10n, MsgFormat


class CalcError(Exception):
    pass


class BaseCalc:
    def __init__(self, adderror: AddMsgL10n | None = None) -> None:
        self.__adderror = adderror if adderror is not None else self.__fallback_adderror

    @staticmethod
    def __fallback_adderror(msg: MsgFormat, *args: object) -> None:
        print(msg, args, file=sys.stderr)

    def _raise_error(self, msg: MsgFormat, *args: object) -> NoReturn:
        self.__adderror(msg, *args)
        raise CalcError()
