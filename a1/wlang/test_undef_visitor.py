import unittest

from . import ast, undef_visitor


class TestUndefVisitor(unittest.TestCase):
    def test1(self):
        prg1 = "x := 10; y:= y + z; z:=x+1"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals (set (   [ast.IntVar('z'),ast.IntVar('y')   ]), uv.get_undefs ())

    def test_if_has_else(self):
        prg1 = "if x>4 then y:=z else z:=5"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals (set ([ast.IntVar('z'), ast.IntVar('x') ]), uv.get_undefs ())
    
    def test_if_no_else(self):
        prg1 = "if x>4 then y:=z"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals (set ([ast.IntVar('z'), ast.IntVar('x') ]), uv.get_undefs ())
    
    def test_while(self):
        prg1 = "while x > 0 do x:=x-y"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set ([ast.IntVar('x'),ast.IntVar('y')]), uv.get_undefs ())

    def test_while_inv(self):
            prg1 = "x:=10; while x>5 inv y>5 do x:=x-1"
            ast1 = ast.parse_string(prg1)
            uv = undef_visitor.UndefVisitor()
            uv.check(ast1)
            self.assertEquals(set ([ast.IntVar('y')]), uv.get_undefs ())

    def test_assert(self):
        prg1 = "assert x=1"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set ([ast.IntVar('x')]), uv.get_undefs ())

    def test_assume(self):
        prg1 = "assume x+y>10"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set ([ast.IntVar('x'),ast.IntVar('y')]), uv.get_undefs ())

    def test_havoc(self):
        prg1 = "havoc x,y"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set (), uv.get_undefs ())

    # def test_line69_branch(self):
    #     uv = undef_visitor.UndefVisitor()
    #     uv._vars_def.add(ast.IntVar('x'))
    #     uv.visit_IntVar(ast.IntVar('x'))
    
    def test_StmtList_None(self):
        ast1 = ast.StmtList(None)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
    
    def test_Visit_Stmt(self):
        ast1 = ast.Stmt()
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)

    def test_pdf_sample(self):
        prg1 = "havoc x; {if x>10 then y:=x-1 else z:=10}; x:=z+1"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set ([ast.IntVar('z')]), uv.get_undefs ())
    
    def test_pdf_sample2(self):
        prg1 = "x:=10; if x<5 then y:=1 else y:=2; z:=y+1 "
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set (), uv.get_undefs ())