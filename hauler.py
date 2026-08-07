import datetime
from decimal import Decimal
from re import I
from typing import List, Dict, Any, Set
from ICalc_type import ICalcType
from get_idx import GetIdx
from text_align import TextAlign


class Hauler:

    def __init__(self, 
                 unsouDict:Dict[str,Any],
                 calcUntin: ICalcType,
                 calcSur:ICalcType,
                 calcTypeRelay: ICalcType,
                 weight: float,
                 deliveryAreas: Dict[str, str],
                 undeliveryAreas: Dict[str, str],
                 address: str
                 ) -> None:
        self._unsouDict = unsouDict
        ''' unsouDict = 
        {'unsouCD': 'U0011', 'distance': 30, 'regionCD': '', 'relayCount': 0, 'isDisabled': 0, 'siteiUnsoCD': '', 'unsouName': 'JP', 'isUseRegionForUntin': '', 'isUseRegionForSur': '', 'isLess': '', 'extraChargeSttday': '20260401', 'extraChargeType': '2', 'fixedFee': Decimal('0.000000'), 'unitAmount': Decimal('10000.000000'), 'unitPrice': Decimal('10.000000')}
        calcTypesが持っているIThreshold型のインスタンスはLessまたはLessEqualのどちらか。HaulerのisLessに合わせて調整されている。
        '''
        self._calcUntin = calcUntin
        self._calcSur = calcSur
        self._calcTypeRelay = calcTypeRelay
        self._weight = weight
        self._deliveryAreas = deliveryAreas
        self._undeliveryAreas = undeliveryAreas
        self._address = address

        # canGoがFalseの場合は運賃計算しない。結果表示もしない。
        self._canGo: bool = self._judge_canGo()

        self._fee = self._calc_fee()

        '''
        # TODO
        print(self._unsouDict['unsouName'])
        print(f'isDisabled: {self._unsouDict["isDisabled"]}')
        print(self._canGo)
        print(f"extraChargeType = {[self._unsouDict['extraChargeType']]}")  
        print(f'運賃= {self._fee}')
        print('=' * 20)
        '''


    def show_untin(self)-> None:
        if not self._canGo:
            return

        unsouName:str = TextAlign.text_align(self._unsouDict['unsouName'], 
                                                                14, -1, ' ')

        untin_s:str = TextAlign.text_align(f'{int(self._fee):,}',
                                                                  9, 1, ' ')

        if self._unsouDict['extraChargeType'] == '2':
            unitAmount:str = f"{int(self._unsouDict['unitAmount']):,}"
            unitPrice:str = f"{int(self._unsouDict['unitPrice']):,}"
            print(f'{unsouName} : {untin_s} <- 売価 {unitAmount}円につき {unitPrice}円追加')
            return

        if self._unsouDict['extraChargeType'] == '1':
            fixedFee:str = f"{int(self._unsouDict['fixedFee']):,}"
            print(f'{unsouName} : {untin_s} <- 一律 {fixedFee}円追加')

        print(f'{unsouName} : {untin_s}')





    def show_siteiUnso(self)-> None:
        if self._unsouDict['siteiUnsoCD'] == self._unsouDict['unsouCD']:
            print(f'顧客指定運送屋 : {self._unsouDict["unsouName"]}')



    def _judge_canGo(self)-> bool:
        # 行く行かないが1の場合はFalse
        if self._unsouDict['isDisabled'] == 1:
            return False
        
        # 自分のCDがdeliveryAreasのキーにあり、そのリストの地名が自分のaddressに
        # 含まれていなかったらFalse
        tmpFlug: bool = False
        if self._unsouDict['unsouCD'] in self._deliveryAreas:
            for area in self._deliveryAreas[self._unsouDict['unsouCD']]:
                if area in self._address:
                    tmpFlug = True 
            return tmpFlug
        
        # 自分のCDがundeliveryAreasのキーにあり、そのリストの地名が自分のaddressに
        # 含まれていたらFalse
        if self._unsouDict['unsouCD'] in self._undeliveryAreas:
            for area in self._undeliveryAreas[self._unsouDict['unsouCD']]:
                if area in self._address:
                    return False

        #undeliveryArea, deliveryAreaに無ければTrue
        return True


    def _calc_fee(self)-> Decimal:

        if not self._canGo:
            return Decimal('0')

        fee: Decimal = Decimal('0')
        base_untin:Decimal = Decimal('0')
        surcharge: Decimal = Decimal('0')
        relay: Decimal = Decimal('0')
        extraCharge: Decimal = Decimal('0')

        base_untin = self._calc_base_untin()
        surcharge = self._calc_srucharge()
        relay = self._calc_relay()
        #extraCharge = self._calc_extraCharge()

        fee = base_untin + surcharge + relay #+ extraCharge
        # ベース運賃が0なら計算不能でトータル0
        if base_untin == Decimal('0'):
            fee = Decimal('0')
        return fee

    
    def _calc_base_untin(self)-> Decimal:
        if (self._unsouDict['isUseRegionForUntin'] == '' or 
            self._unsouDict['isUseRegionForUntin'] == ' '):
            base_untin = self._calcUntin.calc_fee(self._weight, 
                                                self._unsouDict['distance'])
            return base_untin

        base_untin = self._calcUntin.calc_fee(self._weight,
                                                self._unsouDict['regionCD'])
        return base_untin


    def _calc_srucharge(self)-> Decimal:
        if (self._unsouDict['isUseRegionForSur'] == '' or 
            self._unsouDict['isUseRegionForSur'] == ' '):
            surcharge = self._calcSur.calc_fee(self._weight, 
                                                 self._unsouDict['distance'])
            return surcharge

        surcharge = self._calcSur.calc_fee(self._weight,
                                                self._unsouDict['regionCD'])
        return surcharge

    def _calc_relay(self)-> Decimal:
        if self._unsouDict['relayCount'] == 0:
            return Decimal('0')

        relay = self._calcTypeRelay.calc_fee(self._weight, 
                                             self._unsouDict['relayCount'])
        return relay



    def _calc_extraCharge(self)-> Decimal:
        pass

