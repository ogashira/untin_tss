from typing import List, Any
import datetime
from get_idx import GetIdx

class FilterForMaxSttDay:

    @staticmethod
    def filter_maxSttDay(data: List[List[Any]],
                          cols: List[str]) -> List[List[Any]]: 


        def _calc_sttDay(data: List[List[Any]], idx: int)-> str:
            if not data:
                return ''

            set_sttDays = set()
            today = datetime.datetime.today()
            strToday = today.strftime('%Y%m%d')
            # 今日より小さい年月日をsetに入れる
            for line in data:
                if line[idx] <= strToday:
                    set_sttDays.add(line[idx])
            sttDays:List = list(set_sttDays)

            if not sttDays:
                return ''

            return max(sttDays)


        filterd_list: List[List[int]] = []

        sttDay_idx: int = GetIdx.get_idx(cols, 'sttDay')
        sttDay: str = _calc_sttDay(data, sttDay_idx)

        if sttDay == '':
            return filterd_list

        for line in data:
            if line[sttDay_idx] == sttDay:
                filterd_list.append(line)
        return filterd_list

