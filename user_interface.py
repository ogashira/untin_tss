import sys
import platform
import csv
from typing import Dict, List
from instance_factory import InstanceFactory
from get_idx import GetIdx
from text_align import TextAlign


class UserInterface(object):
    
    def user_interface(self) -> Dict[str, str]:

        print('どちらから出荷しますか？') 
        print('番号を入力してください')
        print()
        print('1. 本社    2. 土気')
        input_factory:str = input(': ')
        if not (input_factory == '1' or input_factory =='2'):
            print('出荷場所の選択が不正です')
            sys.exit()
        factory:str = '@0002'
        if input_factory == '1':
            factory = '@0001'

        print()
        parts_of_customer_or_address:str = input(
                '顧客名または住所の一部を入力してください\n: ')

        InstanceFactory.get_sql_server_effit()    
        fetchMAITEM = InstanceFactory.get_fetchMAITEM(
                                    parts_of_customer_or_address)
        col, data = fetchMAITEM.fetch_data()

        
        select_list:List[List[str]] = []
        line:List[str] = []
        num:int = 1
        tokuiName_idx:int = GetIdx.get_idx(col, 'tokuiName')
        tokuiAddr_idx:int = GetIdx.get_idx(col, 'tokuiAddr')
        tokuiCD_idx:int = GetIdx.get_idx(col, 'tokuiCD')
        nonyuCD_idx:int = GetIdx.get_idx(col, 'nonyuCD')
        
        newline_col = ['num', 'tokuiName', 'tokuiAddr', 'tokuiCD', 'nonyuCD']
        for line in data:
            newline = [str(num), line[tokuiName_idx], line[tokuiAddr_idx], 
                    line[tokuiCD_idx], line[nonyuCD_idx]]
            select_list.append(newline)
            num += 1
        if num == 1:
            print("入力したキーワードを含む納入先はありません")
            sys.exit()

                
        print('*' * 105)
        no_idx:int = GetIdx.get_idx(newline_col, 'num')
        tokuiName_idx:int = GetIdx.get_idx(newline_col, 'tokuiName')
        tokuiAddr_idx:int = GetIdx.get_idx(newline_col, 'tokuiAddr')
        tokuiCD_idx:int = GetIdx.get_idx(newline_col, 'tokuiCD')
        nonyuCD_idx:int = GetIdx.get_idx(newline_col, 'nonyuCD')

        for line in select_list:
            no:str = line[no_idx]
            name:str = TextAlign.text_align(line[tokuiName_idx], 40, -1, ' ')
            addr:str = TextAlign.text_align(line[tokuiAddr_idx], 40, -1, ' ')
            tokuiCD:str = TextAlign.text_align(line[tokuiCD_idx], 5, -1, ' ')
            nonyuCD:str = TextAlign.text_align(line[nonyuCD_idx], 5, -1, ' ')

            print(f"{no:>3} : {name} : {addr} : {tokuiCD}:{nonyuCD}")
            print('*' * 105)

        print()
        address:str = ''
        original_name:str = ''
        original_tokuiCD:str = ''
        original_nonyuCD:str = ''
        while True:
            selected_number:str = input(
                    '番号を選択してください\n : ')
            try:
                num:int = int(selected_number)
                address = select_list[num -1][tokuiAddr_idx]
                original_name = select_list[num -1][tokuiName_idx]
                original_tokuiCD = select_list[num -1][tokuiCD_idx]
                original_nonyuCD = select_list[num -1][nonyuCD_idx]
            except ValueError:
                print("番号が不正です")
            except IndexError:
                print("入力した番号は存在しません")
            else:
                break

        
        print()
        name:str = TextAlign.text_align(original_name, 40, -1,' ') 
        addr:str = TextAlign.text_align(address, 40, -1,' ') 
        tokCD:str = TextAlign.text_align(original_tokuiCD, 5, -1,' ') 
        nonyuCD:str = TextAlign.text_align(original_nonyuCD, 5, -1,' ') 
        print(f"{selected_number:>3} : {name} : {addr} : {tokCD}:{nonyuCD}")
        print()
        while True:
            weight_str = input(
                    '重量(kg)を入力してください(例：350)\n : '
                    )
            try:
                weight_str = float(weight_str)
                weight_str = str(weight_str)
                break
            except ValueError:
                print("数値が不正です")


        dic_ui_info:Dict[str,str] = {}
        dic_ui_info['factory'] = factory
        dic_ui_info['tokuiCD'] = original_tokuiCD
        dic_ui_info['nonyuCD'] = original_nonyuCD
        dic_ui_info['weight_str'] = weight_str
        dic_ui_info['address'] = address

        return dic_ui_info
