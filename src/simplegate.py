"""Расчет шандорного затвора."""
from typing import NamedTuple
from dry.allcalc import Mass, Distance, InputDataError
from dry.allgui import fstr


class InputData(NamedTuple):
    """Входные данные для расчета."""

    frame_w: Distance
    gate_h: Distance


class SimpleGate:
    """Расчет шандора."""

    MIN_WIDTH = Distance(0.3)
    MAX_WIDTH = Distance(3.0)

    MIN_HEIGHT = Distance(0.3)
    MAX_HEIGHT = Distance(8.0)

    @property
    def frame_mass(self) -> Mass:
        """Масса рамы шандора."""
        return self._frame_mass

    @property
    def gate_mass(self) -> Mass:
        """Масса щита шандора."""
        return self._gate_mass

    @property
    def mass(self) -> Mass:
        """Масса шандора."""
        return self._mass

    @property
    def designation(self) -> str:
        """Обозначение шандора."""
        return self._designation

    def __init__(self, input_data: InputData) -> None:
        """Конструктор и одновременно расчет."""
        self._input_data = input_data

        if not self.MIN_WIDTH <= self._input_data.frame_w <= self.MAX_WIDTH:
            raise InputDataError('Ширина рамы от {} до {} мм.'.format(
                fstr(self.MIN_WIDTH * 1e3, '%.0f'),
                fstr(self.MAX_WIDTH * 1e3, '%.0f')))

        if not self.MIN_HEIGHT <= self._input_data.gate_h <= self.MAX_HEIGHT:
            raise InputDataError('Высота щита от {} до {} мм.'.format(
                fstr(self.MIN_HEIGHT * 1e3, '%.0f'),
                fstr(self.MAX_HEIGHT * 1e3, '%.0f')))

        self._designation = self._create_designation()

        self._mass_sg01ad001 = self._calc_mass_sg01ad001()
        self._mass_sg01ad002 = self._calc_mass_sg01ad002()
        self._mass_sg01ad003 = self._calc_mass_sg01ad003()
        self._mass_sg01ad004 = self._calc_mass_sg01ad004()
        self._mass_sg01ad005 = self._calc_mass_sg01ad005()
        self._count_sg01ad005 = self._calc_count_sg01ad005()
        self._frame_mass = self._calc_frame_mass()

        self._mass_sg02ad001 = self._calc_mass_sg02ad001()
        self._mass_sg02ad002 = self._calc_mass_sg02ad002()
        self._mass_sg02ad003 = self._calc_mass_sg02ad003()
        self._count_sg02ad003 = self._calc_count_sg02ad003()
        self._mass_sg02ad004 = self._calc_mass_sg02ad004()
        self._fasteners_mass_sg02ad = self._calc_fasteners_mass_sg02ad()
        self._gate_mass = self._calc_gate_mass()

        self._mass = self._calc_mass()

    def _create_designation(self) -> str:
        def fstr_ng(value: float, precision: int) -> str:
            if value.is_integer():
                return fstr(value, f'%.{precision}f')
            return fstr(value)

        return 'Шандор {}х{}'.format(fstr_ng(self._input_data.frame_w, 1),
                                     fstr_ng(self._input_data.gate_h, 1))

    # Швеллер.
    def _calc_mass_sg01ad001(self) -> Mass:
        return Mass(3.5879 * self._input_data.gate_h - 0.0079)

    # Опора нижняя.
    def _calc_mass_sg01ad002(self) -> Mass:
        return Mass(5.6686 * self._input_data.frame_w - 0.0057)

    # Перемычка.
    def _calc_mass_sg01ad003(self) -> Mass:
        return Mass(2.992 * self._input_data.frame_w - 0.06)

    # Проушина.
    @staticmethod
    def _calc_mass_sg01ad004() -> Mass:
        return Mass(0.25)

    # Скоба.
    @staticmethod
    def _calc_mass_sg01ad005() -> Mass:
        return Mass(0.05)

    # Количество скоб на раме.
    def _calc_count_sg01ad005(self) -> int:
        step = 0.4
        return int(self._input_data.gate_h / step)

    # Полотно.
    def _calc_mass_sg02ad001(self) -> Mass:
        return Mass(32 * self._input_data.frame_w * self._input_data.gate_h
                    - 0.9602 * self._input_data.gate_h - 0.009)

    # Ребро вертикальное.
    def _calc_mass_sg02ad002(self) -> Mass:
        return Mass(2.9933 * self._input_data.gate_h - 0.2301)

    # Ребро горизонтальное.
    def _calc_mass_sg02ad003(self) -> Mass:
        return Mass(2.992 * self._input_data.frame_w - 0.64)

    # Количество горизонтальных ребер.
    def _calc_count_sg02ad003(self) -> int:
        step = 0.75
        return 2 + int(self._input_data.gate_h / step)

    # Проушина на щите.
    @staticmethod
    def _calc_mass_sg02ad004() -> Mass:
        return Mass(0.42)

    # Крепеж щита.
    @staticmethod
    def _calc_fasteners_mass_sg02ad() -> Mass:
        return Mass(0.12)

    def _calc_frame_mass(self) -> Mass:
        return Mass(self._mass_sg01ad001 * 4
                    + self._mass_sg01ad002 * 1
                    + self._mass_sg01ad003 * 1
                    + self._mass_sg01ad004 * 2
                    + self._mass_sg01ad005 * self._count_sg01ad005)

    def _calc_gate_mass(self) -> Mass:
        return Mass(self._mass_sg02ad001 * 1
                    + self._mass_sg02ad002 * 2
                    + self._mass_sg02ad003 * self._count_sg02ad003
                    + self._mass_sg02ad004 * 1
                    + self._fasteners_mass_sg02ad)

    def _calc_mass(self) -> Mass:
        return Mass(self._frame_mass + self._gate_mass)
