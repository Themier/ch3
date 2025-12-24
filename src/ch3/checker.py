
"""
    python 内置相关函数：
        chr 接受一个整数参数，返回以该整数为码点的字符
            chr(19968) = chr(0x4e00) = '一'
        ord 接受一个字符参数，返回该字符的码点
        hex 接受一个整数，返回其十六进制字符串

"""

from typing import Tuple


class ChineseCharChecker():
    """中文字符检查器
        方法：
            check 检查字符是否为中文字符，若传入字符串，只检查头部字符
            any 检查字符串中是否包含至少一个中文字符
            all 检查字符串中是否全部是中文字符
            add_extra 将指定字符视为中文字符
            exclude_chr 从中文字符中移除指定字符

        属性：
            swt_general 是否包含常用汉字（默认 True）
            swt_extA, swt_extB, swt_extC, swt_extD, swt_extE
                , swt_extF, swt_extG, swt_extH 是否包含拓展A~H区（默认均为 True）
            swt_com 是否包含兼容汉字（默认 True）
            swt_comsupp 是否包含兼容汉字补充（默认 True）
            swt_kxradical 是否包含康熙部首（默认 True）
            swt_radical 是否包含部首补充（默认 True）
            swt_stroke 是否包含汉字笔画（默认 True）
            swt_zero 是否包含汉字数字零（默认 True）

        注意：
            中文字符包括汉字、部首、笔画、偏僻字等，但不包含任何标点符号
    """
    range_general:Tuple[int, int] = (0x4E00, 0x9FFF + 1)  # CJK Unified Ideographs 最常用的“中日韩统一表意文字”第一块
    range_extA:Tuple[int, int] = (0x3400, 0x4DBF + 1)  # CJK 拓展A区
    range_extB:Tuple[int, int] = (0x20000, 0x2A6DF + 1)  # CJK 拓展，B~H区拓展字符需要额外安装字体才能正常显示
    range_extC:Tuple[int, int] = (0x2A700, 0x2B73F + 1)  # CJK 拓展
    range_extD:Tuple[int, int] = (0x2B740, 0x2B81F + 1)  # CJK 拓展
    range_extE:Tuple[int, int] = (0x2B820, 0x2CEAF + 1)  # CJK 拓展
    range_extF:Tuple[int, int] = (0x2CEB0, 0x2EBEF + 1)  # CJK 拓展
    range_extG:Tuple[int, int] = (0x30000, 0x3134F + 1)  # CJK 拓展
    range_extH:Tuple[int, int] = (0x31350, 0x323AF + 1)  # CJK 拓展
    range_compat:Tuple[int, int] = (0xF900, 0xFAFF + 1)  # 兼容汉字
    range_compat_supp:Tuple[int, int] = (0x2F800, 0x2FA1F + 1)  # 兼容汉字补充
    range_kangxi_radical:Tuple[int, int] = (0x2F00, 0x2FDF + 1)  # 康熙部首
    range_radical:Tuple[int, int] = (0x2E80, 0x2EFF + 1)  # 部首补充
    range_stroke:Tuple[int, int] = (0x31C0, 0x31EF + 1)  # 汉字笔画
    range_zero:Tuple[int, int] = (0x3007, 0x3007+1) # 汉字数字零〇

    def __init__(self):
        self.swt_general:bool = True     # switch of general character 默认包含常用汉字
        self.swt_extA:bool = True        # 默认包含拓展A~H区
        self.swt_extB:bool = True       
        self.swt_extC:bool = True       
        self.swt_extD:bool = True       
        self.swt_extE:bool = True       
        self.swt_extF:bool = True       
        self.swt_extG:bool = True       
        self.swt_extH:bool = True       
        self.swt_com:bool = True         # 默认包含兼容汉字
        self.swt_comsupp:bool = True    # 默认包含兼容汉字补充
        self.swt_kxradical:bool = True   # 默认包含康熙部首
        self.swt_radical:bool = True     # 默认包含部首补充
        self.swt_stroke:bool = True      # 默认包含汉字笔画
        self.swt_zero:bool = True        # 默认包含汉字数字零

        self._extra_chinese_chr:set = set()  # 额外包含的中文字符集合
        self._exclude_chr:set = set()         # 排除的中文字符集合
        return

    def add_extra(self, c:str):
        """添加额外的中文字符
        如果字符已经在排除集合中，则从排除集合中移除
        """
        if c and isinstance(c, str):
            for ch in c:
                if ch in self._exclude_chr:
                    self._exclude_chr.remove(ch)
                self._extra_chinese_chr.add(ch)
        return

    def exclude_chr(self, c:str):
        """排除中文字符
        如果字符已经在额外包含集合中，则从额外包含集合中移除
        """
        if c and isinstance(c, str):
            for ch in c:
                if ch in self._extra_chinese_chr:
                    self._extra_chinese_chr.remove(ch)
                self._exclude_chr.add(ch)
        return

    def check(self, c:str):
        """判断传入的字符是不是中文字符
        如果字符串长度大于1，只判断头部
        空字符串不是中文字符

        首先检查字符是否存在于 _extra_chinese_chr 中，然后检查字符是否在 _exclude_chr 中
        ，最后检查字符是否在各个码点范围内
        """
        if not c or not isinstance(c, str):
            return False
        c = c[0]
        if c in self._extra_chinese_chr:
            return True
        if c in self._exclude_chr:
            return False
        code = ord(c)
        if self.swt_general and self.range_general[0] <= code < self.range_general[1]:
            return True
        if self.swt_extA and self.range_extA[0] <= code < self.range_extA[1]:
            return True
        if self.swt_extB and self.range_extB[0] <= code < self.range_extB[1]:
            return True
        if self.swt_extC and self.range_extC[0] <= code < self.range_extC[1]:
            return True
        if self.swt_extD and self.range_extD[0] <= code < self.range_extD[1]:
            return True
        if self.swt_extE and self.range_extE[0] <= code < self.range_extE[1]:
            return True
        if self.swt_extF and self.range_extF[0] <= code < self.range_extF[1]:
            return True
        if self.swt_extG and self.range_extG[0] <= code < self.range_extG[1]:
            return True
        if self.swt_extH and self.range_extH[0] <= code < self.range_extH[1]:
            return True
        if self.swt_com and self.range_compat[0] <= code < self.range_compat[1]:
            return True
        if self.swt_comsupp and self.range_compat_supp[0] <= code < self.range_compat_supp[1]:
            return True
        if self.swt_kxradical and self.range_kangxi_radical[0] <= code < self.range_kangxi_radical[1]:
            return True
        if self.swt_radical and self.range_radical[0] <= code < self.range_radical[1]:
            return True
        if self.swt_stroke and self.range_stroke[0] <= code < self.range_stroke[1]:
            return True
        if self.swt_zero and self.range_zero[0] <= code < self.range_zero[1]:
            return True
        return False

    def any(self, s:str):
        """判断字符串中是否有至少一个中文字符"""
        if not s or not isinstance(s, str):
            return False
        return any(self.check(c) for c in s)
    
    def all(self, s:str):
        """判断字符串中是否全部是中文字符"""
        if not s or not isinstance(s, str):
            return False
        return all(self.check(c) for c in s)

