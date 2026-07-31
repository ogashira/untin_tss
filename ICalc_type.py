from abc import ABC, abstractmethod
from decimal import Decimal
from typing import overload, Union


class ICalcType(ABC):

    @overload
    def calc_base_untin(self, weight:float, distance:int)-> Decimal:
        pass

    @overload
    def calc_base_untin(self, weight:float, distance:str)-> Decimal:
        pass

    @abstractmethod
    def calc_base_untin(self, weight: float, 
                        distance: Union[int, str]) -> Decimal:
        pass

    @abstractmethod
    def calc_surcharge(self)-> Decimal:
        pass

    @abstractmethod
    def calc_relay(self)-> Decimal:
        pass
