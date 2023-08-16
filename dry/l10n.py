from typing_extensions import Protocol

ENG = "eng"
UKR = "ukr"
RUS = "rus"
LIT = "lit"

MsgFormat = dict[str, str] | str


class AddMsgL10n(Protocol):
    def __call__(self, msg: MsgFormat, *args: object) -> None:
        ...
