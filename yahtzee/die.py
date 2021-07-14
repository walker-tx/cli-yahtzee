from dataclasses import dataclass


@dataclass
class Die:
    _value: int = 1

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val):
        if 1 > val > 6:
            raise ValueError('Cannot land on a value less than one or greater than 6.')

        self._value = val
