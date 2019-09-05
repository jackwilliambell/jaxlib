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

    def test_isBaseTypeDictSimple(self):
        dgood = {"first": 1, "second": 2, "nested": {"isNested": True}}
        dbad1 = {"first": 1, True: 2}
        dbad2 = {"first": 1, "second": 2, "nested": {"isNested": self}}
        self.assertTrue(isBaseType(dgood), "Simple nested dict containing only basetypes is valid base type.")
        self.assertFalse(isBaseType(dbad1), "Simple dict containing non-string key is not valid base type.")
        self.assertFalse(isBaseType(dbad2), "Simple nested dict containing non basetypes is not valid base type.")

    def test_isBaseTypeListSimple(self):
        lgood = [1, "two", [True, 3]]
        lbad1 = [1, "two", self]
        lbad2 = [1, "two", [True, self]]
        self.assertTrue(isBaseType(lgood), "Simple nested list containing only basetypes is valid base type.")
        self.assertFalse(isBaseType(lbad1), "Simple list containing non basetypes is not valid base type.")
        self.assertFalse(isBaseType(lbad2), "Simple nested list containing non basetypes is not valid base type.")

    def test_isBaseTypeDictComplex(self):
        dgood = {"first": 1, "second": 2, "nested": {"isNested": [1, 2, None, {"isDeeperNested": True}]}}
        dbad1 = {"first": 1, "second": 2, "nested": {"isNested": [1, 2, None, {1: True}]}}
        dbad2 = {"first": 1, "second": 2, "nested": {"isNested": [1, 2, None, {"isDeeperNested": self}]}}
        self.assertTrue(isBaseType(dgood), "Complex nested dict containing only basetypes is valid base type.")
        self.assertFalse(isBaseType(dbad1), "Complex dict containing non-string key is not valid base type.")
        self.assertFalse(isBaseType(dbad2), "Complex nested dict containing non basetypes is not valid base type.")
        # TODO: Add even more complex nested dicts and lists.


if __name__ == '__main__':
    unittest.main()
