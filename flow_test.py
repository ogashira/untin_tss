from user_interface import *
from typing import Dict, List, Any
from instance_factory import InstanceFactory
from fetch_data_for_list import IFetchDataForList
from hauler import Hauler


class ProgramFlowTest(object):

    '''
    1. 出荷工場を選択してもらう
    2. 行き先の住所または得意先名の一部を入力してもらう
    3. fetch MAITEM AitCD1, AitCD2, AitNam1, AitAddr1 
    4. AitNam1, AitAddr1を番号付きで表示
    5. 行き先を決定する (tokuiCD, nonyuCD)
    6. 荷物の重さweightを入力してもらう
    7. fetch MDSDST_U2002  DsdDistance, DsdRelayCount, DsdIsDisabled(DsdKojCD,DsdTokCD, DsdNonyuCD で絞る) 運送屋の候補、距離、地域、中継回数、行く行かない が取れる。
    8. fetch MDESTN_U2002 DesSpeCompanyCD(DesKojCD,DesTokCD, DesNonyuCD で絞る)顧客指定運送屋が取れる
    9. MAITEMで重量閾値判定区分が未満：1、以下：""を得ておく

        [{'unsouCD': 'U0011', 'distance': 30, 'regionCD': '', 'relayCount': 0, 'isDisabled': 0, 'siteiUnsoCD': '', 'unsouName': 'JP', 'isUseRegionForFee': '', 'isUseRegionForSur': '', 'isLess': '', 'extraChargeSttday': '20260401', 'extraChargeType': '2', 'fixedFee': Decimal('0.000000'), 'unitAmount': Decimal('10000.000000'), 'unitPrice': Decimal('10.000000')}, {'unsouCD': 'U0012', 'distance': 30, 'regionCD': '', 'relayCount': 0, 'isDisabled': 0, 'siteiUnsoCD': '', 'unsouName': 'JP_奈良広島', 'isUseRegionForFee': '', 'isUseRegionForSur': '', 'isLess': '', 'extraChargeSttday': '20260401', 'extraChargeType': '2', 'fixedFee': Decimal('0.000000'), 'unitAmount': Decimal('10000.000000'), 'unitPrice': Decimal('10.000000')}]

    10. fetch MSHPFE_U2002 ShpSTDay, ShpWeightThreshold, ShpDistanceThreshold(ShpKojCD,ShpCompanyCDで絞る) 運賃表
    11. fetch MSURCH_U2002 サーチャージ
    12. fetch MRELYF_U2002  中継料
    12. U0009, U0011 のインスタンスを作る
        12-1. set(ShpSTDay)を作る。today よりも小さくて最大のshpSTDayを求める。(適用開始日)
        12-2. set(ShpWeightThreshould)を作る。weightが該当する数値を求める
        12-3. set(ShpDistanceThreshold)を作る。distanceが該当する数値を求める
        12-4. 運賃を求める。
    '''

    def _create_list_dict(self, col:List[str], 
                                data:List[List[Any]]) -> List[Dict[str,Any]]:
        listDict = []
        for line in data:
            innerDict = dict(zip(col, line))
            listDict.append(innerDict)

        return listDict


    def start(self) -> None:
        ui:UserInterface = UserInterface()
        dic_ui_info:Dict[str,str] = ui.user_interface()
        '''{'factory': '@0002', 'tokuiCD': 'T1210', 'nonyuCD': 'H127', 
        'weight_str': '256.0'} '''

        # ' 'と''が混在している
        fetchMDSDST:IFetchDataForList = \
                                      InstanceFactory.get_fetchMDSDST(dic_ui_info)
        dsd_col, dsd_data = fetchMDSDST.fetch_data()


        unsouListDict: List[Dict[str,Any]] = \
                                self._create_list_dict(dsd_col, dsd_data)
        '''
        [{'unsouCD': 'U0011', 'distance': 30, 'regionCD': '', 'relayCount': 0, 'isDisabled': 0, 'siteiUnsoCD': '', 'unsouName': 'JP', 'isUseRegionForFee': '', 'isUseRegionForSur': '', 'isLess': '', 'extraChargeSttday': '20260401', 'extraChargeType': '2', 'fixedFee': Decimal('0.000000'), 'unitAmount': Decimal('10000.000000'), 'unitPrice': Decimal('10.000000')}, {'unsouCD': 'U0012', 'distance': 30, 'regionCD': '', 'relayCount': 0, 'isDisabled': 0, 'siteiUnsoCD': '', 'unsouName': 'JP_奈良広島', 'isUseRegionForFee': '', 'isUseRegionForSur': '', 'isLess': '', 'extraChargeSttday': '20260401', 'extraChargeType': '2', 'fixedFee': Decimal('0.000000'), 'unitAmount': Decimal('10000.000000'), 'unitPrice': Decimal('10.000000')}]
        '''

        '''運賃、サーチャージ、中継料を取得'''
        fetchUntin = InstanceFactory.get_fetchUntin(dic_ui_info['factory'])
        untin_col, untin_data = fetchUntin.fetch_data()

        fetchSurcharge = InstanceFactory.get_fetchSurcharge(dic_ui_info['factory'])
        sur_col, sur_data = fetchSurcharge.fetch_data()

        fetchRelay = InstanceFactory.get_fetchRelay(dic_ui_info['factory'])
        relay_col, relay_data = fetchRelay.fetch_data()


        '''運賃、サーチャージ、中継料をunsouListDictに追加する
        それぞれのcolのリストも同時に追加する
        self.add_List_to_unsouListDict(unsouListDict, untin_data, 
                                       untin_col, 'untin')
        self.add_List_to_unsouListDict(unsouListDict, sur_data, 
                                       sur_col, 'surcharge')
        self.add_List_to_unsouListDict(unsouListDict, relay_data, 
                                       relay_col, 'relay')
        '''


        weight:float = float(dic_ui_info['weight_str'])

        # Haulerインスタンスの配列を作成する
        haulers:List[Hauler] = InstanceFactory.get_Haulers(unsouListDict,
                                                           untin_data,
                                                           untin_col,
                                                           sur_data,
                                                           sur_col,
                                                           relay_data,
                                                           relay_col,
                                                           weight
                                                           )

        '''cnxnの消去  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        InstanceFactory.delete_cnxn()
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        
        for hauler in haulers:
            hauler.calc_base_untin()


    '''
    def add_List_to_unsouListDict(self,
                                  unsouListDict:List[Dict[str,Any]],
                                  data:List[List[Any]],
                                  col: List[str],
                                  key: str) -> None:
        unsouCD:U0011 でフィルターしたdataをunsouListDictに追加する
        そのデータのcolもunsouListDictに追加する
        idx:int = GetIdx.get_idx(col, 'unsouCD')
        for innerDict in unsouListDict:
            unsouCD:str = innerDict['unsouCD']
            newLines:List[List[Any]] = []
            for line in data:
                if line[idx] == unsouCD:
                    newLines.append(line)
            innerDict[key] = newLines
            key_col:str = key + '_col'
            innerDict[key_col] = col
            '''
