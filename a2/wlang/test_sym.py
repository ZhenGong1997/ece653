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

import unittest

from . import ast, sym
import z3

class TestSym (unittest.TestCase):
    def test_extra1(self):
        st = sym.SymState()
        st.is_error()
        st.__repr__()   
        print(st)
        st.to_smt2()
        # sym._parse_args()
       
    
    def test_extra2(self):
        st = sym.SymState()
        r = z3.IntVal(1) > z3.IntVal(1)
        st._solver.add(r)
        st.pick_concrete()
    
    # stmtList, asgnstmt, print, skip
    def test_1(self):
        prg1 = "x:=1; print_state; skip"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    
    # cover sym.py:39 false branch
    def test_2(self):
        prg1 = "x:=1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState(solver=z3.Solver())
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    # This test case is from q1, we know it will return us 3 feasible paths
    def test_3(self):
        prg1 = "havoc x,y; if x+y>15 then {x:=x+7; y:=y-12} else {y:=y+10; x:=x-2}; x:=x+2;\
            if(2*x+2*y)>21 then {x:=x*3; y:=y*2} else{x:=x*4;y:=y*3+x}"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
  
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 3)
    
    def test_4(self):
        prg1 = "if not true and false or false then x:=2"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    # branch cover RelExp
    def test_5(self):
        prg1 = "havoc x,y,z; if x<=y and x<z or y>=x and 1=1 then x:=x/2;w:=x+y"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 2)

    # Test whileStmt
    def test_6(self):
        prg1 = "havoc x; while x>1 inv x<4 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 3)

    # Test whileStmt: branch coverage
    def test_7(self):
        prg1 = "havoc x; y:=2; while x>1 inv y>0 do {x:=x-1; y:=y-1}"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 2)

    # Test whileStmt: no inv
    def test_8(self):
        prg1 = "havoc x; while x>1 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 11)

    def test_9(self):
        prg1 = "x:=10; while (not (x=10)) do x:=x-1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)
    
    # Test whileStmt: branch coverage
    def test_10(self):
        prg1 = "x:=10; while true inv x>11 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)
    
    # Test whileStmt: branch coverage
    def test_11(self):
        prg1 = "x:=10; while x>5 do x:=x-1"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 1)

    # test: assumeStmt
    def test_12(self):
        prg1 = "x:=10; assume x=10; assume x=5 "
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)

    # test: assertStmt
    def test_13(self):
        prg1 = "x:=10; assert x=10; assert x=5"
        ast1 = ast.parse_string(prg1)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(ast1, st)]
        self.assertEquals(len(out), 0)
    

    # test: illegal operator, this test will raise Assertion Error
    def test_14(self):
        ae1 = ast.AExp(['+'], [ast.IntConst("1"), ast.IntConst("2")])
        ae2 = ast.AExp(['+'], [ast.IntConst("1"), ast.IntConst("2")])
        Ast = ast.RelExp(ae1, ["?"], ae2)
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(Ast, st)]
    
    # test: illegal operator, this test will raise Assertion Error
    def test_15(self):
        Ast = ast.AExp(['**'], [ast.IntConst("1"), ast.IntConst("2")])
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(Ast, st)]

    # test: illegal operator, this test will raise Assertion Error
    def test_16(self):
        ae1 = ast.AExp(['+'], [ast.IntConst("1"), ast.IntConst("2")])
        ae2 = ast.AExp(['+'], [ast.IntConst("1"), ast.IntConst("2")])
        Ast = ast.BExp(["?"], [ae1,ae2])
        engine = sym.SymExec()
        st = sym.SymState()
        out = [s for s in engine.run(Ast, st)]
    
    # symbolic execution engine diverges when running this test
    # Please uncomment this test for marking Q4e
    # def test_17(self):
    #     ast1 = ast.parse_file("wlang/diverge.wl")
    #     engine = sym.SymExec()
    #     st = sym.SymState()
    #     out = [s for s in engine.run(ast1, st)]
    #     self.assertEquals(len(out), 2662)
