from decimal import Decimal
from typing import Dict, List, Any, overload, Union
from ICalc_type import ICalcType
from IThreshold import IThreshold
from filter_for_maxSttDay import FilterForMaxSttDay
from get_idx import GetIdx


class CalcTypeRegionUntin(ICalcType):

    def __init__(self, unsouCD: str,
                 threshold:IThreshold,
                 untin_data: List[List[Any]], #unsouCDでfilterすみ
                 untin_col: List[str]) -> None:

        self._unsouCD = unsouCD
        self._threshold = threshold
        self._untin_col = untin_col

        '''
        IThreshold型のインスタンスはLessまたはLessEqualのどちらか。
        unsouListDictの'isLess'に合わせて調整されている。isLess='1' なら 
        Lessインスタンス。それ以外は、LessEqualインスタンス.
        '''
        #untin データのsttDayを今日より過去の最新でフィルタする
        # untin_dataが空の場合は空が返る今日より過去の最新が無い場合も空が返る
        self._untin_data = FilterForMaxSttDay.filter_maxSttDay(untin_data,
                                                               untin_col)


    # --- 実際の処理（デコレータは付けず、Unionで受け取る） ---
    def calc_fee(self, weight: float, distance: Union[int, str])-> Decimal:
        fee: Decimal = Decimal('0')
        if not self._untin_data:
            return fee

        # ここに渡ってくるのは必ずstr
        s_distance:str = str(distance)
        
        weight_idx:int = GetIdx.get_idx(self._untin_col, 'weightThre')
        regionCD_idx: int = GetIdx.get_idx(self._untin_col, 'regionCD')
        fee_idx: int = GetIdx.get_idx(self._untin_col, 'fee')

        # weight_setとdistance_setを作る
        weight_set = set()
        for line in self._untin_data:
            weight_set.add(line[weight_idx])
        weights = list(weight_set)

        weight_thre: int = self._threshold.calc_threshold(weights, weight)

        for line in self._untin_data:
            if (line[weight_idx] == weight_thre and
                line[regionCD_idx] == s_distance):
                fee = line[fee_idx]
        
        '''
        # TODO
        print(self._unsouCD)
        print('運賃')
        print(weight_thre)
        print(s_distance)
        print(fee)
        print('.' * 20)
        '''

        return fee
