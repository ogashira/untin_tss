from decimal import Decimal
from typing import Dict, List, Any
from ICalc_type import ICalcType
from IThreshold import IThreshold
from filter_for_maxSttDay import FilterForMaxSttDay


class CalcTypeRelay(ICalcType):

    def __init__(self, unsouCD: str,
                 threshold:IThreshold,
                 relay_data: List[List[Any]],
                 relay_col: List[str])-> None:

        self._unsouCD = unsouCD
        self._threshold = threshold

        '''
        IThreshold型のインスタンスはLessまたはLessEqualのどちらか。
        unsouListDictの'isLess'に合わせて調整されている。isLess='1' なら 
        Lessインスタンス。それ以外は、LessEqualインスタンス.
        '''
        #relay データのsttDayを今日より過去の最新でフィルタする
        self._relay_data:List[List[int]] = []
        self._relay_data = FilterForMaxSttDay.filter_maxSttDay(relay_data,
                                                               relay_col)


    def calc_base_untin(self)-> Decimal:
        return Decimal('0')


    def calc_surcharge(self)-> Decimal:
        return Decimal('0')

    def calc_relay(self)-> Decimal:
        return Decimal('0')
