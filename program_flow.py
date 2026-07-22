from user_interface import *
from hauler_factory import *
from typing import Dict


class ProgramFlow(object):

    '''
    1. 出荷工場を選択してもらう
    2. 行き先の住所または得意先名の一部を入力してもらう
    3. fetch MAITEM AitCD1, AitCD2, AitNam1, AitAddr1 
    4. AitNam1, AitAddr1を番号付きで表示
    5. 行き先を決定する (tokuiCD, nonyuCD)
    6. 荷物の重さweightを入力してもらう
    7. fetch MDSDST_U2002  DsdDistance, DsdRelayCount, DsdIsDisabled(DsdKojCD,DsdTokCD, DsdNonyuCD で絞る) 運送屋の候補、距離、地域、中継回数、行く行かない が取れる。
    8. {'U0009': {distance: 100, relayCount: 0, isDisabled: 0}, 'U0011':{distance:50, relayCount:0, isDisabled:0}...}
    9. fetch MDESTN_U2002 DesSpeCompanyCD(DesKojCD,DesTokCD, DesNonyuCD で絞る)顧客指定運送屋が取れる
    10. fetch MSHPFE_U2002 ShpSTDay, ShpWeightThreshold, ShpDistanceThreshold(ShpKojCD,ShpCompanyCDで絞る) 運賃表
    11. fetch MSURCH_U2002 サーチャージ
    12. fetch MRELYF_U2002  中継料
    11. MAITEMで重量閾値判定区分が未満：1、以下：""を得ておく
    12. U0009, U0011 のインスタンスを作る
        12-1. set(ShpSTDay)を作る。today よりも小さくて最大のshpSTDayを求める。(適用開始日)
        12-2. set(ShpWeightThreshould)を作る。weightが該当する数値を求める
        12-3. set(ShpDistanceThreshold)を作る。distanceが該当する数値を求める
        12-4. 運賃を求める。
    '''

    def start(self) -> None:
        ui:UserInterface = UserInterface()
        dic_ui_info:Dict[str,str] = ui.user_interface()
        '''{'factory': '@0002', 'tokuiCD': 'T1210', 'nonyuCD': 'H127', 
        'weight_str': '256.0'} '''



        torr:IHauler =HaulerFactory.create_torr()
        niigata:IHauler= HaulerFactory.create_niigata()
        keihin:IHauler = HaulerFactory.create_keihin()
        seinou:IHauler = HaulerFactory.create_seinou()
        untin_torr:float = torr.calc_fare(
                        int(dic_unsoutaiou_info['torr_dist']),
                        float(dic_unsoutaiou_info['weight']),
                        dic_unsoutaiou_info['torr_yes_no'],
                        int(dic_unsoutaiou_info['torr_relay']),
                        dic_unsoutaiou_info['address'],
                        )

        untin_niigata:float = niigata.calc_fare(
                        int(dic_unsoutaiou_info['niigata_dist']),
                        float(dic_unsoutaiou_info['weight']),
                        dic_unsoutaiou_info['niigata_yes_no'],
                        int(dic_unsoutaiou_info['niigata_relay'])
                        )  

        '''
        ケイヒンの運賃表は横軸が重量、縦軸が行先（横浜、静岡..など）
        dictは0(使用しない)とし、縦軸の行先を仮引数addressに設定する
        '''
        untin_keihin:float = keihin.calc_fare(
                        0,
                        float(dic_unsoutaiou_info['weight']),
                        YN = dic_unsoutaiou_info['keihin_yes_no'],
                        )

        untin_seinou:float = seinou.calc_fare(
                        int(dic_unsoutaiou_info['seinou_dist']),
                        float(dic_unsoutaiou_info['weight'])
                        )

        print()
        print(f'トール  の運賃 :  {untin_torr: >7} 円')
        print(f'新  潟  の運賃 :  {untin_niigata: >7} 円')
        print(f'西  濃  の運賃 :  {untin_seinou: >7} 円')
        print(f'ケイヒンの運賃 :  {untin_keihin: >7} 円')
        print()
        print(f'顧客指定運送屋 :  {dic_unsoutaiou_info["sitei"]}')
        print()



