import unittest

from jaxtools.basetypes import *

class TestBaseTypes(unittest.TestCase):
    def test_isBaseTypeBasic(self):
        d = {}
        l = []
        t = ()
        self.assertTrue(isBaseType(None), "None should be valid base type. (Null)")
        self.assertTrue(isBaseType(1001), "Integer should be valid base type. (Int)")
        self.assertTrue(isBaseType(-1001), "Integer should be valid base type. (Int)")
        self.assertTrue(isBaseType(1001.001), "Float or double should be valid base type. (Num)")
        self.assertTrue(isBaseType(-1001.001), "Float or double should be valid base type. (Num)")
        self.assertTrue(isBaseType("Regular String"), "String should be valid base type. (String)")
        self.assertTrue(isBaseType(u"Unicode String"), "Unicode String should be valid base type. (String)")
        self.assertTrue(isBaseType(None), "None should be valid base type. (Null)")
        self.assertTrue(isBaseType(None), "None should be valid base type. (Null)")
        self.assertTrue(isBaseType(None), "None should be valid base type. (Null)")
        self.assertTrue(isBaseType(d), "Empty dictionary should be valid base type. (Dict)")
        self.assertTrue(isBaseType(l), "Empty list should be valid base type. (List)")
        self.assertTrue(isBaseType(t), "Empty tuple should be valid base type. (List)")
        self.assertFalse(isBaseType(self), "Test class should not be valid base type.")

if __name__ == '__main__':
    unittest.main()
