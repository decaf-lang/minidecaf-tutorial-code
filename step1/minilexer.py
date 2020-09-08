import re


class TokenKind:
    def __init__(self, name:str, ptn:str, action=None):
        """name 比如 Identifier, Integer，ptn 是一个正则表达式。
        action 可以是 "skip" 或者 "error"，方便忽略空白字符和报错"""
        assert action in { None, "skip", "error" }
        self.name = name
        self.ptn = re.compile('^' + ptn) # ^ 表示输入开头
        self.action = action

    def matchLength(self, txt:str):
        m = self.ptn.search(txt)
        if m is not None:
            return m.span()[1]
        return 0


class Token:
    def __init__(self, kind:TokenKind, text:str):
        self.kind = kind
        self.text = text


class Lexer:
    def __init__(self, tokenKinds:list):
        self.tokenKinds = tokenKinds

    def setInput(self, txt:str):
        self.txt = txt
        self.pos = 0

    def lex(self):
        """用 yield 返回一个 generator，表示 token stream，后续阶段按需从 generator 里面拿 token。
        与之相对的是一口气做完所有词法分析，然后返回一个列表，包含了所有的 token。"""
        while len(self.txt) != 0:
            matchResult = [tk.matchLength(self.txt) for tk in self.tokenKinds]
            # 如果有多个最大值, max 返回第一个
            i, l = max(enumerate(matchResult), key=lambda x:x[1])
            tk = self.tokenKinds[i]
            if tk.action == "skip":
                pass
            elif tk.action == "error":
                raise Exception(f"lex error at input position {self.pos}")
            else:
                yield Token(tk, self.txt[:l])
            self.txt = self.txt[l:]
            self.pos += l


def default():
    identLeadChar = "[a-zA-Z_]"
    digitChar = "[0-9]"
    wordChar = "[a-zA-Z0-9_]"
    whitespaceChar = "[ \r\n\t]"

    lexer = Lexer([
        # 关键字。每个关键字用一个单独的 Token 描述。
        TokenKind("Int", "int"),
        TokenKind("Return", "return"),
        # 标点符号。
        TokenKind("Lbrace", "\\{"),
        TokenKind("Rbrace", "\\}"),
        TokenKind("Lparen", "\\("),
        TokenKind("Rparen", "\\)"),
        TokenKind("Semicolon", ";"),
        # 标识符。
        TokenKind("Identifier", f"{identLeadChar}{wordChar}*"),
        # 整数。非负，可以有前导零。
        TokenKind("Integer", f"{digitChar}+"),
        # 空白。所有空白都被忽略。
        TokenKind("Whitespace", f"{whitespaceChar}+", action="skip"),
        # 我们不认识的字符（比如汉字），报错。
        TokenKind("Error", f".", action="error"),
    ])

    lexer.setInput("""\
    int main() {
        return 123;
    }
    """)
    return lexer


def dumpLexerTokens(lexer):
    print(f"{'token kind':<12} {'text':<20}")
    print(f"{'-'*11:<12} {'-'*19:<20}")
    for tok in lexer.lex():
        print(f"{tok.kind.name:<12} {tok.text:<20}")


if __name__ == "__main__":
    dumpLexerTokens(default())
