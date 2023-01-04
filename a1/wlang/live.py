# from . import ast

# def main():
#     ast1 = ast.parse_string('x := 10; {if x>5 then y := 20 else y:=1} ; z := x+y; print_state')
#     print(ast1)
#     print(list(ast1.stmts))

#     print('This program has %s statements' % len(list(ast1.stmts)))

# class StmtCounter1(ast.AstVisitor):
#     def __init__(self):
#         super().__init__()
    
#     def visit_Stmt(self, node, *args, **kargs):
#         return 1
    
#     def visit_StmtList(self, node, *args, **kargs):
#         # we need to descant the statements (to its children), otherwise it will only count the top-level number of stmts
#         # for example, if x>5 then y:=10 else y:=20, we expect counting 3 statements, but if without descanting, we only count 1
#         res = 0
#         for s in node.stmts:
#             res =  res + self.visit(s, *args, **kargs)
#         return res

#     def visit_IfStmt(self, node, *args, **kwargs):
#         # find node.field in the ast.py file, class IfStmt
#         # 1 is the if statement itself
#         res = 1 + self.visit(node.then_stmt, *args, **kwargs)
#         # either we use 1 or, uncomment next line and remove the 1 in previous line
#         # res = self.visit_Stmt(self, node, *args, *kwargs)
#         if node.has_else():
#             res += self.visit(node.else_stmt, *args, *kwargs)
#         return res

# if __name__ == '__main__':
#     main()