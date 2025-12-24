# 中文字符检查器 <u>Ch</u>inese <u>Ch</u>ar Checker

---

## 用法示例

```python
from ch3 import ChineseCharChecker
checker = ChineseCharChecker()
print(checker.check('汉'))          # True
print(checker.check('A'))          # False
print(checker.any('Hello汉字'))   # True
print(checker.all('汉字测试'))     # True
print(checker.all('汉字Test'))     # False
checker.add_extra('⭐')            # 将“⭐”视为中文字符
print(checker.check('⭐'))          # True
checker.exclude_chr('靰')         # 将'靰'从中文字符中移除
print(checker.check('靰'))          # False
```

---

## ChineseCharChecker

### 方法：

    - check 检查传入的字符是否为中文字符，若传入字符串，只检查头部字符
    - any 检查传入的字符串中是否包含至少一个中文字符
    - all 检查传入的字符串中是否全部是中文字符
    - add_extra 将传入的字符视为中文字符，应用于后续检查，会覆盖原先的exclude_chr
    - exclude_chr 将传入的字符视为非中文字符，应用于后续检查，会覆盖原先的add_extra

### 属性：

    - swt_general 是否包含常用汉字（默认 True）
    - swt_extA, swt_extB, swt_extC, swt_extD, swt_extE
        , swt_extF, swt_extG, swt_extH 是否包含拓展A~H区（默认均为 True）
    - swt_com 是否包含兼容汉字（默认 True）
    - swt_comsupp 是否包含兼容汉字补充（默认 True）
    - swt_kxradical 是否包含康熙部首（默认 True）
    - swt_radical 是否包含部首补充（默认 True）
    - swt_stroke 是否包含汉字笔画（默认 True）
    - swt_zero 是否包含汉字数字零（默认 True）

### 注意：

    - 中文字符包括汉字、部首、笔画、偏僻字等，但不包含任何标点符号

---
