#include "ExprLex.h"
#include "ExprParser.h"
#include <iostream>

int main() {
    antlr4::ANTLRInputStream input(std::cin);
    ExprLex lexer(&input);
    antlr4::CommonTokenStream tokens(&lexer);
    ExprParser parser(&tokens);
    auto tree = parser.expr();
    std::cout << tree->toStringTree(&parser) << std::endl;
    return 0;
}

