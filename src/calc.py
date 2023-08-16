from dataclasses import dataclass

from dry.basecalc import BaseCalc
from dry.comparablefloat import ComparableFloat as Cf
from dry.l10n import AddMsgL10n

import text.error


@dataclass(frozen=True)
class InputData:
    width: float
    height: float


_MIN_WIDTH = 0.3
_MAX_WIDTH = 3.0
_MIN_HEIGHT = 0.3
_MAX_HEIGHT = 4.5


class StoplogGate(BaseCalc):
    def __init__(self, inpdata: InputData, adderror: AddMsgL10n | None = None) -> None:
        super().__init__(adderror)

        if not Cf(_MIN_WIDTH) <= Cf(inpdata.width) <= Cf(_MAX_WIDTH):
            self._raise_error(text.error.NONSTD_WIDTH, _MIN_WIDTH, _MAX_WIDTH)
        if not Cf(_MIN_HEIGHT) <= Cf(inpdata.height) <= Cf(_MAX_HEIGHT):
            self._raise_error(text.error.NONSTD_HEIGHT, _MIN_HEIGHT, _MAX_HEIGHT)

        self.width = inpdata.width
        self.height = inpdata.height

        self.frame_mass = self.__calc_frame_mass()
        self.gate_mass = self.__calc_gate_mass()
        self.mass = self.frame_mass + self.gate_mass

    # Швеллер
    def __calc_mass_01ad001(self) -> float:
        return 3.5879 * self.height - 0.0079

    # Опора нижняя
    def __calc_mass_01ad002(self) -> float:
        return 5.6686 * self.width - 0.0057

    # Перемычка
    def __calc_mass_01ad003(self) -> float:
        return 2.992 * self.width - 0.06

    # Количество скоб на раме
    def __calc_count_01ad005(self) -> int:
        step = 0.4
        return int(self.height / step)

    def __calc_frame_mass(self) -> float:
        mass_01ad004 = 0.25  # Проушина
        mass_01ad005 = 0.05  # Скоба
        return (
            self.__calc_mass_01ad001() * 4
            + self.__calc_mass_01ad002()
            + self.__calc_mass_01ad003()
            + mass_01ad004 * 2
            + mass_01ad005 * self.__calc_count_01ad005()
        )

    def __calc_gate_mass(self) -> float:
        head = self.height
        factor = self.width**2 * self.height * head / 2
        return 11.45 * factor + 105.67
