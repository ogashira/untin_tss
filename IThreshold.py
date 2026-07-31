from typing import List
from abc import ABC, abstractmethod
from decimal import Decimal


class IThreshold(ABC):

    @abstractmethod
    def calc_threshold(self, thresholds: List, val: float)-> int:
        pass
