from decimal import Decimal
from typing import Dict
from ICalc_type import ICalcType
from IThreshold import IThreshold

class CalcTypeRelay(ICalcType):

    def __init__(self, thresholds:Dict[str,IThreshold])-> None:
        self._thresholds = thresholds
        ''' '['less'],['lessEqual']'''


    def calc_fee(self)-> Decimal:
        pass
