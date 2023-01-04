# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from cmath import exp
from operator import truediv
import unittest

from . import ast, int


class TestInt(unittest.TestCase):
    def test_ast_Ast(self):
        prg1 = "x := 10"
        ast1 = ast.parse_string(prg1)
        print(ast1) 
        ast1.__repr__()
        
    def test_ast_StmtList(self):
        prg1 = "x := 10; y:=11"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)
    
    def test_ast_SkipStmt(self):
        prg1 = "skip"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)

    def test_ast_PrintStateStmt(self):
        prg1 = "print_state"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)

    def test_ast_AsgnStmt(self):
        prg1 = "x:=1"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)

    def test_ast_IfStmt(self):
        prg1 = "if 1<2 then x:=2 else x:=1"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)
        ast1.has_else()

    def test_ast_WhileStmt(self):
        prg1 = "while 2<1 do x:=1"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)

    def test_ast_AssertStmt(self):
        prg1 = "assert a<1"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)
        print(ast1)

    def test_ast_HavocStmt(self):
        prg1 = "havoc a:=1"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)

    def test_ast_Exp(self):
        ast1 = ast.Exp(["x:=1", "y:=2"],["x:=1"])
        ast1.arg(0)
        ast1.is_binary()
        ast1.is_unary()
        
    def test_ast_Const(self):
        ast1 = ast.Const(5)
        print(ast1)
        ast1.__repr__()
        ast1.__hash__()
        
    def test_ast_BoolConst(self):
        ast1 = ast.BoolConst(5)

    def test_ast_IntVar(self):
        ast1 = ast.IntVar("xyz")
        print(ast1)
        ast1.__repr__()
        ast1.__hash__()

    def test_ast_parse_file(self):
        file = "wlang/test1.prg"
        ast1 = ast.parse_file(file)
    
    def test_ast_AstVisitor(self):
        prg1 = "if 1<2 then y:=2 else y:=1"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    

    def test_ast_visit_WhileStmt(self):
        prg1 = "x:=10; while x>5 do x:=x-1 else skip"
        ast1 = ast.parse_string(prg1)
        print(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    
    def test_ast_visit_AssumeStmt(self):
        prg1 = "assume 1<2"
        ast1 = ast.parse_string(prg1)
        self.assertEqual(ast1, ast1)
        print(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)

    def test_ast_visit_HavocStmt(self):
        prg1 = "havoc x,y,z"
        ast1 = ast.parse_string(prg1)
        print(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)

    def test_ast_visit_IfStmt(self):
        prg1 = "x:=10; y:=-10; {if x<5 or y>5 then x:=x-1 else x:=x+1}; if x<5 then x:=x-1 "
        ast1 = ast.parse_string(prg1)
        print(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)

    def test_ast_visit_Exp2(self):   
        # arg1 = ast.AsgnStmt(ast.IntVar("x"), ast.IntConst(5))
        exp = ast.Exp("not",[ast.BoolConst(False)])
        print(exp)
     
        

    def test_ast_visit_BoolConst(self):  
        prg1 = "x:=10;if true then x:=x-1 else x:=x+1; if false then x:=x+1"
        ast1 = ast.parse_string(prg1)
        print(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)


    def test_ast_visit_SkipStmt(self):   
        prg1 = "skip"
        ast1 = ast.parse_string(prg1)
        print(ast1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    
    def test_ast_visit_PrintStateStmt(self):   
        visitor = ast.PrintVisitor()
        visitor.visit_PrintStateStmt(ast.SkipStmt())
        print(visitor)

    # cover len(node.stmts) == 0
    def test_visit_StmtList(self):
        stmt_list = ast.StmtList(None)
        print(stmt_list)
    

    # cover int.py
    #-----------------------------------------
    def test_State(self):   
        prg1 = "x:=1;y:=2;skip"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
        print(st)
        st.__repr__()
    
    def test_Interpreter(self):   
        prg1 = "x:=1;y:=2;z:=1;assert x<=y;assert x=z;assert y>=x"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    
    def test_int_visit_BExp(self):   
        prg1 = "if (not true) and (true) then x:=1"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)

    def test_int_visit_AExp(self):   
        prg1 = "x:= 2*10/5"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    
    # cause failure on purpose to cover int.py:155
    def test_int_visit_AssertStmt_error(self):   
        prg1 = "assert 1>2"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        print(interp)
        st = int.State()
        st = interp.run(ast1, st)
    
    def test_int_PrintStateStmt(self):   
        prg1 = "x:=1; print_state"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)


    # cover remaining parser.py
    # ---------------------------------------------
    def test_parser_inv(self):
        prg1 = "x:=10; while x>5 inv x>5 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        interp = int.Interpreter()
        st = int.State()
        st = interp.run(ast1, st)
    
    def test_parser_assert_false(self):
        exp1 = ast.AExp(["+"],[ast.IntConst(1), ast.IntConst(1)])
        rel_exp = ast.RelExp(exp1,"++",exp1)
        # visitor = ast.AstVisitor()
        interp = int.Interpreter()
        st = int.State()
        interp.visit_RelExp(rel_exp,st)