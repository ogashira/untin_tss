from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Union


class ICalcType(ABC):

    @abstractmethod
    def calc_fee(self, weight: float, distance: Union[int, str]) -> Decimal:
        pass

