from decimal import Decimal
from typing import Dict, List, Any, overload, Union
from ICalc_type import ICalcType
from IThreshold import IThreshold
from filter_for_maxSttDay import FilterForMaxSttDay
from get_idx import GetIdx


class CalcTypeDistance(ICalcType):

    def __init__(self, unsouCD: str,
                 threshold:IThreshold,
                 untin_data: List[List[Any]], #unsouCDでfilterすみ
                 untin_col: List[str],
                 sur_data: List[List[Any]], #unsouCDでfilterすみ
                 sur_col: List[str]) -> None:

        self._unsouCD = unsouCD
        self._threshold = threshold
        self._untin_col = untin_col
        self._sur_col = sur_col
        '''
        IThreshold型のインスタンスはLessまたはLessEqualのどちらか。
        unsouListDictの'isLess'に合わせて調整されている。isLess='1' なら 
        Lessインスタンス。それ以外は、LessEqualインスタンス.
        calcTypeDistanceでない場合はuntin_data untin_colまたは
        sur_data sur_colが[]になっている
        '''

        #untin データのsttDayを今日より過去の最新でフィルタする
        # untin_dataが空の場合は空が返る今日より過去の最新が無い場合も空が返る
        self._untin_data = FilterForMaxSttDay.filter_maxSttDay(untin_data,
                                                               untin_col)
        #surcharge データのsttDayを今日より過去の最新でフィルタする
        self._sur_data = FilterForMaxSttDay.filter_maxSttDay(sur_data, sur_col)
        
    # --- エディタ用の型宣言 ---
    @overload                                                       
    def calc_base_untin(self, weight: float, distance: int) -> Decimal: 
        pass
                                                                    
    @overload                                                       
    def calc_base_untin(self, weight: float, distance: str) -> Decimal:
        pass

    # --- 実際の処理（デコレータは付けず、Unionで受け取る） ---
    def calc_base_untin(self, weight: float, distance: Union[int, str])-> Decimal:
        base_untin: Decimal = Decimal('0')
        if not self._untin_data:
            return base_untin

        i_distance:int = int(distance) # ここに渡ってくるdistanceは必ずint
        
        weight_idx:int = GetIdx.get_idx(self._untin_col, 'weightThre')
        distance_idx: int = GetIdx.get_idx(self._untin_col, 'distanceThre')
        fee_idx: int = GetIdx.get_idx(self._untin_col, 'fee')
        # weight_setとdistance_setを作る
        weight_set = set()
        distance_set = set()
        for line in self._untin_data:
            weight_set.add(line[weight_idx])
            distance_set.add(line[distance_idx])
        weights: List[int] = list(weight_set)
        distances: List[int] = list(distance_set)
        
        weight_thre: int = self._threshold.calc_threshold(weights, weight)
        distance_thre: int = self._threshold.calc_threshold(distances, 
                                                                i_distance)
        for line in self._untin_data:
            if (line[weight_idx] == weight_thre and
                line[distance_idx] == distance_thre):
                base_untin = line[fee_idx]


        print(self._unsouCD)
        print(weight_thre)
        print(distance_thre)
        print(base_untin)


        
        return base_untin


    def calc_surcharge(self)-> Decimal:
        return Decimal('0')

    def calc_relay(self)-> Decimal:
        return Decimal('0')
