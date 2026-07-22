from decimal import Decimal
from typing import List, Dict, Any
from ICalc_type import ICalcType


class Hauler:

    def __init__(self, 
                 unsouDict:Dict[str,Any],
                 calcTypes:Dict[str,ICalcType],
                 weight: float,
                 ) -> None:
        self._unsouDict = unsouDict
        self._calcTypes = calcTypes
        self._weight = weight
        

    def calc_base_untin(self)-> Decimal:
        pass

    def calc_srucharge(self)-> Decimal:
        pass

    def calc_relay(self)-> Decimal:
        pass

    def calc_extraCharge(self)-> Decimal:
        pass

    def show(self)-> None:
        print(self._unsouDict['unsouCD'])
        print(self._unsouDict['unsouName'])
