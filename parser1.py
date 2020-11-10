#
# Graham Hopkins
#
# 22 Oct 2020
#
#
# From Writing Interpreters and Compilers for the Raspberry Pi Using Python
#
# By Anthony J, Dos Reis
#
import sys


class Token:
    def __init__(self, line, column, category, lexeme):
        self.line = line
        self.column = column
        self.category = category
        self.lexeme = lexeme


# constants for token categories
EOF = 0  # end of file
PRINT = 1  # 'print' keyword
UNSIGNEDINT = 2  # integer
NAME = 3  # identifier that is not a keyword
ASSIGNOP = 4  # '=' assignment operator
LEFTPAREN = 5  # '('
RIGHTPAREN = 6  # ')'
PLUS = 7  # '+'
MINUS = 8  # '-'
TIMES = 9  # '•'
NEWLINE = 10  # newline character
ERROR = 11  # if not defined above then error

# global variables
trace = True
source = ''
sourceindex = 0
line = 0
column = 0
tokenlist = []
tokenindex = -1
prevchar = '\n'
blankline = True
token = None

# displayable names for each token category
catnames = ['EOF', 'PRINT', 'UNSIGNEDINT', 'NAME', 'ASSIGNOP', 'LEFTPAREN', 'RIGHTPAREN', 'PLUS', 'MINUS', 'TIMES',
            'NEWLINE', 'ERROR']

# keywords and their token categories
keywords = {'print': PRINT}

# one-character tokens and their token categories
smalltokens = {'=': ASSIGNOP, '(': LEFTPAREN, ')': RIGHTPAREN, '+': PLUS, '-': MINUS,
               '*': TIMES, '\n': NEWLINE, '': EOF}


def tokenizer():
    global token
    curchar = ' '  # prime curchar with a space

    while True:
        # skip whitespace but not newlines
        while curchar != '\n' and curchar.isspace():
            curchar = getchar()  # get the next char from the source program

        # construct and initialize a new token
        token = Token(line, column, None, '')

        if curchar.isdigit():  # start of unsigned integer ?
            token.category = UNSIGNEDINT  # save category of token
            while True:
                token.lexeme += curchar
                curchar = getchar()
                if not curchar.isdigit():  # break if not digit
                    break
        elif curchar.isalpha() or curchar == '_':  # start of name ?
            while True:
                token.lexeme += curchar
                curchar = getchar()
                # break oif not letter, "_' or digit
                if not (curchar.isalnum() or curchar == '_'):
                    break

            # determine if lexeme is a keyword or the name of a variable
            if token.lexeme in keywords:
                token.category = keywords[token.lexeme]
            else:
                token.category = NAME
        elif curchar in smalltokens:
            token.category = smalltokens[curchar]
            token.lexeme = curchar
            curchar = getchar()  # more to first character after token
        else:
            token.category = ERROR
            token.lexeme = curchar
            raise RuntimeError('Invalid Token')

        tokenlist.append(token)
        if trace:
            print(f'{str(token.line):7}{str(token.column):5}{catnames[token.category]:15}{token.lexeme:10}')

        if token.category == EOF:
            break


# getchar() gets next char from source and adjusts line and column

def getchar():
    global sourceindex, column, line, prevchar, blankline

    # check if starting a newline

    if prevchar == '\n':
        line += 1
        column = 0
        blankline = True  # initialise blank line

    if sourceindex >= len(source):  # at end of source code ?
        column = 1  # set EOF column to 1
        prevchar = ''  # save current char for next call
        return ''

    c = source[sourceindex]
    sourceindex += 1
    column += 1
    if not c.isspace():  # if c is not a space then the line is nøt blank
        blankline = False
    prevchar = c
    # if at the end of a blank line return a space in place of '\n'
    if c == '\n' and blankline:
        return ' '
    else:
        return c


# top level function of parser
def parser():
    advance()  # advance so token holds first token
    program()  # call function corresponding to start symbol


def advance():
    global token, tokenindex
    tokenindex += 1
    if tokenindex >= len(tokenlist):
        raise RuntimeError('Unexpected end of file')
    token = tokenlist[tokenindex]


def consume(expectedcat):
    if token.category == expectedcat:
        advance()
    else:
        raise RuntimeError('Expecting {catnames[expectedcat]')


def assignmentstmt():
    advance()
    consume(ASSIGNOP)
    expr()


def printstmt():
    advance()
    consume(LEFTPAREN)
    expr()
    consume(RIGHTPAREN)


def simplestmt():
    if token.category == NAME:
        assignmentstmt()
    elif token.category == PRINT:
        printstmt()
    else:
        raise RuntimeError('Expecting statement')


def stmt():
    simplestmt()
    consume(NEWLINE)


def term():
    factor()
    while token.category == TIMES:
        advance()
        factor()


def factor():
    if token.category == PLUS:
        advance()
        factor()
    elif token.category == MINUS:
        advance()
        factor()
    elif token.category == UNSIGNEDINT:
        advance()
    elif token.category == NAME:
        advance()
    elif token.category == LEFTPAREN:
        advance()
        expr()
        consume(RIGHTPAREN)
    else:
        raise RuntimeError('Expecting factor')


def expr():
    term()
    while token.category == PLUS:
        advance()
        term()


# <program> -> <stmt>* EOF

def program():
    while token.category in [NAME, PRINT]:
        stmt()
    if token.category != EOF:
        raise RuntimeError('Expecting end of file')


def main():
    global source
    if len(sys.argv) == 2:
        try:
            infile = open(sys.argv[1], 'r')
            source = infile.read()
        except IOError:
            print('Cannot read input file :sys.argv[1]')
    else:
        print('Wrong number of command line arguments')
        print('Format python parser1.py <input file>')
        sys.exit(1)

    if source[-1] != '\n':
        source = source + '\n'
    if trace:
        print('Line   Col  Category       Lexeme\n')

    try:
        tokenizer()
        parser()
    except RuntimeError as emsg:
        # output slash n in place of newline
        lexeme = token.lexeme.replace('\n', '\\n')
        print('\nError on ' + "'" + lexeme + "'" + ' line ' + str(token.line) + ' column ' + str(token.column))
        print(emsg)  # message from RuntimeError object
        sys.exit(1)


if __name__ == '__main__':
    main()
