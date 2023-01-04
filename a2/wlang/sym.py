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

# Reference : https://github.com/Youlina3/ECE653a3/blob/master/wlang/sym.py
import sys

import io 
import z3

from . import ast, int
from functools import reduce

class SymState(object):
    def __init__(self, solver=None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver()

        # true if this is an error state
        self._is_error = False

    def add_pc(self, *exp):
        """Add constraints to the path condition"""
        self.path.extend(exp)
        self._solver.append(exp)

    def is_error(self):
        return self._is_error

    def mk_error(self):
        self._is_error = True

    def is_empty(self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check()
        return res == z3.unsat

    def pick_concrete(self):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""
        res = self._solver.check()
        if res != z3.sat:
            return None
        model = self._solver.model()
        st = int.State()
        for (k, v) in self.env.items():
            st.env[k] = model.eval(v)
        return st

    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState()
        child.env = dict(self.env)
        child.add_pc(*self.path)

        return (self, child)

    def __repr__(self):
        return str(self)

    def to_smt2(self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2()

    def __str__(self):
        buf = io.StringIO()
        for k, v in self.env.items():
            buf.write(str(k))
            buf.write(': ')
            buf.write(str(v))
            buf.write('\n')
        buf.write('pc: ')
        buf.write(str(self.path))
        buf.write('\n')

        return buf.getvalue()


class SymExec(ast.AstVisitor):
    def __init__(self):
        pass

    def run(self, ast, state):
        # set things up and
        # call self.visit (ast, state=state)
        return self.visit(ast, state=state)

    def visit_IntVar(self, node, *args, **kwargs):
        return kwargs['state'].env[node.name]

    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal(node.val)

    def visit_IntConst(self, node, *args, **kwargs):
        return z3.IntVal(node.val)

    def visit_RelExp(self, node, *args, **kwargs):
        lhs = self.visit(node.arg(0), *args, **kwargs)
        rhs = self.visit(node.arg(1), *args, **kwargs)
        if node.op == "<=":
            return lhs <= rhs
        if node.op == "<":
            return lhs < rhs
        if node.op == "=":
            return lhs == rhs
        if node.op == ">=":
            return lhs >= rhs
        if node.op == ">":
            return lhs > rhs
        # raise error if operator is invalid 
        assert False

    def visit_BExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        if node.op == "not":
            assert node.is_unary()
            assert len(kids) == 1
            return z3.Not(kids[0]) 

        elif node.op == "and":
            return z3.And(*kids)
        elif node.op == "or":
            return z3.Or(*kids)

        # raise error if logical operator is invalid 
        assert False

    def visit_AExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        fn = None

        if node.op == "+":
            fn = lambda x, y: x + y

        elif node.op == "-":
            fn = lambda x, y: x - y

        elif node.op == "*":
            fn = lambda x, y: x * y

        elif node.op == "/":
            fn = lambda x, y: x / y

        assert fn is not None
        return reduce(fn, kids)

    def visit_SkipStmt(self, node, *args, **kwargs):
        return [kwargs['state']]

    def visit_PrintStateStmt(self, node, *args, **kwargs):
        print([kwargs['state']])
        return [kwargs['state']]

    def visit_AsgnStmt(self, node, *args, **kwargs):
        exp = self.visit(node.rhs, *args, **kwargs)
        var = node.lhs.name
        st = kwargs['state']
        if var not in st.env:
            st.env[var] = z3.FreshInt(var)
        st.env[var] = exp
        return [st]
     

    def visit_IfStmt(self, node, *args, **kwargs):
        states = []
        cond = self.visit(node.cond, *args, **kwargs)
        st = kwargs['state']

        st1, st2 = st.fork()
        st1.add_pc(cond)
        if not st1.is_empty():
            states.extend(self.visit(node.then_stmt, state = st1))

        st2.add_pc(z3.Not(cond))
        if not st2.is_empty():
            if node.has_else():
                states.extend(self.visit(node.else_stmt, state=st2))
            else:
                states.extend([st2])
        return states

    def visit_WhileStmt(self, node, *args, **kwargs):
        states = []
        # get condition and inv part
        cond = self.visit (node.cond, * args, ** kwargs)
        inv = node.inv
        st = kwargs['state']
        
        st0, st1 = st.fork()
        st0.add_pc(z3.Not(cond))
        # Add to result path: do not enter the loop
        if not st0.is_empty():
            states.extend([st0])

        # SAT path: enter the loop， at most iteration 10 times
        st1.add_pc(cond)
        if not st1.is_empty():
    
            if node.inv is not None:
                st1,st2 = st1.fork()
                st2.add_pc(z3.Not(self.visit(node.inv, state = st1)))
                # st2 check inv regulation upon entering the loop 
                if not st2.is_empty():
                    print("inv may fail when first entering the loop, under\n", st1)
                    print("on ", inv)
                    print("if ", st2.pick_concrete())
                    st2.mk_error()
                st1.add_pc(self.visit(node.inv, state = st1))
            else:
                st1 = st1
            # SAT path: satisfy inv or no inv, enter first iteration
            if not st1.is_empty():
                start_states = [st1]   
                # the reason we iterate 11 times is that in last round we only check if #10 states can exit        
                for iter in range(0,11):   
                    finish_states = [] 
                    temp_states = []          
                    for each_state in start_states:    
                        cond = self.visit(node.cond, state = each_state)
                        # check cond except for first entering the loop
                        st0_cond, st1_cond = each_state.fork()
                        if(iter != 0):     
                            st0_cond.add_pc(z3.Not(cond))
                            # Add to result path: sym state can exit the loop
                            if not st0_cond.is_empty():
                                states.extend([st0_cond])

                        if iter == 0:
                            st = self.visit(node.body, state = each_state)
                            # finish_state stores the surviving states after executing loop body
                            temp_states.extend(st) 
                    
                        # will check exit condition SAT for iteration # 10, but need to stop visit loop body in # 11   
                        elif iter>0 and iter<10:
                            cond = self.visit (node.cond, state=st1_cond)
                            st1_cond.add_pc(cond)
                            # execute loop body if st1.pc ^ cond is SAT
                            if not st1_cond.is_empty():
                                st = self.visit(node.body, state = st1_cond)
                                # finish_state stores the surviving states after executing loop body
                                temp_states.extend(st) 

                        # check if inv still holds after each iteration
                        if node.inv is not None:
                            
                            for state in temp_states:
                                inv = self.visit (node.inv, state = state)
                                inv_st1, inv_st2 = state.fork()
                                inv_st1.add_pc(z3.Not(self.visit(node.inv, state = state)))
                                # abort path violate inv
                                if not inv_st1.is_empty():
                                    print("inv may fail at iteration {}".format(iter+1))
                                    print("under\n", state)
                                    print("on ", inv)
                                    print("if ", inv_st1.pick_concrete())
                                inv_st2.add_pc(inv)
                                # path SAT inv survived
                                if not inv_st2.is_empty():
                                    finish_states.append(inv_st2)
                        else:
                            finish_states = temp_states
                    start_states = finish_states
        return states

    
    def visit_AssertStmt(self, node, *args, **kwargs):
        # Don't forget to print an error message if an assertion might be violated
      
        cond = self.visit (node.cond, * args, ** kwargs)
        st0, st1 = kwargs['state'].fork()
        st0.add_pc(z3.Not(cond))
        # assertion may fail on cond, handle error
        if not st0.is_empty():
            print("Assertion may fail for\n", st1)
            print("on ", node.cond)
            print("if ", st0.pick_concrete())
            st0.mk_error()

        # assertion pass, check pc satisfiability
        st1.add_pc(cond)
        if st1.is_empty(): return []
        else: return [st1]

    def visit_AssumeStmt(self, node, *args, **kwargs):
        cond = self.visit(node.cond, *args, **kwargs)
        st = kwargs['state']
        st.add_pc(cond)
        if st.is_empty(): return []
        else: return [st]

    def visit_HavocStmt(self, node, *args, **kwargs):
        st = kwargs['state']
        for var in node.vars:
            st.env [var.name] = z3.FreshInt (var.name)
        return [st]

    def visit_StmtList(self, node, *args, **kwargs):
        start_states = [kwargs['state']] 
        for stmt in node.stmts:
            finish_states = []
            for state in start_states:
                # st will get 0,1,2 states depend on the visited stmt 
                st = self.visit(stmt, state = state)
                finish_states.extend(st)
            # update the symbolic state for the next coming statement
            start_states = finish_states
        return start_states


def _parse_args():
    import argparse
    ap = argparse.ArgumentParser(prog='sym',
                                 description='WLang Interpreter')
    ap.add_argument('in_file', metavar='FILE',
                    help='WLang program to interpret')
    args = ap.parse_args()
    return args


def main():
    args = _parse_args()
    prg = ast.parse_file(args.in_file)
    st = SymState()
    sym = SymExec()

    states = sym.run(prg, st)
    if states is None:
        print('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print('[symexec]: symbolic state reached')
            print(out)
        print('[symexec]: found', count, 'symbolic states')
    return 0


if __name__ == '__main__':
    sys.exit(main())
