from sly import Lexer

class DLangLexer(Lexer):
    tokens = {BOOLEAN, KEYWORD, IDENTIFIER, INTEGER, DOUBLE, STRING, OPERATOR, COMMENT}

    # Ignored characters
    ignore = ' \t\r'

    # Token patterns
    COMMENT = r'//.*|/\*(.|\n)*?\*/'
    KEYWORD = r'\b(nothing|int|double|bool|string|class|interface|null|this|extends|implements|for|while|if|else|return|break|new|ArrayInstance|Output|InputInt|InputLine)\b'
    BOOLEAN = r'\b(True|False)\b'
    INTEGER = r'\b\d+\b'
    DOUBLE = r'\b\d+\.\d*([Ee][+-]?\d+)?\b|\b\d+[Ee][+-]?\d+\b'
    STRING = r'"[^"\n]*"'
    OPERATOR = r'\+|-|\*|/|%|<=?|>=?|==?|!=|&&|\|\||!|;|,|\.|[\[\](){}]'

    # Boolean validation
    @_(r'\b(True|False)\b')
    def BOOLEAN(self, t):
        if t.value not in {'True', 'False'}:
            print(f"Error: Invalid boolean literal '{t.value}' at line {self.lineno}")
            return None
        return t

    # Identifier pattern with length check
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def IDENTIFIER(self, t):
        if len(t.value) > 50:
            print(f"Error: Identifier '{t.value}' exceeds maximum length of 50 characters at line {self.lineno}")
            return None
        if t.value in self.keywords:
            t.type = 'KEYWORD'
        return t

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Error handling
    def error(self, t):
        print(f"Lexical error: Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

    # Priority handling for keywords vs identifiers
    keywords = {'nothing', 'int', 'double', 'bool', 'string', 'class', 'interface', 'null', 'this', 'extends', 'implements', 'for', 'while', 'if', 'else', 'return', 'break', 'new', 'ArrayInstance', 'Output', 'InputInt', 'InputLine'}

def analyze_code(lexer, code):
    tokens = lexer.tokenize(code)
    if not tokens:
        print("No tokens found. Please enter valid DLang code.")
    else:
        for tok in tokens:
            print(f'type={tok.type}, value={tok.value}')

if __name__ == '__main__':
    lexer = DLangLexer()
    
    print("DLang Lexical Analyzer")
    print("Enter 'file' to read from 'input.txt', 'input' to enter code manually, or 'exit' to quit.")

    while True:
        user_option = input("Enter your choice (file/input/exit): ").lower()

        if user_option == 'exit':
            print("Exiting the program.")
            break
        elif user_option == 'file':
            try:
                with open('input.txt', 'r') as file:
                    text = file.read()
                print("Analyzing code from 'input.txt':")
                analyze_code(lexer, text)
            except FileNotFoundError:
                print("Error: 'input.txt' not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif user_option == 'input':
            print("Enter your DLang code (type 'END' on a new line to finish):")
            code_lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                code_lines.append(line)
            code = '\n'.join(code_lines)
            print("Analyzing input code:")
            analyze_code(lexer, code)
        else:
            print("Invalid choice. Please enter 'file', 'input', or 'exit'.")

    print("Lexical analysis complete.")
