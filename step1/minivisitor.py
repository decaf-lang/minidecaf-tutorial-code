import miniparser



def accept(self, visitor):
    if self.label == "program":    return visitor.visitProgram(self)
    if self.label == "function":   return visitor.visitFunction(self)
    if self.label == "type":       return visitor.visitType(self)
    if self.label == "statement":  return visitor.visitStatement(self)
    if self.label == "expression": return visitor.visitExpression(self)
    raise Exception("bad node")

# 给 Node 实现 accept 方法，一种不太好的写法
miniparser.Node.accept = accept


class Visitor:
    """默认行为是遍历、但什么也不做"""
    def visitProgram(self, node:miniparser.Node):
        node.children[0].accept(self) # func

    def visitFunction(self, node:miniparser.Node):
        node.children[0].accept(self) # ty
        node.children[5].accept(self) # stmt

    def visitType(self, node:miniparser.Node):
        pass

    def visitStatement(self, node:miniparser.Node):
        node.children[1].accept(self) # expr

    def visitExpression(self, node:miniparser.Node):
        pass


class TargetCodeEmission(Visitor):
    def visitFunction(self, node:miniparser.Node):
        ident = node.children[1]
        if ident.text != "main":
            raise Exception(f"function name expected 'main', found '{ident.text}'")
        Visitor.visitFunction(self, node)

    def visitStatement(self, node:miniparser.Node):
        expr = node.children[1]
        Integer = expr.children[0]
        value = int(Integer.text)
        # 简单的语义检查：int 范围正确
        if value < -2147483648 or value >= 2147483648:
            raise Exception(f"{value} is too large for int")
        # 下面的就是汇编模板
        print(f""".text
	.globl	main
main:
	li	a0,{value}
	ret""")


def default():
    parser = miniparser.default()
    ast = parser.parse("program")
    visitor = TargetCodeEmission()
    ast.accept(visitor)


if __name__ == "__main__":
    default()
