import datetime
from decimal import Decimal
from typing import List, Dict, Any, Set
from ICalc_type import ICalcType
from get_idx import GetIdx


class Hauler:

    def __init__(self, 
                 unsouDict:Dict[str,Any],
                 calcTypeDistance: ICalcType,
                 calcTypeRegion:ICalcType,
                 calcTypeRelay: ICalcType,
                 weight: float,
                 ) -> None:
        self._unsouDict = unsouDict
        ''' unsouDict = 
        {'unsouCD': 'U0011', 'distance': 30, 'regionCD': '', 'relayCount': 0, 'isDisabled': 0, 'siteiUnsoCD': '', 'unsouName': 'JP', 'isUseRegionForFee': '', 'isUseRegionForSur': '', 'isLess': '', 'extraChargeSttday': '20260401', 'extraChargeType': '2', 'fixedFee': Decimal('0.000000'), 'unitAmount': Decimal('10000.000000'), 'unitPrice': Decimal('10.000000')}
        calcTypesが持っているIThreshold型のインスタンスはLessまたはLessEqualのどちらか。HaulerのisLessに合わせて調整されている。
        '''
        self._calcTypeDistance = calcTypeDistance
        self._calcTypeRegion = calcTypeRegion
        self._weight = weight

    def calc_base_untin(self)-> Decimal:

        base_untin:Decimal = Decimal('0')
        
        if (self._unsouDict['regionCD'] == '' or 
            self._unsouDict['regionCD'] == ' '):
            base_untin = self._calcTypeDistance.calc_base_untin(self._weight, 
                                                 self._unsouDict['distance'])
            return base_untin

        base_untin = self._calcTypeRegion.calc_base_untin(self._weight,
                                                self._unsouDict['regionCD'])

        return Decimal('0')


        


    def calc_srucharge(self)-> Decimal:
        pass

    def calc_relay(self)-> Decimal:
        pass

    def calc_extraCharge(self)-> Decimal:
        pass

