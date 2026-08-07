from decimal import Decimal
from typing import Dict, List, Any, Union
from ICalc_type import ICalcType
from IThreshold import IThreshold
from filter_for_maxSttDay import FilterForMaxSttDay
from get_idx import GetIdx


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
        self._relay_data = FilterForMaxSttDay.filter_maxSttDay(relay_data,
                                                               relay_col)
        self._relay_col = relay_col


    # --- 実際の処理（デコレータは付けず、Unionで受け取る） ---
    def calc_fee(self, weight: float, distance: Union[int, str])-> Decimal:
        # relayの場合のdistanceは回数
        fee: Decimal = Decimal('0')
        if not self._relay_data:
            return fee

        count:int = int(distance)

        weight_idx:int = GetIdx.get_idx(self._relay_col, 'weightThre')
        fee_idx: int = GetIdx.get_idx(self._relay_col, 'fee')

        # weight_setとdistance_setを作る
        weight_set = set()
        for line in self._relay_data:
            weight_set.add(line[weight_idx])
        weights = list(weight_set)

        weight_thre: int = self._threshold.calc_threshold(weights, weight)

        weightFee:Decimal = Decimal('0')
        for line in self._relay_data:
            if line[weight_idx] == weight_thre:
                weightFee = line[fee_idx]

        '''
        # TODO
        print(self._unsouCD)
        print('中継')
        print(weight_thre)
        print(f'count= {count}')
        print(weightFee * count)
        print('.' * 20)
        '''

        return  weightFee * count
