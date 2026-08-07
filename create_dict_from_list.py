from typing import List, Dict
from get_idx import GetIdx

class CreateDictFromList:

    @staticmethod
    def deli_areas(col: List[str], data: List[List[str]], 
                   canGo:str)-> Dict[str, List[str]]:

        arias: Dict[str, List[str]] = {}

        '''indexNoを取得'''
        kubun:int = GetIdx.get_idx(col, 'henkanKBN')
        unsou1:int = GetIdx.get_idx(col, 'unsou1')
        unsou2:int = GetIdx.get_idx(col, 'unsou2')
        unsou3:int = GetIdx.get_idx(col, 'unsou3')
        unsou4:int = GetIdx.get_idx(col, 'unsou4')
        unsou5:int = GetIdx.get_idx(col, 'unsou5')
        unsou6:int = GetIdx.get_idx(col, 'unsou6')
        area1:int = GetIdx.get_idx(col, 'area1')
        area2:int = GetIdx.get_idx(col, 'area2')
        area3:int = GetIdx.get_idx(col, 'area3')
        area4:int = GetIdx.get_idx(col, 'area4')
        area5:int = GetIdx.get_idx(col, 'area5')
        area6:int = GetIdx.get_idx(col, 'area6')

        for line in data:
            if line[kubun] != canGo:
                continue
            innerList: List[str] = []
            for i in range(unsou1, area1):
                if line[i] == ' ':
                    break
                if line[i] in arias:
                    arias[line[i]].append(line[i + 6])
                    continue
                innerList.append(line[i + 6])
                arias[line[i]] = innerList

        return arias








        
        


        return arias
