from abc import ABC, abstractmethod
from decimal import Decimal


class IThreshold(ABC):

    @abstractmethod
    def calc_threshold(self)-> int:
        pass
