import unicodedata

class TextAlign:

    @staticmethod
    def text_align(text, width, align=-1, fill_char=' ')->str:
        '''
        全角／半角が混在するテキストを
        指定の長さ（半角換算）になるように空白などで埋める
        
        width: 半角換算で文字数を指定
        align: -1 -> left, 1 -> right
        fill_char: 埋める文字を指定

        return: 空白を埋めたテキスト（'abcde     '）
        '''
        
        def get_han_count(text) -> int:
            '''
            全角文字は[2],半角文字は[1]として文字列の長さを計算する
            '''
            count = 0

            for char in text:
                if unicodedata.east_asian_width(char) in 'FWA':
                    count += 2
                else:
                    count += 1
            return count

        fill_count:int = width - get_han_count(text)
        if (fill_count <= 0): return text

        if align < 0:
            return text + fill_char*fill_count
        else:
            return fill_char*fill_count + text
        

