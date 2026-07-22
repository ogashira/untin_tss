from re import I
import warnings
from typing import List, Any, Tuple, Dict
from abc import ABC, abstractmethod

warnings.filterwarnings('ignore', category=UserWarning)


class IFetchDataForList(ABC):

    @abstractmethod
    def fetch_data(self)-> Tuple[List[str],List[List[Any]]]:
        pass


class FetchMAITEM(IFetchDataForList):
    def __init__(self, cnxn, parts: str) -> None:
        self.cnxn = cnxn
        self._parts = parts

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT AitNam1 AS 'tokuiName',"
                    " AitAddr1 AS 'tokuiAddr',"
                    " AitCD1 AS 'tokuiCD',"
                    " AitCD2 AS 'nonyuCD'"
                    " FROM MAITEM"
                    " WHERE AitKojCD = ' '"
                    " AND AitCD1 LIKE 'T%'"
                    " AND (AitNam1 LIKE '%" + self._parts + "%'"
                    " OR AitAddr1 LIKE '%" + self._parts + "%')"
                    " ORDER BY AitCD1, AitCD2"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f'データベースfetch中に予期せぬエラーです FetchMAITEM') from e
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ


        return columns, data_list


class FetchMDSDST(IFetchDataForList):
    def __init__(self, cnxn, ui_info: Dict[str,str]) -> None:
        self.cnxn = cnxn
        self._factory = ui_info['factory']
        self._tokuiCD = ui_info['tokuiCD']
        self._nonyuCD = ui_info['nonyuCD']
        '''nonyuCD = ' '半角スペースでもWHEREに渡すと''も同じ'''

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT MDSDST_U2002.DsdCompanyCD AS 'unsouCD',"
                    " MDSDST_U2002.DsdDistance AS 'distance',"
                    " MDSDST_U2002.DsdRegionCD AS 'regionCD',"
                    " MNAM.NamNam AS 'regionName',"
                    " MDSDST_U2002.DsdRelayCount AS 'relayCount',"
                    " MDSDST_U2002.DsdIsDisabled AS 'isDisabled',"
                    " MDESTN_U2002.DesSpeCompanyCD AS 'siteiUnsoCD',"
                    " MA_UNS.AitNam1 AS 'unsouName',"
                    " MA_UNS.AitFree1 AS 'isUseRegionForFee'," #地域を使用する:1
                    " MA_UNS.AitFree2 AS 'isUseRegionForSur'," #地域を使用する:1
                    " MA_UNS.AitFree3 AS 'isLess'," #未満:1
                    " MINDEX_U2002.IndSTDay AS 'extraChargeSttday',"
                    " MINDEX_U2002.IndExtraChargeType AS 'extraChargeType',"
                    " MINDEX_U2002.IndFixedFee AS 'fixedFee',"
                    " MINDEX_U2002.IndUnitAmount AS 'unitAmount',"
                    " MINDEX_U2002.IndUnitPrice AS 'unitPrice'"
                    " FROM MDSDST_U2002"
                    " LEFT JOIN MDESTN_U2002"
                    " ON MDSDST_U2002.DsdKojCD = MDESTN_U2002.DesKojCD"
                    " AND MDSDST_U2002.DsdTokCD = MDESTN_U2002.DesTokCD"
                    " AND MDSDST_U2002.DsdNonyuCD = MDESTN_U2002.DesNonyuCD"
                    " LEFT JOIN("
                        " SELECT MAITEM.AitCD1, MAITEM.AitNam1, MAITEM.AitFree1,"
                        " MAITEM.AitFree2, MAITEM.AitFree3"
                        " FROM dbo.MAITEM"
                        " WHERE MAITEM.AitAitKBN = 'A'"
                    ")MA_UNS ON MDSDST_U2002.DsdCompanyCD = MA_UNS.AitCD1"
                    " LEFT JOIN("
                        " SELECT MNAMEM.NamKBN, MNAMEM.NamCD, MNAMEM.NamNam"
                        " FROM dbo.MNAMEM"
                        " WHERE MNAMEM.NamKBN = 'AA'"
                    ")MNAM ON MDSDST_U2002.DsdRegionCD = MNAM.NamCD"
                    " LEFT JOIN MINDEX_U2002"
                    " ON MDSDST_U2002.DsdCompanyCD = MINDEX_U2002.IndCompanyCD"
                    " WHERE MDSDST_U2002.DsdKojCD =" + "'" + self._factory + "'"
                    " AND MDSDST_U2002.DsdTokCD =" + "'" + self._tokuiCD + "'"
                    " AND MDSDST_U2002.DsdNonyuCD =" + "'" + self._nonyuCD + "'"
                    " ORDER BY MDSDST_U2002.DsdTokCD, MDSDST_U2002.DsdNonyuCD"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f'データベースfetch中に予期せぬエラーです FetchMDSDST') from e
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ


        return columns, data_list


class FetchUntin(IFetchDataForList):
    def __init__(self, cnxn, kojCD:str) -> None:
        self.cnxn = cnxn
        self._kojCD = kojCD

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT ShpCompanyCD AS 'unsouCD',"
                    " ShpSTDay AS 'sttDay',"
                    " ShpWeightThreshold AS 'weightThre',"
                    " ShpDistanceThreshold AS 'distanceThre',"
                    " ShpRegionCD AS 'regionCD',"
                    " ShpFee AS 'fee'"
                    " FROM MSHPFE_U2002"
                    " WHERE ShpKojCD=" + "'" + self._kojCD + "'"
                    " ORDER BY ShpCompanyCD, ShpSTDay"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f'データベースfetch中に予期せぬエラーです FetchUntin') from e
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ


        return columns, data_list


class FetchSurcharge(IFetchDataForList):
    def __init__(self, cnxn, kojCD:str) -> None:
        self.cnxn = cnxn
        self._kojCD = kojCD

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT SurCompanyCD AS 'unsouCD',"
                    " SurSTDay AS 'sttDay',"
                    " SurWeightThreshold AS 'weightThre',"
                    " SurDistanceThreshold AS 'distanceThre',"
                    " SurRegionCD AS 'regionCD',"
                    " SurFee AS 'fee'"
                    " FROM MSURCH_U2002"
                    " WHERE SurKojCD=" + "'" + self._kojCD + "'"
                    " ORDER BY SurCompanyCD, SurSTDay"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f'データベースfetch中に予期せぬエラーです FetchSurcharge') from e
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ


        return columns, data_list


class FetchRelay(IFetchDataForList):
    def __init__(self, cnxn, kojCD:str) -> None:
        self.cnxn = cnxn
        self._kojCD = kojCD

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT RelCompanyCD AS 'unsouCD',"
                    " RelSTDay AS 'sttDay',"
                    " RelWeightThreshold AS 'weightThre',"
                    " RelFee AS 'fee'"
                    " FROM MRELYF_U2002"
                    " WHERE RelKojCD=" + "'" + self._kojCD + "'"
                    " ORDER BY RelCompanyCD, RelSTDay"
                    )

        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f'データベースfetch中に予期せぬエラーです FetchRelay') from e
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ


        return columns, data_list


