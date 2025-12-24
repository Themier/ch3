
""" 单元测试

"""

import unittest, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from ch3 import ChineseCharChecker


class TestChineseCharChecker(unittest.TestCase):

    def setUp(self):
        self.checker = ChineseCharChecker()

    # -------------------
    # 测试 check 方法
    # -------------------

    def test_check_single_common_chinese_char(self):
        self.assertTrue(self.checker.check('一'))  # U+4E00
        self.assertTrue(self.checker.check('中'))
        self.assertTrue(self.checker.check('国'))

    def test_check_non_chinese_char(self):
        self.assertFalse(self.checker.check('a'))
        self.assertFalse(self.checker.check('1'))
        self.assertFalse(self.checker.check('！'))  # 中文标点，应为 False
        self.assertFalse(self.checker.check(' '))

    def test_check_empty_string(self):
        self.assertFalse(self.checker.check(''))

    def test_check_none_input(self):
        self.assertFalse(self.checker.check(None))

    def test_check_long_string(self):
        self.assertTrue(self.checker.check('你好世界'))  # 只检查首字符 '你'
        self.assertFalse(self.checker.check('a你好'))   # 首字符 'a'

    def test_check_extA_char(self):
        # U+3400 是 CJK Ext A 起始
        self.assertTrue(self.checker.check(chr(0x3400)))

    def test_check_kangxi_radical(self):
        self.assertTrue(self.checker.check(chr(0x2F00)))  # 康熙部首起始

    def test_check_radical_supplement(self):
        self.assertTrue(self.checker.check(chr(0x2E80)))

    def test_check_stroke(self):
        self.assertTrue(self.checker.check(chr(0x31C0)))

    def test_check_zero(self):
        self.assertTrue(self.checker.check('〇'))  # U+3007

    def test_check_compat(self):
        self.assertTrue(self.checker.check(chr(0xF900)))

    def test_check_compat_supp(self):
        self.assertTrue(self.checker.check(chr(0x2F800)))

    # -------------------
    # 测试开关功能（toggle ranges）
    # -------------------

    def test_disable_general_range(self):
        self.checker.swt_general = False
        self.assertFalse(self.checker.check('中'))
        self.assertTrue(self.checker.check('〇'))  # zero still enabled

    def test_disable_all_ranges(self):
        for attr in [attr for attr in dir(self.checker) if attr.startswith('swt_')]:
            setattr(self.checker, attr, False)
        self.assertFalse(self.checker.check('中'))
        self.assertFalse(self.checker.check('〇'))

    def test_exclude_char(self):
        self.checker.exclude_chr('中')
        self.assertFalse(self.checker.check('中'))

    def test_add_extra_char(self):
        self.checker.add_extra('€')
        self.assertTrue(self.checker.check('€'))

    def test_exclude_overrides_extra(self):
        self.checker.add_extra('€')
        self.checker.exclude_chr('€')
        self.assertFalse(self.checker.check('€'))

    def test_extra_overrides_exclude(self):
        self.checker.exclude_chr('€')
        self.checker.add_extra('€')
        self.assertTrue(self.checker.check('€'))

    # -------------------
    # 测试 any 方法
    # -------------------

    def test_any_contains_chinese(self):
        self.assertTrue(self.checker.any("Hello 世界!"))

    def test_any_no_chinese(self):
        self.assertFalse(self.checker.any("Hello World!"))

    def test_any_empty_string(self):
        self.assertFalse(self.checker.any(""))

    def test_any_none_input(self):
        self.assertFalse(self.checker.any(None))

    # -------------------
    # 测试 all 方法
    # -------------------

    def test_all_all_chinese(self):
        self.assertTrue(self.checker.all("中文测试"))

    def test_all_mixed(self):
        self.assertFalse(self.checker.all("中文123"))

    def test_all_no_chinese(self):
        self.assertFalse(self.checker.all("abc"))

    def test_all_empty(self):
        self.assertFalse(self.checker.all(""))

    def test_all_none_input(self):
        self.assertFalse(self.checker.all(None))

    # -------------------
    # 测试 check_series 方法
    # -------------------

    def test_check_series(self):
        result = self.checker.check_series("a中1国")
        expected = [False, True, False, True]
        self.assertEqual(result, expected)

    def test_check_series_empty(self):
        self.assertEqual(self.checker.check_series(""), [])
        self.assertEqual(self.checker.check_series(None), [])

    # -------------------
    # 边界测试：ExtB~H（高码点）
    # -------------------

    def test_check_extB_char(self):
        self.assertTrue(self.checker.check(chr(0x20000)))

    def test_check_extH_char(self):
        self.assertTrue(self.checker.check(chr(0x31350)))


if __name__ == '__main__':
    unittest.main()