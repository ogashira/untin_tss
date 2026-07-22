from abc import ABC, abstractmethod
from decimal import Decimal


class ICalcType(ABC):

    @abstractmethod
    def calc_fee(self)-> Decimal:
        pass

