import unittest

from . import ast, stats_visitor


class TestStatsVisitor(unittest.TestCase):
    # test Stmt, StmtList, AsgnStmt
    def test_1(self):
        prg1 = "x:=1; y:=-10"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        # UNCOMMENT to run the test
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 2)

    def test_if1(self):
        # define undefined vars on purpose
        # they should be counted
        prg1 = "x:=1;if x>0 then y:=z+1 else y:=z-1"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 4)
        self.assertEquals(sv.get_num_vars(), 3)
    
    def test_if2(self):
        # define undefined vars on purpose
        # they should be counted
        prg1 = "x:=1;if x=0 then y:=z+1"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 3)

    def test_while(self):
        prg1 = "x:=5; while x>0 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 1)

    def test_assert(self):
        prg1 = "assert (x<y and y<z+1)"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 3)
    
    def test_assume(self):
        prg1 = "assume w=100"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 1)

    def test_havoc(self):
        prg1 = "havoc a,b,c"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 3)

    def test_stmtList_None(self):
        stmt_list = ast.StmtList(None)
        sv = stats_visitor.StatsVisitor()
        sv.visit(stmt_list)
    
    def test_while_inv(self):
        prg1 = "x:=10; while x>5 inv y>5 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        sv = stats_visitor.StatsVisitor()
        sv.count(ast1)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 2)