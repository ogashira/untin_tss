from typing import Dict, TYPE_CHECKING, Any, List, Tuple
import platform
import sys
from fetch_data_for_list import IFetchDataForList

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
                                         weight:float) -> List['Hauler']:

        from IThreshold import IThreshold
        from less import Less
        from less_equal import LessEqual
        from ICalc_type import ICalcType
        from calc_type_relay import CalcTypeRelay
        from calc_type_distance import CalcTypeDistance
        from calc_type_region import CalcTypeRegion
        from hauler import Hauler

        thresholds: Dict[str, IThreshold] = {}
        thresholds['less'] = Less()
        thresholds['lessEqual'] = LessEqual()

        calcTypes: Dict[str, ICalcType] = {}
        calcTypes['relay'] = CalcTypeRelay(thresholds)
        calcTypes['distance'] = CalcTypeDistance(thresholds)
        calcTypes['region'] = CalcTypeRegion(thresholds)

        haulers:List[Hauler] = []
        for line in unsouListDict:
            haulers.append(Hauler(line, calcTypes, weight))

        return haulers
