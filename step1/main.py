import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser


def main():
    input  = InputStream(sys.stdin.read())
    lexer  = ExprLexer(input)
    tokens = CommonTokenStream(lexer)
    parser = ExprParser(tokens)
    parser._errHandler = BailErrorStrategy() # 设置错误处理
    tree   = parser.expr() # 取得一棵以 expr 为根的 AST
    print(tree.toStringTree(recog=parser))


if __name__ == '__main__':
    main()

