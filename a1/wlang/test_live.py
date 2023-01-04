# import unittest

# from . import ast, live


# class TestLive(unittest.TestCase):
#     def test1(self):
#         prg1 = "x := 10; {if x>5 then y := 20 else y:=1} ; z := x+y; print_state"
#         ast1 = ast.parse_string(prg1)

#         v = live.StmtCounter1()
#         # visit the program
#         c = v.visit(ast1)
#         self.assertEqual(c, 6)
