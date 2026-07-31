from typing import Dict, TYPE_CHECKING, Any, List, Tuple
import platform
import sys
from fetch_data_for_list import IFetchDataForList
from get_idx import GetIdx

# 実行時にはインポートせず、型チェックの為だけに書く
if TYPE_CHECKING:
    from ICalc_type import ICalcType
    from hauler import Hauler

class InstanceFactory:
    '''
    各モジュールのインポートは必要な時にメソッド内で行う。
    冒頭でまとめてやると実行速度が急激に遅くなったため
    '''

    _sqlServerTss: Any = None
    _sqlServerEffit: Any = None
    _cnxn_tss = None
    _cnxn_effit = None

    _instances: Dict[str, Any] = {}

    @classmethod
    def _setup_sql_path(cls) -> None:
        """SQLサーバー用モジュールのパスを通す (一度だけ実行)"""
        if 'sql_path_setup' in cls._instances:
            return
            
        shared_folder_path: str = r'./'
        if platform.system() == 'Linux':
            shared_folder_path = \
                r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
        elif platform.system() == 'Windows':
            shared_folder_path = \
                r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
        
        if shared_folder_path not in sys.path:
            sys.path.append(shared_folder_path)
        cls._instances['sql_path_setup'] = True

    @classmethod
    def get_sql_server_tss(cls) -> None:
        if cls._sqlServerTss is None:
            cls._setup_sql_path()
            from sql_server_tss_addmin import SqlServer as SqlServerTss 
            cls._sqlServerTss = SqlServerTss()
            cls._cnxn_tss = cls._sqlServerTss.get_cnxn()

    # TODO テストが終わったら、sql_server_testをsql_serverに戻す
    @classmethod
    def get_sql_server_effit(cls) -> None:
        if cls._sqlServerEffit is None:
            cls._setup_sql_path()
            from sql_server_test import SqlServer as SqlServerEffit
            cls._sqlServerEffit = SqlServerEffit()
            cls._cnxn_effit = cls._sqlServerEffit.get_cnxn()

    @classmethod
    def delete_cnxn(cls) -> None:
        if cls._sqlServerTss:
            cls._sqlServerTss.close()
        if cls._sqlServerEffit:
            cls._sqlServerEffit.close()

    @classmethod
    def get_fetchMAITEM(cls, parts:str) -> IFetchDataForList:
        from fetch_data_for_list import FetchMAITEM
        ins_name: str = 'fetchMAITEM'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchMAITEM(cls._cnxn_effit, parts)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchMDSDST(cls, ui_info: Dict[str,str]) -> IFetchDataForList:
        from fetch_data_for_list import FetchMDSDST
        ins_name: str = 'fetchMDSDST'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchMDSDST(cls._cnxn_effit, ui_info)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchUntin(cls, kojCD: str) -> IFetchDataForList:
        from fetch_data_for_list import FetchUntin
        ins_name: str = 'fetchUntin'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchUntin(cls._cnxn_effit, kojCD)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchSurcharge(cls, kojCD: str) -> IFetchDataForList:
        from fetch_data_for_list import FetchSurcharge
        ins_name: str = 'fetchSurcharge'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchSurcharge(cls._cnxn_effit, kojCD)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchRelay(cls, kojCD: str) -> IFetchDataForList:
        from fetch_data_for_list import FetchRelay
        ins_name: str = 'fetchRelay'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchRelay(cls._cnxn_effit, kojCD)
        return cls._instances[ins_name]


    @classmethod
    def get_Haulers(cls, unsouListDict:List[Dict[str, Any]], 
                    untin_data: List[List[Any]],
                    untin_col: List[str],
                    sur_data: List[List[Any]],
                    sur_col: List[str],
                    relay_data: List[List[Any]],
                    relay_col: List[str],
                    weight:float) -> List['Hauler']:

        from IThreshold import IThreshold
        from less import Less
        from less_equal import LessEqual
        from ICalc_type import ICalcType
        from calc_type_relay import CalcTypeRelay
        from calc_type_distance import CalcTypeDistance
        from calc_type_region import CalcTypeRegion
        from hauler import Hauler

        less: IThreshold = Less()
        lessEqual: IThreshold = LessEqual()

        haulers: List[Hauler] = []
        for innerDict in unsouListDict:
            filterUntin:List[List[Any]] = []
            filterSur: List[List[Any]] = []
            filterRelay: List[List[Any]] = []
            unsouCD:str = innerDict['unsouCD']
            untin_idx: int = GetIdx.get_idx(untin_col, 'unsouCD')
            sur_idx: int = GetIdx.get_idx(sur_col, 'unsouCD')
            relay_idx: int = GetIdx.get_idx(relay_col, 'unsouCD')
            for line in untin_data:
                if line[untin_idx] == unsouCD:
                    filterUntin.append(line)
            for line in sur_data:
                if line[sur_idx] == unsouCD:
                    filterSur.append(line)
            for line in relay_data:
                if line[relay_idx] == unsouCD:
                    filterRelay.append(line)
                
            #hauler = None
            if innerDict['isLess'] == '1':
                if innerDict['isUseRegionForFee'] == '1':
                    if innerDict['isUseRegionForSur'] == '1':
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, less, 
                                                 [],[],
                                                 [],[]),
                                CalcTypeRegion(unsouCD, less, 
                                               filterUntin, untin_col, 
                                               filterSur, sur_col), 
                                CalcTypeRelay(unsouCD, less, 
                                              filterRelay, relay_col),
                                weight
                                )
                    else:
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, less, 
                                                 [],[],
                                                 filterSur, sur_col),
                                CalcTypeRegion(unsouCD, less, 
                                               filterUntin, untin_col, 
                                               [],[]), 
                                CalcTypeRelay(unsouCD, less, 
                                              filterRelay, relay_col),
                                weight
                                )
                else:
                    if innerDict['isUseRegionForSur'] == '1':
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, less, 
                                                 filterUntin, untin_col, 
                                                 [],[]),
                                CalcTypeRegion(unsouCD, less, 
                                               [],[], 
                                               filterSur, sur_col), 
                                CalcTypeRelay(unsouCD, less, 
                                              filterRelay, relay_col),
                                weight
                                )
                    else:
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, less, 
                                                 filterUntin, untin_col, 
                                                 filterSur, sur_col),
                                CalcTypeRegion(unsouCD, less, 
                                               [],[],
                                               [],[]), 
                                CalcTypeRelay(unsouCD, less, 
                                              filterRelay, relay_col),
                                weight
                                )
            else:
                if innerDict['isUseRegionForFee'] == '1':
                    if innerDict['isUseRegionForSur'] == '1':
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, lessEqual, 
                                                 [],[],
                                                 [],[]),
                                CalcTypeRegion(unsouCD, lessEqual, 
                                               filterUntin, untin_col, 
                                               filterSur, sur_col), 
                                CalcTypeRelay(unsouCD, lessEqual, 
                                              filterRelay, relay_col),
                                weight
                                )
                    else:
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, lessEqual, 
                                                 [],[],
                                                 filterSur, sur_col),
                                CalcTypeRegion(unsouCD, lessEqual, 
                                               filterUntin, untin_col, 
                                               [],[]), 
                                CalcTypeRelay(unsouCD, lessEqual, 
                                              filterRelay, relay_col),
                                weight
                                )
                else:
                    if innerDict['isUseRegionForSur'] == '1':
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, lessEqual, 
                                                 filterUntin, untin_col, 
                                                 [],[]),
                                CalcTypeRegion(unsouCD, lessEqual, 
                                               [],[], 
                                               filterSur, sur_col), 
                                CalcTypeRelay(unsouCD, lessEqual, 
                                              filterRelay, relay_col),
                                weight
                                )
                    else:
                        hauler = Hauler(
                                innerDict, 
                                CalcTypeDistance(unsouCD, lessEqual, 
                                                 filterUntin, untin_col, 
                                                 filterSur, sur_col),
                                CalcTypeRegion(unsouCD, lessEqual, 
                                               [],[],
                                               [],[]), 
                                CalcTypeRelay(unsouCD, lessEqual, 
                                              filterRelay, relay_col),
                                weight
                                )

            if hauler is not None:
                haulers.append(hauler)

        return haulers
