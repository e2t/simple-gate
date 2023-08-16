import math
from typing import SupportsFloat


class ComparableFloat(float):
    PRECISION = 1e-6

    def __eq__(self, x: object) -> bool:
        if not isinstance(x, SupportsFloat):
            return NotImplemented
        return math.isclose(self, x, abs_tol=self.PRECISION)

    def __ne__(self, x: object) -> bool:
        if not isinstance(x, SupportsFloat):
            return NotImplemented
        return not math.isclose(self, x, abs_tol=self.PRECISION)

    def __lt__(self, x: object) -> bool:
        if not isinstance(x, SupportsFloat):
            return NotImplemented
        return (not math.isclose(self, x, abs_tol=self.PRECISION)) and super().__lt__(
            x.__float__()
        )

    def __gt__(self, x: object) -> bool:
        if not isinstance(x, SupportsFloat):
            return NotImplemented
        return (not math.isclose(self, x, abs_tol=self.PRECISION)) and super().__gt__(
            x.__float__()
        )

    def __le__(self, x: object) -> bool:
        if not isinstance(x, SupportsFloat):
            return NotImplemented
        return super().__le__(x.__float__()) or math.isclose(
            self, x, abs_tol=self.PRECISION
        )

    def __ge__(self, x: object) -> bool:
        if not isinstance(x, SupportsFloat):
            return NotImplemented
        return super().__ge__(x.__float__()) or math.isclose(
            self, x, abs_tol=self.PRECISION
        )
