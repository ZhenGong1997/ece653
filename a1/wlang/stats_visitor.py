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

from . import ast


class StatsVisitor(ast.AstVisitor):
    """Statistics gathering visitor"""

    def __init__(self):
        super(StatsVisitor, self).__init__()
        # number of statements visited
        self._num_stmts = 0
        # the set of all visited variables
        self._vars = set()

    def get_num_stmts(self):
        """Returns number of statements visited"""
        return self._num_stmts

    def get_num_vars(self):
        """Returns number of distinct variables visited"""
        # delete print after debugging
        return len(self._vars)

    def count(self, node, *args, **kwargs):
        self._num_stmts = 0
        self.visit(node, *args, **kwargs)

    def visit_StmtList(self, node, *args, **kwargs):
        if node.stmts is None:
            return
        for s in node.stmts:
            self.visit(s)

    def visit_Stmt(self, node, *args, **kwargs):
        self._num_stmts = self._num_stmts + 1

    def visit_IntVar(self, node, *args, **kwargs):
        # root: count num_of var
        self._vars.add(node.name)
        pass

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        self._num_stmts += 1
        # count num_of var
        self.visit(node.lhs)
        self.visit(node.rhs)
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node)
        self.visit(node.then_stmt)
        if node.has_else():
            self.visit(node.else_stmt)
        
    def visit_WhileStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node)
        if node.inv:
            self.visit(node.inv)
        self.visit(node.body)
     
    def visit_AssertStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node)

        # count num_of var
        self.visit(node.cond)
        pass

    def visit_AssumeStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node)

        # count num_of var
        self.visit(node.cond)
        pass

    def visit_HavocStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node)
        # count num_of var
        for var in node.vars:
            self.visit(var)
        pass

    def visit_Exp(self, node, *args, **kwargs):
        # count num_of var
        for var in node.args:  
            self.visit(var)            
        pass


def main():
    import sys

    prg = ast.parse_file(sys.argv[1])
    sv = StatsVisitor()
    sv.visit(prg)
    print("stmts:", sv.get_num_stmts(), "vars:", sv.get_num_vars())


if __name__ == "__main__":
    import sys

    sys.exit(main())
